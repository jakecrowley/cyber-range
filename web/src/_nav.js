import React from 'react'
import CIcon from '@coreui/icons-react'
import { cilCloud, cilSpeedometer, cilLaptop, cilDescription } from '@coreui/icons'
import { CNavGroup, CNavItem, CNavTitle } from '@coreui/react'
import ConsoleNavList from './components/ConsoleNavList'

const _nav = [
  {
    component: CNavTitle,
    name: 'Compute',
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
    to: '/networks',
    icon: <CIcon icon={cilCloud} customClassName="nav-icon" />,
  },
  {
    component: CNavGroup,
    name: 'Console',
    to: '/console',
    icon: <CIcon icon={cilLaptop} customClassName="nav-icon" />,
    items: [
      {
        component: ConsoleNavList,
      },
    ],
  },
  {
    component: CNavTitle,
    name: 'Student',
  },
  {
    component: CNavItem,
    name: 'Labs',
    to: '/labs',
    icon: <CIcon icon={cilDescription} customClassName="nav-icon" />,
  },
]

export default _nav
