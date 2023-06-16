import React from 'react'
import {
  CDropdown,
  CDropdownDivider,
  CDropdownHeader,
  CDropdownItem,
  CDropdownMenu,
  CDropdownToggle,
} from '@coreui/react'
import { cilLockLocked, cilSettings, cilUser, cilMenu } from '@coreui/icons'
import CIcon from '@coreui/icons-react'
import Cookies from 'js-cookie'
import jwt_decode from 'jwt-decode'

const AppHeaderDropdown = () => {
  function getDisplayName() {
    var token = Cookies.get('token')
    if (token === undefined) {
      window.location = '/#/login'
      return ''
    }

    return jwt_decode(token).display_name
  }

  function logout() {
    document.cookie = `token=x;domain=.jakecrowley.com;path=/;expires=Thu, 01 Jan 1970 00:00:01 GMT`
    window.location = '/#/login'
  }

  return (
    <CDropdown variant="nav-item">
      <CDropdownToggle placement="bottom-end" className="py-0" caret={false}>
        <CIcon icon={cilMenu} style={{ flexGrow: 1 }} />
        &nbsp;
        {getDisplayName()}
      </CDropdownToggle>
      <CDropdownMenu className="pt-0" placement="bottom-end">
        <CDropdownHeader className="bg-light fw-semibold py-2">Settings</CDropdownHeader>
        <CDropdownItem href="#">
          <CIcon icon={cilUser} className="me-2" />
          Profile
        </CDropdownItem>
        <CDropdownItem href="#">
          <CIcon icon={cilSettings} className="me-2" />
          Settings
        </CDropdownItem>
        <CDropdownDivider />
        <CDropdownItem onClick={logout}>
          <CIcon icon={cilLockLocked} className="me-2" />
          Logout
        </CDropdownItem>
      </CDropdownMenu>
    </CDropdown>
  )
}

export default AppHeaderDropdown
