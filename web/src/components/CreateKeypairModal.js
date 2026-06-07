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

const CreateKeypairModal = ({ visible, setVisible }) => {
  const [loading, setLoading] = useState(false)
  const [privateKey, setPrivateKey] = useState(null)
  const [error, setError] = useState(null)
  const [keypairName, setKeypairName] = useState('')

  const handleCreate = async () => {
    if (!keypairName.trim()) {
      setError('Please enter a keypair name')
      return
    }

    setLoading(true)
    setError(null)

    try {
      const response = await axios.post(
        API_URLS['CREATE_KEYPAIR'],
        { name: keypairName },
        { withCredentials: true },
      )

      if (response.status === 200 && response.data.err === false) {
        setPrivateKey(response.data.private_key)
      } else {
        setError(response.data.msg || 'Failed to create keypair')
      }
    } catch (err) {
      console.error('Error creating keypair:', err)
      setError('Failed to create keypair')
    } finally {
      setLoading(false)
    }
  }

  const handleClose = () => {
    setVisible(false)
    setPrivateKey(null)
    setError(null)
    setKeypairName('')
  }

  const downloadPrivateKey = () => {
    const element = document.createElement('a')
    const file = new Blob([privateKey], { type: 'text/plain' })
    element.href = URL.createObjectURL(file)
    element.download = `${keypairName}.pem`
    document.body.appendChild(element)
    element.click()
    document.body.removeChild(element)
  }

  return (
    <CModal visible={visible} onClose={handleClose}>
      <CModalHeader onClose={handleClose}>
        <CModalTitle>{privateKey ? 'Keypair Created' : 'Create SSH Keypair'}</CModalTitle>
      </CModalHeader>

      <CModalBody>
        {privateKey ? (
          <>
            <CAlert color="warning">
              <strong>Important:</strong> This is the only time you will see the private key. Please
              save it securely.
            </CAlert>
            <CForm>
              <CRow className="mb-3">
                <CFormLabel className="col-sm-3 col-form-label">Keypair Name:</CFormLabel>
                <CCol sm={9}>
                  <CFormInput type="text" value={keypairName} disabled />
                </CCol>
              </CRow>
              <CRow className="mb-3">
                <CFormLabel className="col-sm-3 col-form-label">Private Key:</CFormLabel>
                <CCol sm={9}>
                  <CFormInput
                    component="textarea"
                    rows={10}
                    value={privateKey}
                    readOnly
                    style={{ fontFamily: 'monospace', fontSize: '0.8rem' }}
                  />
                </CCol>
              </CRow>
            </CForm>
          </>
        ) : (
          <CForm>
            {error && <CAlert color="danger">{error}</CAlert>}
            <CRow className="mb-3">
              <CFormLabel htmlFor="keypairName" className="col-sm-3 col-form-label">
                Name:
              </CFormLabel>
              <CCol sm={9}>
                <CFormInput
                  type="text"
                  id="keypairName"
                  placeholder="my-keypair"
                  value={keypairName}
                  onChange={(e) => setKeypairName(e.target.value)}
                />
              </CCol>
            </CRow>
          </CForm>
        )}
      </CModalBody>

      <CModalFooter>
        {privateKey ? (
          <>
            <CButton color="secondary" onClick={handleClose}>
              Close
            </CButton>
            <CButton color="primary" onClick={downloadPrivateKey}>
              Download .pem
            </CButton>
          </>
        ) : (
          <>
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
          </>
        )}
      </CModalFooter>
    </CModal>
  )
}

CreateKeypairModal.propTypes = {
  visible: PropTypes.bool.isRequired,
  setVisible: PropTypes.func.isRequired,
}

export default CreateKeypairModal
