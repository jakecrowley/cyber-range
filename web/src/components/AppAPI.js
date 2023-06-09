const BASE_API_URL = 'https://cyberrangeapi.jakecrowley.com/v1'
const BASE_SIO_URL = 'https://cyberrangeapi.jakecrowley.com/'

const API_URLS = {
  LOGIN: BASE_API_URL + '/auth/login',
  LIST_VMS: BASE_API_URL + '/compute/list_vms',
  START_VM: BASE_API_URL + '/compute/start_vm',
  STOP_VM: BASE_API_URL + '/compute/stop_vm',
  REBOOT_VM: BASE_API_URL + '/compute/reboot_vm',
  CREATE_VM: BASE_API_URL + '/compute/create_vm',
  DELETE_VM: BASE_API_URL + '/compute/delete_vm',
  LIST_IMAGES: BASE_API_URL + '/compute/list_images',
  LIST_KEYPAIRS: BASE_API_URL + '/compute/list_keypairs',
  GET_CONSOLE_URL: BASE_API_URL + '/compute/get_console_url',
  LIST_SUBNETS: BASE_API_URL + '/networking/get_subnets',
  SOCKETIO: BASE_SIO_URL,
}

export default API_URLS
