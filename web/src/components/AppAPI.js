const BASE_API_URL = 'https://cyberrangeapi.jakecrowley.com/v1'

const API_URLS = {
  LOGIN: BASE_API_URL + '/auth/login',
  LIST_VMS: BASE_API_URL + '/compute/list_vms',
  START_VM: BASE_API_URL + '/compute/start_vm',
  STOP_VM: BASE_API_URL + '/compute/stop_vm',
  REBOOT_VM: BASE_API_URL + '/compute/reboot_vm',
  CREATE_VM: BASE_API_URL + '/compute/create_vm',
  GET_CONSOLE_URL: BASE_API_URL + '/compute/get_console_url',
  WEBSOCKET: BASE_API_URL.replace('https', 'wss') + '/ws',
}

export default API_URLS
