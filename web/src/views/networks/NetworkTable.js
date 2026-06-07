import React, { useEffect, useState } from 'react'
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
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
  CModalFooter,
} from '@coreui/react'
import { API_URLS } from 'src/components'

const NetworkTable = (ctx) => {
  const [networks, setNetworks] = useState([])
  const [deleteNetworkId, setDeleteNetworkId] = useState('')
  const [deleteModalVisible, setDeleteModalVisible] = useState(false)
  const [errorModalVisible, setErrorModalVisible] = useState(false)
  const [errorMsg, setErrorMsg] = useState('')
  const socket = useSelector((state) => state.ws.socket)

  const fetchData = async () => {
    try {
      const response = await axios.get(API_URLS['LIST_SUBNETS'], { withCredentials: true })
      const data = response.data
      ctx.setLoading(false)
      setNetworks(data.subnets)
    } catch (error) {
      console.error('Error fetching network data:', error)
      window.location = '/#/login'
    }
  }

  useEffect(() => {
    fetchData()
  }, [ctx.refreshKey, socket])

  const delete_network = async (network_id) => {
    try {
      const response = await axios.get(API_URLS['DELETE_NETWORK'] + '?network_id=' + network_id, {
        withCredentials: true,
      })
      if (response.status === 401) {
        window.location = '/#/login'
        return
      }
      if (response.data.err === true) {
        setErrorMsg(response.data.msg || 'Failed to delete network')
        setErrorModalVisible(true)
      } else {
        fetchData()
      }
    } catch (error) {
      console.error('Error deleting network:', error)
      setErrorMsg('Failed to delete network')
      setErrorModalVisible(true)
    }
  }

  return (
    <>
      <CModal visible={deleteModalVisible} onClose={() => setDeleteModalVisible(false)}>
        <CModalHeader onClose={() => setDeleteModalVisible(false)}>
          <CModalTitle>Permanently Delete Network</CModalTitle>
        </CModalHeader>
        <CModalBody>
          WARNING! If you proceed, the network along with all of its data will be permanently
          deleted.
        </CModalBody>
        <CModalFooter>
          <CButton color="secondary" onClick={() => setDeleteModalVisible(false)}>
            Close
          </CButton>
          <CButton
            color="danger"
            onClick={() => {
              delete_network(deleteNetworkId)
              setDeleteModalVisible(false)
            }}
          >
            DELETE
          </CButton>
        </CModalFooter>
      </CModal>
      <CModal visible={errorModalVisible} onClose={() => setErrorModalVisible(false)}>
        <CModalHeader onClose={() => setErrorModalVisible(false)}>
          <CModalTitle>Error</CModalTitle>
        </CModalHeader>
        <CModalBody>{errorMsg}</CModalBody>
        <CModalFooter>
          <CButton color="secondary" onClick={() => setErrorModalVisible(false)}>
            Close
          </CButton>
        </CModalFooter>
      </CModal>
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
                    <CDropdownItem
                      onClick={() => {
                        setDeleteNetworkId(network.network_id)
                        setDeleteModalVisible(true)
                      }}
                    >
                      Delete
                    </CDropdownItem>
                  </CDropdownMenu>
                </CDropdown>
              </CTableDataCell>
            </CTableRow>
          ))}
        </CTableBody>
      </CTable>
    </>
  )
}

export default NetworkTable
