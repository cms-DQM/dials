import React, { useState } from 'react'

import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Card from 'react-bootstrap/Card'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import RangeSlider from 'react-bootstrap-range-slider'

import { FILE_INDEX_STATUSES } from '../../../services/api'

const FileIndexFilter = () => {
  const [pathContains, setPathContains] = useState()
  const [dataEra, setDataEra] = useState()
  const [minSize, setMinSize] = useState(0)
  const [fileStatus, setFileStatus] = useState()

  const handleClick = () => { }

  return (
    <Card>
      <Card.Header className='text-center' as='h4'>Filters</Card.Header>
      <Card.Body>
        <Form.Group className='mb-3' controlId='formPathContains'>
          <Form.Label>Path contains</Form.Label>
          <Form.Control
            type='string'
            placeholder='Enter path substring'
            value={pathContains}
            onChange={e => setPathContains(e.target.value)}
          />
        </Form.Group>

        <Form.Group className='mb-3' controlId='formDataEra'>
          <Form.Label>Era</Form.Label>
          <Form.Control
            type='string'
            placeholder='Enter data era'
            value={dataEra}
            onChange={e => setDataEra(e.target.value)}
          />
        </Form.Group>

        <Form.Group className='mb-3' controlId='formSizeRange' as={Row}>
          <Form.Label>Minimum size (MB)</Form.Label>
          <Col xs={3}>
            <Form.Control
              type='number'
              value={minSize}
              onChange={e => setMinSize(e.target.value)}
            />
          </Col>
          <Col xs={9}>
            <RangeSlider
              min={0}
              max={1000}
              value={minSize}
              onChange={e => setMinSize(e.target.value)}
            />
          </Col>
        </Form.Group>

        <Form.Group className='mb-3' controlId='formFileStatus'>
          <Form.Label>Status</Form.Label>
          <Form.Select
            default=''
            value={fileStatus}
            onChange={e => setFileStatus(e.target.value)}
          >
            <option key='blankChoice' hidden value/>
            {
              FILE_INDEX_STATUSES.map(item => {
                return (<option key={item} value={item}>{item}</option>)
              })
            }
          </Form.Select>
        </Form.Group>

        <Button
          variant='primary'
          type='submit'
          onClick={handleClick}
        >
          Submit
        </Button>
      </Card.Body>
    </Card>
  )
}

export default FileIndexFilter
