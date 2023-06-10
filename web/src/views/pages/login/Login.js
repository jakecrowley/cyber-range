import React, { useRef } from 'react'
import axios from 'axios'
import {
  CButton,
  CCard,
  CCardBody,
  CCardGroup,
  CCol,
  CContainer,
  CForm,
  CFormInput,
  CInputGroup,
  CInputGroupText,
  CRow,
} from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilLockLocked, cilUser } from '@coreui/icons'

const Login = () => {
  const usernameRef = useRef()
  const passwordRef = useRef()

  function login() {
    if (usernameRef.current !== undefined && passwordRef.current !== undefined) {
      let username = usernameRef.current.value
      let password = passwordRef.current.value

      axios
        .post('https://cyberrangeapi.jakecrowley.com/v1/auth/login', { username, password })
        .then((response) => {
          if (response.data.err === true) {
            console.log(response.data.msg)
            return
          } else {
            const token = response.data.token

            // Set the token as a cookie in the browser
            // This cookie will be automatically attached to all subsequent requests for *.jakecrowley.com
            document.cookie = `token=${token};domain=.jakecrowley.com;path=/;`

            // Perform any further actions after successful login
            // For example, redirect to another page or update the application state
            // Redirect to the home page
            window.location.href = '/#/servers'
          }
        })
        .catch((error) => {
          // Handle login errors
          console.error('Login failed:', error)
        })
    }
  }

  function onKeyPress(e) {
    if (e.key === 'Enter') login()
  }

  return (
    <div className="bg-light min-vh-100 d-flex flex-row align-items-center">
      <CContainer>
        <CRow className="justify-content-center">
          <CCol md={5}>
            <CCardGroup>
              <CCard className="p-4">
                <CCardBody>
                  <CForm>
                    <h1>Login</h1>
                    <p className="text-medium-emphasis">Sign In to your account</p>
                    <CInputGroup className="mb-3">
                      <CInputGroupText>
                        <CIcon icon={cilUser} />
                      </CInputGroupText>
                      <CFormInput
                        placeholder="Username"
                        autoComplete="username"
                        ref={usernameRef}
                      />
                    </CInputGroup>
                    <CInputGroup className="mb-4">
                      <CInputGroupText>
                        <CIcon icon={cilLockLocked} />
                      </CInputGroupText>
                      <CFormInput
                        type="password"
                        placeholder="Password"
                        autoComplete="current-password"
                        ref={passwordRef}
                        onKeyDown={onKeyPress}
                      />
                    </CInputGroup>
                    <CRow>
                      <CCol xs={6}>
                        <CButton color="primary" className="px-4" onClick={login}>
                          Login
                        </CButton>
                      </CCol>
                      <CCol xs={6} className="text-right">
                        <CButton color="link" className="px-0">
                          Forgot password?
                        </CButton>
                      </CCol>
                    </CRow>
                  </CForm>
                </CCardBody>
              </CCard>
            </CCardGroup>
          </CCol>
        </CRow>
      </CContainer>
    </div>
  )
}

export default Login
