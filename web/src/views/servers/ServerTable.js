import React, { useEffect, useState } from 'react'
import {
  CTable,
  CTableHead,
  CTableRow,
  CTableHeaderCell,
  CTableBody,
  CButton,
  CDropdownMenu,
  CDropdownToggle,
  CDropdown,
  CDropdownItem,
  CTableDataCell,
} from '@coreui/react'
import { API_URLS } from 'src/components'
import axios from 'axios'
import { useSelector } from 'react-redux'

const ServerTable = (ctx) => {
  const [runOnce, setRunOnce] = useState(false)
  const [vms, setVMs] = useState([])
  const socket = useSelector((state) => state.ws.socket)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(API_URLS['LIST_VMS'], { withCredentials: true })
        const data = response.data
        ctx.setLoading(false)
        setVMs(data.vms) // Update the state with the retrieved data
      } catch (error) {
        console.error('Error fetching VM data:', error)
        window.location = '/#/login'
      }
    }

    if (!runOnce) {
      setRunOnce(true)
      fetchData()
    }

    if (socket) {
      socket.on('INSTANCE_STATUS', (vm_status) => {
        setVMs((prevData) => {
          const newData = prevData.map((vm) => {
            if (vm.id === vm_status.vm_id) {
              if (vm_status.status === 'DELETED') {
                return null
              }
              return { ...vm, status: vm_status.status }
            }
            return vm
          })
          return newData.filter((vm) => vm !== null)
        })
      })

      socket.on('INSTANCE_UPDATE', (vm_update) => {
        setVMs((prevData) => {
          const newData = prevData.map((vm) => {
            if (vm.id === vm_update.vm_id) {
              if (vm_update.vm.status === 'DELETED') {
                return null
              }
              return vm_update.vm
            }
            return vm
          })
          return newData.filter((vm) => vm !== null)
        })
      })

      socket.on('INSTANCE_CREATE', (vm) => {
        fetchData()
      })
    }
  }, [ctx, runOnce, socket]) // Empty dependency array to run the effect only once on component mount

  const startStopVM = async (vm_id, status) => {
    var action_url = ''
    if (status === 'REBOOT') {
      action_url = API_URLS['REBOOT_VM']
    } else if (status === 'SHUTOFF') {
      action_url = API_URLS['START_VM']
    } else if (status === 'ACTIVE') {
      action_url = API_URLS['STOP_VM']
    } else {
      console.error('unknown vm power action')
      return
    }

    try {
      await axios.get(action_url + '?vm_id=' + vm_id, { withCredentials: true })
    } catch (error) {
      console.error('Request Error:', error)
    }
  }

  return (
    <CTable>
      <CTableHead>
        <CTableRow>
          <CTableHeaderCell scope="col">Name</CTableHeaderCell>
          <CTableHeaderCell scope="col">IP Address</CTableHeaderCell>
          <CTableHeaderCell scope="col">vCPUs</CTableHeaderCell>
          <CTableHeaderCell scope="col">Memory</CTableHeaderCell>
          <CTableHeaderCell scope="col">Disk</CTableHeaderCell>
          <CTableHeaderCell scope="col">Status</CTableHeaderCell>
          <CTableHeaderCell scope="col">Actions</CTableHeaderCell>
        </CTableRow>
      </CTableHead>
      <CTableBody>
        {vms.map((vm) => (
          <CTableRow key={vm.id}>
            <CTableDataCell>{vm.name}</CTableDataCell>
            <CTableDataCell>{vm.ip !== '' ? vm.ip : 'No IP'}</CTableDataCell>
            <CTableDataCell>{vm.vcpus}</CTableDataCell>
            <CTableDataCell>{vm.memory}</CTableDataCell>
            <CTableDataCell>{vm.disk} GB</CTableDataCell>
            <CTableDataCell>{vm.status}</CTableDataCell>
            <CTableDataCell>
              <CDropdown variant="btn-group" key={vm.id}>
                <CButton
                  disabled={
                    vm.status === 'STARTING' ||
                    vm.status === 'STOPPING' ||
                    vm.status === 'REBOOTING'
                      ? true
                      : false
                  }
                  color={vm.status === 'SHUTOFF' ? 'success' : 'danger'}
                  onClick={() => startStopVM(vm.id, vm.status)}
                >
                  {vm.status === 'SHUTOFF' ? 'Start' : 'Stop'}
                </CButton>
                <CDropdownToggle color="secondary" split />
                <CDropdownMenu>
                  <CDropdownItem onClick={() => startStopVM(vm.id, 'REBOOT')}>Reboot</CDropdownItem>
                  <CDropdownItem href="#">Console Log</CDropdownItem>
                  <CDropdownItem
                    onClick={() => {
                      ctx.setDeleteServerId(vm.id)
                      ctx.setModalVisible(true)
                    }}
                  >
                    Delete
                  </CDropdownItem>
                </CDropdownMenu>
              </CDropdown>
              &nbsp;
              <CButton
                href={'#/console/' + vm.id}
                disabled={vm.status === 'ACTIVE' ? false : true}
                color="success"
              >
                Connect
              </CButton>
            </CTableDataCell>
          </CTableRow>
        ))}
      </CTableBody>
    </CTable>
  )
}

export default ServerTable
