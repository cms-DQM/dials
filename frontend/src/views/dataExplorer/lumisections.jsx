import React, { useState, useEffect } from 'react'

import { Link, useNavigate } from 'react-router-dom'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import { toast } from 'react-toastify'

import { Table } from '../../components'
import API from '../../services/api'
import {
  isNumericNonZero,
  isStringNonEmpty,
  getNextToken,
} from '../../utils/sanitizer'

const Lumisections = () => {
  const navigate = useNavigate()
  const [isLoading, setLoading] = useState(true)

  // Filters
  const [dataset, setDataset] = useState()
  const [datasetRegex, setDatasetRegex] = useState()
  const [runNumber, setRunNumber] = useState()
  const [runNumberLte, setRunNumberLte] = useState()
  const [runNumberGte, setRunNumberGte] = useState()
  const [lsNumber, setLsNumber] = useState()
  const [lsNumberLte, setLsNumberNumberLte] = useState()
  const [lsNumberGte, setLsNumberNumberGte] = useState()

  // Search
  const [searchDataset, setSearchDataset] = useState()
  const [searchRunNumber, setSearchRunNumber] = useState()
  const [searchLsNumber, setSearchLsNumber] = useState()

  // Form validation
  const [searchDatasetIsInvalid, setSearchDatasetIsInvalid] = useState()
  const [searchRunNumberIsInvalid, setSearchRunNumberIsInvalid] = useState()
  const [searchLsNumberIsInvalid, setSearchLsNumberIsInvalid] = useState()

  // API results
  const [data, setData] = useState([])
  const [nextToken, setNextToken] = useState(null)
  const [previousToken, setPreviousToken] = useState(null)

  const columns = [
    {
      dataField: 'dataset',
      text: 'Dataset',
      type: 'number',
    },
    {
      dataField: 'run_number',
      text: 'Run',
      type: 'number',
      formatter: (cell, row) => {
        const linkTo = `/runs/${row.dataset_id}/${row.run_number}`
        return <Link to={linkTo}>{row.run_number}</Link>
      },
    },
    {
      dataField: 'ls_number',
      text: 'Lumisection',
      type: 'number',
      formatter: (cell, row) => {
        const linkTo = `/lumisections/${row.dataset_id}/${row.run_number}/${row.ls_number}`
        return <Link to={linkTo}>{row.ls_number}</Link>
      },
    },
    {
      dataField: 'th1_count',
      text: 'TH1 Count',
      type: 'number',
    },
    {
      dataField: 'th2_count',
      text: 'TH2 Count',
      type: 'number',
    },
  ]

  const validateSearchForm = () => {
    const isDatasetValid = isStringNonEmpty(searchDataset)
    const isRunValid = isNumericNonZero(searchRunNumber)
    const isLsValid = isNumericNonZero(searchLsNumber)
    setSearchDatasetIsInvalid(!isDatasetValid)
    setSearchRunNumberIsInvalid(!isRunValid)
    setSearchLsNumberIsInvalid(!isLsValid)
    return isDatasetValid && isRunValid && isLsValid
  }

  const handleSearch = () => {
    const isFormValid = validateSearchForm()
    if (!isFormValid) {
      return
    }

    API.dataset
      .list({ dataset: searchDataset })
      .then((response) => {
        if (response.length === 0) {
          toast.error('Dataset not found!')
        } else {
          const datasetId = response.results[0].dataset_id
          API.lumisection
            .get({
              datasetId,
              runNumber: searchRunNumber,
              lsNumber: searchLsNumber,
            })
            .then((lsResponse) => {
              return navigate(
                `${datasetId}/${searchRunNumber}/${searchLsNumber}`
              )
            })
            .catch((error) => {
              if (error.response.status === 404) {
                toast.error('Lumisection not found!')
              } else {
                toast.error('Failure to communicate with the API!')
              }
            })
        }
      })
      .catch((error) => {
        if (error.response.status === 404) {
          toast.error('Dataset not found!')
        } else {
          toast.error('Failure to communicate with the API!')
        }
      })
  }

  const fetchData = ({
    nextToken,
    dataset,
    datasetRegex,
    runNumber,
    runNumberLte,
    runNumberGte,
    lsNumber,
    lsNumberLte,
    lsNumberGte,
  }) => {
    setLoading(true)
    API.lumisection
      .list({
        nextToken,
        dataset,
        datasetRegex,
        runNumber,
        runNumberLte,
        runNumberGte,
        lsNumber,
        lsNumberLte,
        lsNumberGte,
      })
      .then((response) => {
        const results = response.results.map((item) => {
          return {
            ...item,
            keyField: `${item.dataset_id}_${item.run_number}_${item.ls_number}`,
          }
        })
        const nextToken = getNextToken(response, 'next')
        const previousToken = getNextToken(response, 'previous')
        setData(results)
        setNextToken(nextToken)
        setPreviousToken(previousToken)
      })
      .catch((error) => {
        console.error(error)
        toast.error('Failure to communicate with the API!')
      })
      .finally(() => {
        setLoading(false)
      })
  }

  useEffect(() => {
    fetchData({})
  }, [])

  return (
    <Row className='mt-5 mb-3 m-3'>
      <Col sm={3}>
        <div className='mb-4'>
          <Card>
            <Card.Header className='text-center' as='h4'>
              Filters
            </Card.Header>
            <Card.Body>
              <Form.Group className='mb-3' controlId='formDataset'>
                <Form.Label>Dataset</Form.Label>
                <Form.Control
                  type='string'
                  placeholder='Enter dataset'
                  value={dataset}
                  onChange={(e) => setDataset(e.target.value)}
                />
              </Form.Group>

              <Form.Group className='mb-3' controlId='formDatasetRegex'>
                <Form.Label>Dataset regex</Form.Label>
                <Form.Control
                  type='string'
                  placeholder='Enter dataset regex'
                  value={datasetRegex}
                  onChange={(e) => setDatasetRegex(e.target.value)}
                />
              </Form.Group>

              <Form.Group className='mb-3' controlId='formRunNumber'>
                <Form.Label>Run</Form.Label>
                <Form.Control
                  type='number'
                  placeholder='Enter run number'
                  value={runNumber}
                  onChange={(e) => setRunNumber(e.target.value)}
                />
              </Form.Group>

              <Form.Group className='mb-3' controlId='formRunRange'>
                <Form.Label>Run range</Form.Label>
                <Row>
                  <Col xs={6}>
                    <Form.Control
                      type='number'
                      value={runNumberGte}
                      placeholder='Min'
                      onChange={(e) => setRunNumberGte(e.target.value)}
                    />
                  </Col>
                  <Col xs={6}>
                    <Form.Control
                      type='number'
                      value={runNumberLte}
                      placeholder='Max'
                      onChange={(e) => setRunNumberLte(e.target.value)}
                    />
                  </Col>
                </Row>
              </Form.Group>

              <Form.Group className='mb-3' controlId='formLsNumber'>
                <Form.Label>Lumisection</Form.Label>
                <Form.Control
                  type='number'
                  placeholder='Enter lumisection number'
                  value={lsNumber}
                  onChange={(e) => setLsNumber(e.target.value)}
                />
              </Form.Group>

              <Form.Group className='mb-3' controlId='formLsRange'>
                <Form.Label>Lumisection range</Form.Label>
                <Row>
                  <Col xs={6}>
                    <Form.Control
                      type='number'
                      value={lsNumberGte}
                      placeholder='Min'
                      onChange={(e) => setLsNumberNumberGte(e.target.value)}
                    />
                  </Col>
                  <Col xs={6}>
                    <Form.Control
                      type='number'
                      value={lsNumberLte}
                      placeholder='Max'
                      onChange={(e) => setLsNumberNumberLte(e.target.value)}
                    />
                  </Col>
                </Row>
              </Form.Group>

              <Button
                variant='primary'
                type='submit'
                onClick={() => {
                  fetchData({
                    dataset,
                    datasetRegex,
                    runNumber,
                    runNumberLte,
                    runNumberGte,
                    lsNumber,
                    lsNumberLte,
                    lsNumberGte,
                  })
                }}
              >
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
              <Form.Group className='mb-3' controlId='formSearchDataset'>
                <Form.Label>Dataset</Form.Label>
                <Form.Control
                  type='string'
                  value={searchDataset}
                  onChange={(e) => setSearchDataset(e.target.value)}
                  isInvalid={searchDatasetIsInvalid}
                />
                <Form.Control.Feedback type='invalid'>
                  Dataset cannot be empty
                </Form.Control.Feedback>
              </Form.Group>

              <Form.Group className='mb-3' controlId='formSearchRunNumber'>
                <Form.Label>Run number</Form.Label>
                <Form.Control
                  type='number'
                  value={searchRunNumber}
                  onChange={(e) => setSearchRunNumber(e.target.value)}
                  isInvalid={searchRunNumberIsInvalid}
                />
                <Form.Control.Feedback type='invalid'>
                  Run number cannot be empty
                </Form.Control.Feedback>
              </Form.Group>

              <Form.Group className='mb-3' controlId='formRunNumber'>
                <Form.Label>Lumisection number</Form.Label>
                <Form.Control
                  type='number'
                  value={searchLsNumber}
                  onChange={(e) => setSearchLsNumber(e.target.value)}
                  isInvalid={searchLsNumberIsInvalid}
                />
                <Form.Control.Feedback type='invalid'>
                  Lumisection number cannot be empty
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
          <Card.Header as='h4'>Lumisections</Card.Header>
          <Card.Body>
            <Table
              keyField='keyField'
              isLoading={isLoading}
              data={data}
              columns={columns}
              bordered={false}
              hover={true}
              remote
              cursorPagination={true}
              previousToken={previousToken}
              nextToken={nextToken}
              previousOnClick={() => {
                fetchData({
                  nextToken: previousToken,
                  dataset,
                  datasetRegex,
                  runNumber,
                  runNumberLte,
                  runNumberGte,
                  lsNumber,
                  lsNumberLte,
                  lsNumberGte,
                })
              }}
              nextOnClick={() => {
                fetchData({
                  nextToken,
                  dataset,
                  datasetRegex,
                  runNumber,
                  runNumberLte,
                  runNumberGte,
                  lsNumber,
                  lsNumberLte,
                  lsNumberGte,
                })
              }}
            />
          </Card.Body>
        </Card>
      </Col>
    </Row>
  )
}

export default Lumisections
