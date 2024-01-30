import React from 'react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

import LumisectionsSearch from './search'
import LumisectionsFilter from './filters'
import LumisectionsViz from './dataViz'

const Lumisections = () => {
  return (
    <Row className='mt-5 mb-3 m-3'>
      <Col sm={3}>
        <div className='mb-4'><LumisectionsFilter /></div>
        <div><LumisectionsSearch /></div>
      </Col>
      <Col sm={9}>
        <LumisectionsViz />
      </Col>
    </Row>
  )
}

export default Lumisections
