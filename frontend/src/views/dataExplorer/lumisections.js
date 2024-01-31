import React, { useState, useEffect } from 'react'

import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import paginationFactory from 'react-bootstrap-table2-paginator'

import Table from '../../components/table'
import API from '../../services/api'

const Lumisections = () => {
  // Loading indicator and filter props
  const [isLoading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [minLs, setMinLs] = useState()
  const [maxLs, setMaxLs] = useState()
  const [minRun, setMinRun] = useState()
  const [maxRun, setMaxRun] = useState()

  // Search props
  const [lumisectionNumber, setLumisectionNumber] = useState()
  const [runNumber, setRunNumber] = useState()

  // Actual data after fetching
  const [data, setData] = useState([])
  const [totalSize, setTotalSize] = useState()

  // Boolean to trigger useEffect
  const [filterSubmited, setFilterSubmited] = useState(false)

  const columns = [
    { dataField: 'ls_number', text: 'Lumisection', type: 'number' },
    { dataField: 'run', text: 'Run', type: 'number' },
    { dataField: 'oms_zerobias_rate', text: 'OMS ZeroBias Rate', type: 'string' }
  ]
  const pagination = paginationFactory({ page, totalSize, hideSizePerPage: true })
  const remote = { pagination: true, filter: false, sort: false }

  const handleTableChange = (type, { page }) => {
    if (type === 'pagination') {
      setPage(page)
    }
  }

  useEffect(() => {
    const handleData = () => {
      setLoading(true)
      API.lumisection.get({ page, minLs, maxLs, minRun, maxRun })
        .then(response => {
          setData(response.results)
          setTotalSize(response.count)
        })
        .catch(error => {
          console.error(error)
        })
        .finally(() => {
          setLoading(false)
        })
    }
    handleData()
  }, [page, filterSubmited])

  return (
    <Row className='mt-5 mb-3 m-3'>
      <Col sm={3}>
        <div className='mb-4'>
          <Card>
            <Card.Header className='text-center' as='h4'>Filters</Card.Header>
            <Card.Body>
              <Form.Group className='mb-3' controlId='formMinRun'>
                <Form.Label>Lumisection Range</Form.Label>
                <Row>
                  <Col xs={6}>
                    <Form.Control
                      type='number'
                      value={minLs}
                      placeholder='Min'
                      onChange={e => setMinLs(e.target.value)}
                    />
                  </Col>
                  <Col xs={6}>
                    <Form.Control
                      type='number'
                      value={maxLs}
                      placeholder='Max'
                      onChange={e => setMaxLs(e.target.value)}
                    />
                  </Col>
                </Row>
              </Form.Group>

              <Form.Group className='mb-3' controlId='formMinRun'>
                <Form.Label>Run Range</Form.Label>
                <Row>
                  <Col xs={6}>
                    <Form.Control
                      type='number'
                      value={minRun}
                      placeholder='Min'
                      onChange={e => setMinRun(e.target.value)}
                    />
                  </Col>
                  <Col xs={6}>
                    <Form.Control
                      type='number'
                      value={maxRun}
                      placeholder='Max'
                      onChange={e => setMaxRun(e.target.value)}
                    />
                  </Col>
                </Row>
              </Form.Group>

              <Button
                variant='primary'
                type='submit'
                onClick={() => {
                  setPage(1)
                  setFilterSubmited(!filterSubmited)
                }}
              >
                Submit
              </Button>
            </Card.Body>
          </Card>
        </div>
        {/* TODO: Integrate search form to fetch exactly one lumisection and display a page for it */}
        {/* <div>
          <Card>
            <Card.Header className='text-center' as='h4'>Search</Card.Header>
            <Card.Body>
              <Form.Group className='mb-3' controlId='formRunNumber'>
                <Form.Label>Lumisection Number</Form.Label>
                <Form.Control
                  type='number'
                  value={lumisectionNumber}
                  onChange={e => setLumisectionNumber(e.target.value)}
                />
              </Form.Group>

              <Form.Group className='mb-3' controlId='formRunNumber'>
                <Form.Label>Run Number</Form.Label>
                <Form.Control
                  type='number'
                  value={runNumber}
                  onChange={e => setRunNumber(e.target.value)}
                />
              </Form.Group>

              <Button
                variant='primary'
                type='submit'
              >
                Submit
              </Button>
            </Card.Body>
          </Card>
        </div> */}
      </Col>
      <Col sm={9}>
        <Card className='text-center'>
          <Card.Header as='h4'>Lumisections</Card.Header>
          <Card.Body>
            <Table
              keyField='file_path'
              isLoading={isLoading}
              data={data}
              columns={columns}
              bordered={false}
              hover={true}
              remote={remote}
              pagination={pagination}
              onTableChange={handleTableChange}
            />
          </Card.Body>
        </Card>
      </Col>
    </Row>
  )
}

export default Lumisections
