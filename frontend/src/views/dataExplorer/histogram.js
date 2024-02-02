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
import ResponsivePlot from '../../components/responsivePlot'
import CMSOMSCard from '../../components/cmsOMSCard'
import { isNumericNonZero, isStringNonEmpty } from '../../utils/sanitizer'

const Histogram = (props) => {
  const navigate = useNavigate()
  const { id } = useParams()
  const { dim } = props

  const [isLoading, setLoading] = useState(true)
  const [data, setData] = useState({})
  const [plotData, setPlotData] = useState([])
  const [plotLayout, setPlotLayout] = useState([])
  const [runNumber, setRunNumber] = useState()
  const [lsNumber, setLsNumber] = useState()
  const [title, setTitle] = useState()
  const [runNumberIsInvalid, setRunNumberIsInvalid] = useState()
  const [lsNumberIsInvalid, setLsNumberIsInvalid] = useState()
  const [titleIsInvalid, setTitleIsInvalid] = useState()

  useEffect(() => {
    const fetchData = () => {
      setLoading(true)
      API.lumisection.getHistogram(dim, id)
        .then(response => {
          const data = dim === 1
            ? [
                {
                  y: response.data,
                  x: response.xbins,
                  type: 'bar',
                  marker: { color: '#0033A0' }
                }
              ]
            : [
                {
                  z: response.data,
                  x: response.xbins,
                  y: response.ybins,
                  type: 'heatmap',
                  colorscale: 'Viridis'
                }
              ]
          const layout = {
            bargap: 0,
            margin: { t: 20, b: 20, l: 20, r: 20 }
          }
          setData(response)
          setPlotData(data)
          setPlotLayout(layout)
          setRunNumber(response.run_number)
          setLsNumber(response.ls_number)
          setTitle(response.title)
        })
        .catch(error => {
          console.error(error)
        })
        .finally(() => {
          setLoading(false)
        })
    }

    fetchData()
  }, [id])

  const validateSearhForm = () => {
    const isRunValid = isNumericNonZero(runNumber)
    const isLsValid = isNumericNonZero(lsNumber)
    const isTitleValid = isStringNonEmpty(title)
    setRunNumberIsInvalid(!isRunValid)
    setLsNumberIsInvalid(!isLsValid)
    setTitleIsInvalid(!isTitleValid)
    return isRunValid && isLsValid && isTitleValid
  }

  const handleSearch = () => {
    const isFormValid = validateSearhForm()
    if (!isFormValid) {
      return
    }

    API.lumisection.listHistograms(dim, { run: runNumber, ls: lsNumber, title })
      .then(response => {
        if (response.count === 0) {
          toast.error('Histogram not found!')
        } else {
          return navigate(`/histograms-${dim}d/${response.results[0].id}`)
        }
      })
      .catch(error => {
        console.error(error)
        toast.error('Failure to communicate with the API!')
      })
  }

  return (
    <>
      <Row className='mt-5 mb-3 m-3'>
        <Breadcrumb>
          <Breadcrumb.Item linkAs={Link} linkProps={{ to: '/runs' }}>All runs</Breadcrumb.Item>
          {
            isLoading
              ? (
                <Breadcrumb.Item active>Loading...</Breadcrumb.Item>
                )
              : (
                <>
                  <Breadcrumb.Item linkAs={Link} linkProps={{ to: `/runs/${data.run_number}` }}>{`Run ${data.run_number}`}</Breadcrumb.Item>
                  <Breadcrumb.Item linkAs={Link} linkProps={{ to: { pathname: `/lumisections/${data.ls_number}`, search: `?runNumber=${data.run_number}` } }}>{`Lumisection ${data.ls_number}`}</Breadcrumb.Item>
                  <Breadcrumb.Item active>{`H${dim}D #${data.id}`}</Breadcrumb.Item>
                </>
                )
          }
        </Breadcrumb>
      </Row>
      <Row className='mt-1 mb-3 m-3'>
        <Col sm={9}>
          <Card>
            {
              isLoading
                ? (
                  <Spinner
                    animation='border'
                    role='status'
                  />
                  )
                : (
                  <Card.Header>{`${data.title} - ${data.entries} entries`}</Card.Header>
                  )
            }
            <Card.Body>
              {
                isLoading
                  ? (
                    <Spinner
                      animation='border'
                      role='status'
                    />
                    )
                  : (
                    <>
                      <ResponsivePlot
                        data={plotData}
                        layout={plotLayout}
                        boxWidth='100%'
                        boxHeight='70vh'
                      />
                    </>
                    )
              }
            </Card.Body>
          </Card>
        </Col>
        <Col sm={3}>
          <CMSOMSCard isLoading={isLoading} runNumber={data.run_number} />
          <Card className='mt-3'>
            <Card.Header>Search</Card.Header>
            <Card.Body>
              <Form.Group className='mb-3' controlId='formRunNumber'>
                <Form.Label>Run Number</Form.Label>
                <Form.Control
                  type='number'
                  value={runNumber}
                  onChange={e => setRunNumber(e.target.value)}
                  isInvalid={runNumberIsInvalid}
                />
                <Form.Control.Feedback type='invalid'>Run number cannot be empty</Form.Control.Feedback>
              </Form.Group>

              <Form.Group className='mb-3' controlId='formLsNumber'>
                <Form.Label>Lumisection Number</Form.Label>
                <Form.Control
                  type='number'
                  value={lsNumber}
                  onChange={e => setLsNumber(e.target.value)}
                  isInvalid={lsNumberIsInvalid}
                />
                <Form.Control.Feedback type='invalid'>Lumisection number cannot be empty</Form.Control.Feedback>
              </Form.Group>

              <Form.Group className='mb-3' controlId='formTitle'>
                <Form.Label>Title</Form.Label>
                <Form.Control
                  type='string'
                  value={title}
                  onChange={e => setTitle(e.target.value)}
                  isInvalid={titleIsInvalid}
                />
                <Form.Control.Feedback type='invalid'>Title cannot be empty</Form.Control.Feedback>
              </Form.Group>

              <Button
                variant='primary'
                type='submit'
                onClick={handleSearch}
              >
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
