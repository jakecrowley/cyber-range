import { React, useEffect, useRef, useState } from 'react'
import axios from 'axios'
import {
  CButton,
  CCol,
  CForm,
  CFormInput,
  CFormLabel,
  CFormSelect,
  CInputGroup,
  CInputGroupText,
  CModal,
  CModalBody,
  CModalFooter,
  CModalHeader,
  CModalTitle,
  CRow,
  CSpinner,
} from '@coreui/react'
import { API_URLS } from 'src/components'

const CreateServerModal = (ctx) => {
  const [images, setImages] = useState([])
  const [subnets, setSubnets] = useState([])
  const [loading, setLoading] = useState(false)
  const form = useRef(null)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const imgResp = await axios.get(API_URLS['LIST_IMAGES'], { withCredentials: true })
        if (imgResp.status === 200 && imgResp.data.err === false) {
          setImages(imgResp.data.images)
        }

        const subnetResp = await axios.get(API_URLS['LIST_SUBNETS'], { withCredentials: true })
        if (subnetResp.status === 200 && subnetResp.data.err === false) {
          setSubnets(subnetResp.data.subnets)
        }
      } catch (error) {
        console.error('Error fetching VM data:', error)
        window.location = '/#/login'
      }
    }

    fetchData()
  }, [])

  const onSelectOS = (e) => {
    const selectedImage = images.find((image) => image.id === e.target.value)
    if (selectedImage.recommended_specs !== undefined) {
      e.target.form[3].value = selectedImage.recommended_specs.vcpus
      e.target.form[4].value = selectedImage.recommended_specs.disk
      e.target.form[5].value = selectedImage.recommended_specs.memory
    }
  }

  const onFormSubmit = () => {
    const name = form.current.elements['inputName'].value
    const os = form.current.elements['inputOS'].value
    const vcpus = form.current.elements['inputvCPUs'].value
    const disk = form.current.elements['inputDisk'].value
    const memory = form.current.elements['inputMemory'].value
    const subnet = form.current.elements['inputSubnet'].value

    try {
      axios
        .post(
          API_URLS['CREATE_VM'],
          {
            vm_name: name,
            vcpus: vcpus,
            memory: memory,
            disk: disk,
            image_id: os,
            network_id: subnet,
          },
          { withCredentials: true },
        )
        .then((response) => {
          if (response.status === 200 && response.data.err === false) {
            ctx.setModalVisible(false)
          }
        })
    } catch (error) {
      console.error('Error creating VM:', error)
    }
  }

  return (
    <>
      <CModal size="lg" visible={ctx.modalVisible} onClose={() => ctx.setModalVisible(false)}>
        <CModalHeader onClose={() => ctx.setModalVisible(false)}>
          <CModalTitle>Create Virtual Machine</CModalTitle>
        </CModalHeader>

        <CModalBody>
          <CForm ref={form}>
            <CRow className="mb-3">
              <CFormLabel htmlFor="inputName" className="col-sm-1 col-form-label">
                Name:
              </CFormLabel>
              <CCol sm={10}>
                <CFormInput type="input" id="inputName" />
              </CCol>
            </CRow>
            <CRow className="mb-3">
              <CFormLabel htmlFor="inputOS" className="col-sm-1 col-form-label">
                OS:
              </CFormLabel>
              <CCol sm={10}>
                <CFormSelect id="inputOS" aria-label="Select an OS" onInput={onSelectOS}>
                  <option>Select an Operating System</option>
                  {images.map((image, i) => (
                    <option key={i} value={image.id}>
                      {image.name}
                    </option>
                  ))}
                </CFormSelect>
              </CCol>
            </CRow>
            <CRow className="mb-3">
              <CFormLabel htmlFor="inputSubnet" className="col-sm-1 col-form-label">
                Subnet:
              </CFormLabel>
              <CCol sm={10}>
                <CFormSelect id="inputSubnet" aria-label="Select a Subnet">
                  <option>Select a Subnet</option>
                  {subnets.map((subnet, i) => (
                    <option key={i} value={subnet.id}>
                      {subnet.name}
                    </option>
                  ))}
                </CFormSelect>
              </CCol>
            </CRow>
            <CRow className="mb-3">
              <CFormLabel htmlFor="inputvCPUs" className="col-sm-1 col-form-label">
                vCPUs:
              </CFormLabel>
              <CCol sm={2}>
                <CFormInput type="input" id="inputvCPUs" />
              </CCol>
              <CFormLabel htmlFor="inputDisk" className="col-sm-1 col-form-label">
                Disk:
              </CFormLabel>
              <CCol sm={2}>
                <CInputGroup>
                  <CFormInput type="input" id="inputDisk" />
                  <CInputGroupText>GB</CInputGroupText>
                </CInputGroup>
              </CCol>
              <CFormLabel htmlFor="inputMemory" className="col-sm-1 col-form-label">
                RAM:
              </CFormLabel>
              <CCol sm={3}>
                <CInputGroup>
                  <CFormInput type="input" id="inputMemory" />
                  <CInputGroupText>MB</CInputGroupText>
                </CInputGroup>
              </CCol>
            </CRow>
          </CForm>
        </CModalBody>

        <CModalFooter>
          <CButton
            color="success"
            disabled={loading}
            onClick={() => {
              setLoading(true)
              onFormSubmit()
            }}
          >
            <CSpinner
              color="primary"
              size="sm"
              style={!loading ? { display: 'none' } : { marginRight: '5px' }}
            />
            Create
          </CButton>
        </CModalFooter>
      </CModal>
    </>
  )
}

export default CreateServerModal
