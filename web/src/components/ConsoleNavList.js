import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { CNavItem } from '@coreui/react'

const ConsoleNavList = () => {
  const [vms, setVMs] = useState([])

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get(
          'https://cyberrangeapi.jakecrowley.com/v1/compute/list_vms',
          { withCredentials: true },
        )
        const data = response.data
        setVMs(data.vms) // Update the state with the retrieved data
      } catch (error) {
        console.error('Error fetching VM data:', error)
        if (error.response.status === 401) {
          window.location = '/#/login'
        }
      }
    }

    fetchData()
  }, []) // Empty dependency array to run the effect only once on component mount

  return vms.map((vm) => (
    <CNavItem key={vm.id} href={`/#/console/${vm.id}`}>
      {vm.name}
    </CNavItem>
  ))
}

export default ConsoleNavList