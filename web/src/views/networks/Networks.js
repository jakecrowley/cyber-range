import React, { useState } from 'react'

import NetworkTable from './NetworkTable'
import { CButton, CCard, CCardBody, CCardHeader, CSpinner } from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilPlus } from '@coreui/icons'

const Networks = () => {
  const [loading, setLoading] = useState(true)

  return (
    <>
      <CCard className="mb-4">
        <CCardHeader style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{ flexGrow: 1 }}>Networks</div>
          <CButton color="success">
            <CIcon icon={cilPlus} />
            &nbsp; Create Network
          </CButton>
        </CCardHeader>
        <CCardBody>
          <NetworkTable setLoading={setLoading} />
          <div
            style={loading ? {} : { visibility: 'hidden' }}
            className="d-flex justify-content-center align-items-center"
          >
            Loading Networks... &nbsp;
            <CSpinner color="primary" />
          </div>
        </CCardBody>
      </CCard>
    </>
  )
}

export default Networks
