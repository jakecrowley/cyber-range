import React from 'react'

import ServerTable from './ServerTable'
import { CButton, CCard, CCardBody, CCardHeader, CPlaceholder } from '@coreui/react'
import CIcon from '@coreui/icons-react'
import { cilPlus } from '@coreui/icons'

const Servers = () => {
  return (
    <>
      <CCard className="mb-4">
        <CCardHeader style={{ display: 'flex', alignItems: 'center' }}>
          <div style={{ flexGrow: 1 }}>Virtual Machines</div>
          <CButton color="success">
            <CIcon icon={cilPlus} />
            &nbsp; Create VM
          </CButton>
        </CCardHeader>
        <CCardBody>
          <CPlaceholder component={ServerTable} animation="glow" xs={7} />
        </CCardBody>
      </CCard>
    </>
  )
}

export default Servers
