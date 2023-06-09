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
} from '@coreui/react'
import axios from 'axios'

const ServerTable = () => {
  const [vms, setVMs] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          'https://cyberrangeapi.jakecrowley.com/v1/compute/list_vms',
          { withCredentials: true },
        )
        const data = response.data
        setVMs(data.vms) // Update the state with the retrieved data
      } catch (error) {
        console.error('Error fetching VM data:', error)
      }
    }

    fetchData()
  }, []) // Empty dependency array to run the effect only once on component mount

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
            <CTableHeaderCell>{vm.name}</CTableHeaderCell>
            <CTableHeaderCell>{vm.ip !== '' ? vm.ip : 'No IP'}</CTableHeaderCell>
            <CTableHeaderCell>{vm.vcpus}</CTableHeaderCell>
            <CTableHeaderCell>{vm.memory}</CTableHeaderCell>
            <CTableHeaderCell>{vm.disk} GB</CTableHeaderCell>
            <CTableHeaderCell>{vm.status}</CTableHeaderCell>
            <CTableHeaderCell>
              <CDropdown variant="btn-group" key={vm.id}>
                <CButton color={vm.status === 'SHUTOFF' ? 'success' : 'danger'}>
                  {vm.status === 'SHUTOFF' ? 'Start' : 'Stop'}
                </CButton>
                <CDropdownToggle color="secondary" split />
                <CDropdownMenu>
                  <CDropdownItem href="#">Things</CDropdownItem>
                </CDropdownMenu>
              </CDropdown>
            </CTableHeaderCell>
          </CTableRow>
        ))}
      </CTableBody>
    </CTable>
  )
}

export default ServerTable
