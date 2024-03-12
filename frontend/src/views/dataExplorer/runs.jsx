import React, { useState, useEffect } from 'react'

import { Link, useNavigate } from 'react-router-dom'
import Card from 'react-bootstrap/Card'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import paginationFactory from 'react-bootstrap-table2-paginator'
import { toast } from 'react-toastify'

import { Table } from '../../components'
import API from '../../services/api'
import { isNumericNonZero } from '../../utils/sanitizer'

const Runs = () => {
  const navigate = useNavigate()

  const [isLoading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [minRun, setMinRun] = useState()
  const [maxRun, setMaxRun] = useState()
  const [runNumber, setRunNumber] = useState()
  const [runNumberIsInvalid, setRunNumberIsInvalid] = useState()
  const [data, setData] = useState([])
  const [totalSize, setTotalSize] = useState()
  const [filterSubmited, setFilterSubmited] = useState(false)

  const columns = [
    {
      dataField: 'run_number',
      text: 'Run',
      type: 'number',
      formatter: (cell, row) => {
        const linkTo = row.run_number.toString()
        return <Link to={linkTo}>{row.run_number}</Link>
      },
    },
    { dataField: 'year', text: 'Year', type: 'string' },
    { dataField: 'period', text: 'Period', type: 'string' },
    { dataField: 'oms_fill', text: 'OMS Fill', type: 'string' },
    { dataField: 'oms_lumisections', text: 'OMS Lumisections', type: 'string' },
    { dataField: 'oms_initial_lumi', text: 'OMS Initial Lumi', type: 'string' },
    { dataField: 'oms_end_lumi', text: 'OMS End Lumi', type: 'string' },
  ]
  const pagination = paginationFactory({
    page,
    totalSize,
    hideSizePerPage: true,
    showTotal: true,
  })
  const remote = { pagination: true, filter: false, sort: false }

  const handleTableChange = (type, { page }) => {
    if (type === 'pagination') {
      setPage(page)
    }
  }

  const validateSearchForm = () => {
    const isRunValid = isNumericNonZero(runNumber)
    setRunNumberIsInvalid(!isRunValid)
    return isRunValid
  }

  const handleSearch = () => {
    const isFormValid = validateSearchForm()
    if (!isFormValid) {
      return
    }

    API.run
      .get({ run: runNumber })
      .then((response) => {
        return navigate(runNumber)
      })
      .catch((error) => {
        if (error.response.status === 404) {
          toast.error('Run not found!')
        } else {
          toast.error('Failure to communicate with the API!')
        }
      })
  }

  const handleFilter = () => {
    setPage(1)
    setFilterSubmited(!filterSubmited)
  }

  useEffect(() => {
    const handleData = () => {
      setLoading(true)
      API.run
        .list({ page, minRun, maxRun })
        .then((response) => {
          setData(response.results)
          setTotalSize(response.count)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
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
            <Card.Header className='text-center' as='h4'>
              Filters
            </Card.Header>
            <Card.Body>
              <Form.Group className='mb-3' controlId='formRunRange'>
                <Form.Label>Run Range</Form.Label>
                <Row>
                  <Col xs={6}>
                    <Form.Control
                      type='number'
                      value={minRun}
                      placeholder='Min'
                      onChange={(e) => setMinRun(e.target.value)}
                    />
                  </Col>
                  <Col xs={6}>
                    <Form.Control
                      type='number'
                      value={maxRun}
                      placeholder='Max'
                      onChange={(e) => setMaxRun(e.target.value)}
                    />
                  </Col>
                </Row>
              </Form.Group>

              <Button variant='primary' type='submit' onClick={handleFilter}>
                Submit
              </Button>
            </Card.Body>
          </Card>
        </div>
        <div>
          <Card>
            <Card.Header className='text-center' as='h4'>
              Search
            </Card.Header>
            <Card.Body>
              <Form.Group className='mb-3' controlId='formRunNumber'>
                <Form.Label>Run Number</Form.Label>
                <Form.Control
                  type='number'
                  value={runNumber}
                  onChange={(e) => setRunNumber(e.target.value)}
                  isInvalid={runNumberIsInvalid}
                />
                <Form.Control.Feedback type='invalid'>
                  Run number cannot be empty
                </Form.Control.Feedback>
              </Form.Group>

              <Button variant='primary' type='submit' onClick={handleSearch}>
                Go
              </Button>
            </Card.Body>
          </Card>
        </div>
      </Col>
      <Col sm={9}>
        <Card className='text-center'>
          <Card.Header as='h4'>Runs</Card.Header>
          <Card.Body>
            <Table
              keyField='run_number'
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

export default Runs
