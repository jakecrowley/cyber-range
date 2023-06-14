import { React, useState } from 'react'

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
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilPlus } from '@coreui/icons'

const Servers = () => {
  const [deleteServerId, setDeleteServerId] = useState('')
  const [modalVisible, setModalVisible] = useState(false)

  return (
    <>
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
              console.log(deleteServerId)
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
          <CButton color="success">
            <CIcon icon={cilPlus} />
            &nbsp; Create VM
          </CButton>
        </CCardHeader>
        <CCardBody>
          <ServerTable
            modalVisible={modalVisible}
            setModalVisible={setModalVisible}
            setDeleteServerId={setDeleteServerId}
          />
        </CCardBody>
      </CCard>
    </>
  )
}

export default Servers
