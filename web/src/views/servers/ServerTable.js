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

const ServerTable = () => {
  const [vms, setVMs] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(API_URLS['LIST_VMS'], { withCredentials: true })
        const data = response.data
        setVMs(data.vms) // Update the state with the retrieved data
      } catch (error) {
        console.error('Error fetching VM data:', error)
        window.location = '/#/login'
      }
    }

    fetchData()
  }, []) // Empty dependency array to run the effect only once on component mount

  const startStopVM = async (vm_id, status) => {
    var action_url = ''
    if (status === 'SHUTOFF') action_url = API_URLS['START_VM']
    else action_url = API_URLS['STOP_VM']

    try {
      const response = await axios.get(action_url + '?vm_id=' + vm_id, { withCredentials: true })
      console.log(response.data)
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
                  color={vm.status === 'SHUTOFF' ? 'success' : 'danger'}
                  onClick={() => startStopVM(vm.id, vm.status)}
                >
                  {vm.status === 'SHUTOFF' ? 'Start' : 'Stop'}
                </CButton>
                <CDropdownToggle color="secondary" split />
                <CDropdownMenu>
                  <CDropdownItem href="#">Reboot</CDropdownItem>
                  <CDropdownItem href="#">Console Log</CDropdownItem>
                </CDropdownMenu>
              </CDropdown>
            </CTableDataCell>
          </CTableRow>
        ))}
      </CTableBody>
    </CTable>
  )
}

export default ServerTable
