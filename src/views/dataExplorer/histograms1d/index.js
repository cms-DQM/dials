import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import Histograms1DFilter from './filters'
import Histograms1DViz from './dataViz'

const Histograms1D = () => {
  return (
    <Row className="px-4 my-5 m-0">
      <Col sm={3}>
        <Histograms1DFilter/>
      </Col>
      <Col sm={9}>
        <Histograms1DViz/>
      </Col>
    </Row>
  )
}

export default Histograms1D;