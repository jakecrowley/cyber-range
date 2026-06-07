import { React, useState } from 'react'
import PropTypes from 'prop-types'
import axios from 'axios'
import {
  CButton,
  CForm,
  CFormInput,
  CFormLabel,
  CModal,
  CModalBody,
  CModalFooter,
  CModalHeader,
  CModalTitle,
  CRow,
  CCol,
  CAlert,
  CSpinner,
} from '@coreui/react'
import { API_URLS } from 'src/components'

const CreateNetworkModal = ({ visible, setVisible, onNetworkCreated }) => {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [networkName, setNetworkName] = useState('')
  const [networkCidr, setNetworkCidr] = useState('')

  const handleCreate = async () => {
    if (!networkName.trim()) {
      setError('Please enter a network name')
      return
    }
    if (!networkCidr.trim()) {
      setError('Please enter a CIDR (e.g. 192.168.1.0/24)')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await axios.post(
        API_URLS['CREATE_NETWORK'],
        { name: networkName, cidr: networkCidr },
        { withCredentials: true },
      )

      if (response.status === 200 && response.data.err === false) {
        setVisible(false)
        setNetworkName('')
        setNetworkCidr('')
        if (onNetworkCreated) onNetworkCreated()
      } else {
        setError(response.data.msg || 'Failed to create network')
      }
    } catch (err) {
      console.error('Error creating network:', err)
      setError('Failed to create network')
    } finally {
      setLoading(false)
    }
  }

  const handleClose = () => {
    setVisible(false)
    setError(null)
    setNetworkName('')
    setNetworkCidr('')
  }

  return (
    <CModal visible={visible} onClose={handleClose}>
      <CModalHeader onClose={handleClose}>
        <CModalTitle>Create Network</CModalTitle>
      </CModalHeader>

      <CModalBody>
        <CForm>
          {error && <CAlert color="danger">{error}</CAlert>}
          <CRow className="mb-3">
            <CFormLabel htmlFor="networkName" className="col-sm-3 col-form-label">
              Name:
            </CFormLabel>
            <CCol sm={9}>
              <CFormInput
                type="text"
                id="networkName"
                placeholder="my-network"
                value={networkName}
                onChange={(e) => setNetworkName(e.target.value)}
              />
            </CCol>
          </CRow>
          <CRow className="mb-3">
            <CFormLabel htmlFor="networkCidr" className="col-sm-3 col-form-label">
              CIDR:
            </CFormLabel>
            <CCol sm={9}>
              <CFormInput
                type="text"
                id="networkCidr"
                placeholder="192.168.1.0/24"
                value={networkCidr}
                onChange={(e) => setNetworkCidr(e.target.value)}
              />
            </CCol>
          </CRow>
        </CForm>
      </CModalBody>

      <CModalFooter>
        <CButton color="secondary" onClick={handleClose}>
          Cancel
        </CButton>
        <CButton color="success" disabled={loading} onClick={handleCreate}>
          <CSpinner
            color="primary"
            size="sm"
            style={!loading ? { display: 'none' } : { marginRight: '5px' }}
          />
          Create
        </CButton>
      </CModalFooter>
    </CModal>
  )
}

CreateNetworkModal.propTypes = {
  visible: PropTypes.bool.isRequired,
  setVisible: PropTypes.func.isRequired,
  onNetworkCreated: PropTypes.func,
}

export default CreateNetworkModal
