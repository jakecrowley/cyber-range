import { createSlice } from '@reduxjs/toolkit'

const websocketSlice = createSlice({
  name: 'ws',
  initialState: {
    socket: null,
  },
  reducers: {
    setSocket: (state, action) => {
      state.socket = action.payload
    },
  },
})

export const { setSocket } = websocketSlice.actions

export default websocketSlice.reducer
