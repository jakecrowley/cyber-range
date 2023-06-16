import { configureStore } from '@reduxjs/toolkit'
import websocketReducer from './websocketSlice'

const initialState = {
  sidebarShow: true,
}

const changeState = (state = initialState, { type, ...rest }) => {
  switch (type) {
    case 'set':
      return { ...state, ...rest }
    default:
      return state
  }
}

const store = configureStore({
  reducer: {
    ws: websocketReducer,
  },
})
export default store
