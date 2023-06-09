import React from 'react'
import CIcon from '@coreui/icons-react'
import { cilCloud, cilSpeedometer } from '@coreui/icons'
import { CNavItem, CNavTitle } from '@coreui/react'

const _nav = [
  {
    component: CNavTitle,
    name: '',
  },
  {
    component: CNavItem,
    name: 'Virtual Machines',
    to: '/servers',
    icon: <CIcon icon={cilSpeedometer} customClassName="nav-icon" />,
  },
  {
    component: CNavItem,
    name: 'Networks',
    to: '/servers',
    icon: <CIcon icon={cilCloud} customClassName="nav-icon" />,
  },
]

export default _nav
