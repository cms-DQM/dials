import React from 'react'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

import FileIndexFilter from './filters'
import FileIndexViz from './dataViz'

const FileIndex = () => {
  return (
    <Row className='mt-5 mb-3 m-3'>
      <Col sm={3}>
        <FileIndexFilter/>
      </Col>
      <Col sm={9}>
        <FileIndexViz/>
      </Col>
    </Row>
  )
}

export default FileIndex
