import React, { useState, useEffect } from 'react'

import { useNavigate, useParams, Link } from 'react-router-dom'
import Breadcrumb from 'react-bootstrap/Breadcrumb'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Card from 'react-bootstrap/Card'
import Spinner from 'react-bootstrap/Spinner'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import { toast } from 'react-toastify'

import API from '../../services/api'
import { CMSOMSCard, ResponsivePlot } from '../components'
import { isNumericNonZero, isStringNonEmpty } from '../../utils/sanitizer'

const Histogram = (props) => {
  const navigate = useNavigate()
  const { datasetId, runNumber, lsNumber, meId } = useParams()
  const { dim } = props
  const [isLoading, setLoading] = useState(true)

  // API results
  const [data, setData] = useState({})
  const [plotData, setPlotData] = useState([])
  const [plotLayout, setPlotLayout] = useState([])

  // Search
  const [searchDataset, setSearchDataset] = useState()
  const [searchRunNumber, setSearchRunNumber] = useState()
  const [searchLsNumber, setSearchLsNumber] = useState()
  const [searchMe, setSearchMe] = useState()

  // Form validation
  const [searchDatasetIsInvalid, setSearchDatasetIsInvalid] = useState()
  const [searchRunNumberIsInvalid, setSearchRunNumberIsInvalid] = useState()
  const [searchLsNumberIsInvalid, setSearchLsNumberIsInvalid] = useState()
  const [searchMeIsInvalid, setSearchMeIsInvalid] = useState()

  useEffect(() => {
    const fetchData = () => {
      setLoading(true)
      API.histogram
        .get({ dim, datasetId, runNumber, lsNumber, meId })
        .then((response) => {
          const data =
            dim === 1
              ? [
                  {
                    y: response.data,
                    x: response.xbins,
                    type: 'bar',
                    marker: { color: '#0033A0' },
                  },
                ]
              : [
                  {
                    z: response.data,
                    x: response.xbins,
                    y: response.ybins,
                    type: 'heatmap',
                    colorscale: 'Viridis',
                  },
                ]
          const layout = {
            bargap: 0,
            margin: { t: 20, b: 20, l: 20, r: 20 },
          }
          setData(response)
          setPlotData(data)
          setPlotLayout(layout)
          setSearchDataset(response.dataset)
          setSearchRunNumber(response.run_number)
          setSearchLsNumber(response.ls_number)
          setSearchMe(response.me)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
        .finally(() => {
          setLoading(false)
        })
    }

    fetchData()
  }, [dim, datasetId, runNumber, lsNumber, meId])

  const validateSearhForm = () => {
    const isDatasetValid = isStringNonEmpty(searchDataset)
    const isRunValid = isNumericNonZero(searchRunNumber)
    const isLsValid = isNumericNonZero(searchLsNumber)
    const isMeValid = isStringNonEmpty(searchMe)
    setSearchDatasetIsInvalid(!isDatasetValid)
    setSearchRunNumberIsInvalid(!isRunValid)
    setSearchLsNumberIsInvalid(!isLsValid)
    setSearchMeIsInvalid(!isMeValid)
    return isDatasetValid && isRunValid && isLsValid && isMeValid
  }

  const handleSearch = () => {
    const isFormValid = validateSearhForm()
    if (!isFormValid) {
      return
    }

    API.histogram
      .list(dim, {
        dataset: searchDataset,
        runNumber: searchRunNumber,
        lsNumber: searchLsNumber,
        me: searchMe,
      })
      .then((response) => {
        if (response.results.length === 0) {
          toast.error('Histogram not found!')
        } else {
          const elem = response.results[0]
          return navigate(
            `/histograms-${dim}d/${elem.dataset_id}/${elem.run_number}/${elem.ls_number}/${elem.me_id}`
          )
        }
      })
      .catch((error) => {
        console.error(error)
        toast.error('Failure to communicate with the API!')
      })
  }

  return (
    <>
      <Row className='mt-5 mb-3 m-3'>
        <Breadcrumb>
          <Breadcrumb.Item linkAs={Link} linkProps={{ to: '/runs' }}>
            All runs
          </Breadcrumb.Item>
          {isLoading ? (
            <Breadcrumb.Item active>Loading...</Breadcrumb.Item>
          ) : (
            <>
              <Breadcrumb.Item
                active
              >{`Dataset ${data.dataset_id} (${data.dataset})`}</Breadcrumb.Item>
              <Breadcrumb.Item
                linkAs={Link}
                linkProps={{
                  to: `/runs/${data.dataset_id}/${data.run_number}`,
                }}
              >{`Run ${data.run_number}`}</Breadcrumb.Item>
              <Breadcrumb.Item
                linkAs={Link}
                linkProps={{
                  to: `/lumisections/${data.dataset_id}/${data.run_number}/${data.ls_number}`,
                }}
              >{`Lumisection ${data.ls_number}`}</Breadcrumb.Item>
              <Breadcrumb.Item
                active
              >{`H${dim}D ME #${data.me_id}`}</Breadcrumb.Item>
            </>
          )}
        </Breadcrumb>
      </Row>
      <Row className='mt-1 mb-3 m-3'>
        <Col sm={9}>
          <Card>
            {isLoading ? (
              <Spinner animation='border' role='status' />
            ) : (
              <Card.Header>{`${data.me} - ${data.entries} entries`}</Card.Header>
            )}
            <Card.Body>
              {isLoading ? (
                <Spinner animation='border' role='status' />
              ) : (
                <>
                  <ResponsivePlot
                    data={plotData}
                    layout={plotLayout}
                    style={{ width: '100%', height: '70vh' }}
                  />
                </>
              )}
            </Card.Body>
          </Card>
        </Col>
        <Col sm={3}>
          <CMSOMSCard isLoading={isLoading} runNumber={data.run_number} />
          <Card className='mt-3'>
            <Card.Header>Search</Card.Header>
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

              <Form.Group className='mb-3' controlId='formMe'>
                <Form.Label>Monitoring element</Form.Label>
                <Form.Control
                  type='string'
                  value={searchMe}
                  onChange={(e) => setSearchMe(e.target.value)}
                  isInvalid={searchMeIsInvalid}
                />
                <Form.Control.Feedback type='invalid'>
                  Monitoring element cannot be empty
                </Form.Control.Feedback>
              </Form.Group>

              <Button variant='primary' type='submit' onClick={handleSearch}>
                Go
              </Button>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </>
  )
}

export default Histogram
