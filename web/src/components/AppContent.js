import React, { Suspense, useEffect } from 'react'
import { Navigate, Route, Routes } from 'react-router-dom'
import { CContainer, CSpinner } from '@coreui/react'

// routes config
import routes from '../routes'
import { useDispatch } from 'react-redux'
import { setSocket } from '../websocketSlice'
import API_URLS from './AppAPI'
import { io } from 'socket.io-client'
import Cookies from 'js-cookie'

const AppContent = () => {
  const dispatch = useDispatch()

  useEffect(() => {
    const token = Cookies.get('token')

    const socket = io(API_URLS['SOCKETIO'], {
      autoConnect: true,
      extraHeaders: { token: token },
    })
    socket.on('connect', () => {
      console.log('Connected to websocket')
      dispatch(setSocket(socket))
    })
  }, [dispatch])

  /*
  useEffect(() => {
    if (!socket) return

    socket.onclose = () => {
      console.error('Socket disconnected unexpectedly')

      setTimeout(() => {
        const ws = new WebSocket(API_URLS['WEBSOCKET'])
        dispatch(setSocket(ws))
      }, 1000)
    }
  }, [socket, dispatch])
  */

  return (
    <CContainer lg>
      <Suspense fallback={<CSpinner color="primary" />}>
        <Routes>
          {routes.map((route, idx) => {
            return (
              route.element && (
                <Route
                  key={idx}
                  path={route.path}
                  exact={route.exact}
                  name={route.name}
                  element={<route.element />}
                />
              )
            )
          })}
          <Route path="/" element={<Navigate to="servers" replace />} />
        </Routes>
      </Suspense>
    </CContainer>
  )
}

export default React.memo(AppContent)
