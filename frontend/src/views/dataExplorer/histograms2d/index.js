import React from 'react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

import Histograms2DFilter from './filters'
import Histograms2DViz from './dataViz'

const Histograms2D = () => {
  return (
    <Row className='mt-5 mb-3 m-3'>
      <Col sm={3}>
        <Histograms2DFilter/>
      </Col>
      <Col sm={9}>
        <Histograms2DViz/>
      </Col>
    </Row>
  )
}

export default Histograms2D
