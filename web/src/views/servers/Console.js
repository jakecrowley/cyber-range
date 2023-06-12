import { CButton, CCard, CCardBody, CCardHeader } from '@coreui/react'
import { React, useEffect, useRef, useState } from 'react'
import axios from 'axios'
import { API_URLS } from 'src/components'

const ConsolePage = () => {
  const [consoleUrl, setConsoleUrl] = useState([])
  const vmConsole = useRef(null)

  useEffect(() => {
    const fetchData = async () => {
      var server_id = window.location.href.split('/').pop()
      try {
        const response = await axios.get(API_URLS['GET_CONSOLE_URL'] + '?server_id=' + server_id, {
          withCredentials: true,
        })
        const data = response.data
        setConsoleUrl(data.url) // Update the state with the retrieved data
      } catch (error) {
        console.error('Error fetching VM data:', error)
        if (error.response.status === 401) {
          window.location = '/#/login'
        }
      }
    }

    fetchData()
  }, []) // Empty dependency array to run the effect only once on component mount

  return (
    <CCard className="mb-4" style={{ height: '90vh' }}>
      <CCardHeader style={{ display: 'flex', alignItems: 'center' }}>
        <div style={{ flexGrow: 1 }}>Server Console</div>
        <CButton color="success">Restart</CButton>
      </CCardHeader>
      <CCardBody style={{ height: 'calc(90% - 2.5rem)' }}>
        <iframe
          title="console"
          src={consoleUrl}
          ref={vmConsole}
          style={{ height: '100%', width: '100%', border: 'none', overflow: 'hidden' }}
        ></iframe>
      </CCardBody>
    </CCard>
  )
}

export default ConsolePage
