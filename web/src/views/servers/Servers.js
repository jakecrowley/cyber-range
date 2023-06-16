import { React, useState } from 'react'
import { API_URLS } from 'src/components'
import axios from 'axios'

import ServerTable from './ServerTable'
import {
  CButton,
  CCard,
  CCardBody,
  CCardHeader,
  CModal,
  CModalHeader,
  CModalTitle,
  CModalBody,
  CModalFooter,
  CSpinner,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilPlus } from '@coreui/icons'
import CreateServerModal from './CreateServerModal'

const Servers = () => {
  const [deleteServerId, setDeleteServerId] = useState('')
  const [modalVisible, setModalVisible] = useState(false)
  const [csModalVisible, setCSModalVisible] = useState(false)
  const [loading, setLoading] = useState(true)

  const delete_vm = async (vm_id) => {
    try {
      const response = await axios.get(API_URLS['DELETE_VM'] + '?vm_id=' + vm_id, {
        withCredentials: true,
      })
      if (response.status === 401) window.location = '/#/login'
    } catch (error) {
      console.error('Error fetching VM data:', error)
    }
  }

  return (
    <>
      <CreateServerModal modalVisible={csModalVisible} setModalVisible={setCSModalVisible} />
      <CModal visible={modalVisible} onClose={() => setModalVisible(false)}>
        <CModalHeader onClose={() => setModalVisible(false)}>
          <CModalTitle>Permanently Delete Server</CModalTitle>
        </CModalHeader>

        <CModalBody>
          WARNING! If you proceed, the virtual machine along with all of its data will be
          permanently deleted.
        </CModalBody>

        <CModalFooter>
          <CButton color="secondary" onClick={() => setModalVisible(false)}>
            Close
          </CButton>

          <CButton
            color="danger"
            onClick={() => {
              delete_vm(deleteServerId)
              setModalVisible(false)
            }}
          >
            DELETE
          </CButton>
        </CModalFooter>
      </CModal>
      <CCard className="mb-4">
        <CCardHeader style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{ flexGrow: 1 }}>Virtual Machines</div>
          <CButton
            color="success"
            onClick={() => {
              setCSModalVisible(true)
            }}
          >
            <CIcon icon={cilPlus} />
            &nbsp; Create VM
          </CButton>
        </CCardHeader>
        <CCardBody>
          <ServerTable
            modalVisible={modalVisible}
            setModalVisible={setModalVisible}
            setDeleteServerId={setDeleteServerId}
            setLoading={setLoading}
          />
          <div
            style={loading ? {} : { visibility: 'hidden' }}
            className="d-flex justify-content-center align-items-center"
          >
            Loading VMs... &nbsp;
            <CSpinner color="primary" />
          </div>
        </CCardBody>
      </CCard>
    </>
  )
}

export default Servers
