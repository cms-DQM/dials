import React from 'react';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import RunsSearch from './search'
import RunsFilter from './filters'
import RunsViz from './dataViz'

const Runs = () => {
  return (
    <Row className="mt-5 mb-3 m-3">
      <Col sm={3}>
        <div className='mb-4'><RunsFilter /></div>
        <div><RunsSearch /></div>
      </Col>
      <Col sm={9}>
        <RunsViz />
      </Col>
    </Row>
  )
}

export default Runs;