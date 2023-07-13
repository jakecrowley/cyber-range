import React, { useEffect, useRef, useState } from 'react'
import { useSelector } from 'react-redux'
import axios from 'axios'
import {
  CTable,
  CTableHead,
  CTableHeaderCell,
  CTableRow,
  CTableBody,
  CTableDataCell,
  CDropdown,
  CDropdownMenu,
  CDropdownItem,
  CDropdownToggle,
  CButton,
} from '@coreui/react'
import { API_URLS } from 'src/components'

const NetworkTable = (ctx) => {
  const [runOnce, setRunOnce] = useState(false)
  const [networks, setNetworks] = useState([])
  const socket = useSelector((state) => state.ws.socket)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(API_URLS['LIST_SUBNETS'], { withCredentials: true })
        const data = response.data
        ctx.setLoading(false)
        setNetworks(data.subnets) // Update the state with the retrieved data
      } catch (error) {
        console.error('Error fetching network data:', error)
        window.location = '/#/login'
      }
    }

    if (!runOnce) {
      setRunOnce(true)
      fetchData()
    }
  }, [ctx, runOnce, socket]) // Empty dependency array to run the effect only once on component mount

  return (
    <CTable>
      <CTableHead>
        <CTableRow>
          <CTableHeaderCell scope="col">Name</CTableHeaderCell>
          <CTableHeaderCell scope="col">Subnet</CTableHeaderCell>
          <CTableHeaderCell scope="col">Gateway IP</CTableHeaderCell>
          <CTableHeaderCell scope="col">Actions</CTableHeaderCell>
        </CTableRow>
      </CTableHead>
      <CTableBody>
        {networks.map((network) => (
          <CTableRow key={network.id}>
            <CTableDataCell>{network.name}</CTableDataCell>
            <CTableDataCell>{network.cidr}</CTableDataCell>
            <CTableDataCell>{network.gateway_ip}</CTableDataCell>
            <CTableDataCell>
              <CDropdown variant="btn-group" key={network.id}>
                <CButton>Edit Subnet</CButton>
                <CDropdownToggle color="secondary" split />
                <CDropdownMenu>
                  <CDropdownItem href="#">Delete</CDropdownItem>
                </CDropdownMenu>
              </CDropdown>
            </CTableDataCell>
          </CTableRow>
        ))}
      </CTableBody>
    </CTable>
  )
}

export default NetworkTable
