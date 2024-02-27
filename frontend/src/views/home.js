import React from 'react'
import Image from 'react-bootstrap/Image'

import background from '../assets/img/background.png'

const Home = () => {
  return (
    <Image
    style={{ opacity: 1, position: 'fixed', top: 0, left: 0, 'min-width': '100%', 'min-height': '100%' }}
    src={background} alt=''
  />
  )
}

export default Home
