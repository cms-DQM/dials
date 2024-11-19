import React, { useState, useEffect } from 'react'

import { useParams, Link } from 'react-router-dom'
import Breadcrumb from 'react-bootstrap/Breadcrumb'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Card from 'react-bootstrap/Card'
import Accordion from 'react-bootstrap/Accordion'
import Spinner from 'react-bootstrap/Spinner'
import { toast } from 'react-toastify'

import API from '../../services/api'
import { CMSOMSCard, ResponsivePlot } from '../components'

const Lumisection = () => {
  const defaultPageSizeTH1 = 500
  const defaultPageSizeTH2 = 10

  const { datasetId, runNumber, lsNumber } = useParams()
  const [isDatasetLoading, setDatasetLoading] = useState(true)
  const [isH1DLoading, setH1DLoading] = useState(true)
  const [isH2DLoading, setH2DLoading] = useState(true)

  // API results
  const [dataset, setDataset] = useState()
  const [h1dData, setH1DData] = useState([])
  const [h2dData, setH2DData] = useState([])
  const [h1dTotalSize, setH1DTotalSize] = useState()
  const [h2dTotalSize, setH2DTotalSize] = useState()

  useEffect(() => {
    const fetchDataset = () => {
      setDatasetLoading(true)
      API.dataset
        .get({ datasetId })
        .then((response) => {
          setDataset(response.dataset)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
        .finally(() => {
          setDatasetLoading(false)
        })
    }

    const fetchH1D = () => {
      setH1DLoading(true)
      API.utils
        .genericFetchAllPages({
          apiMethod: API.histogram.list,
          params: {
            pageSize: defaultPageSizeTH1,
            dim: 1,
            datasetId,
            runNumber,
            lsNumber,
            fields: ['dataset_id', 'run_number', 'ls_number', 'me_id', 'me', 'data']
          },
        })
        .then((response) => {
          setH1DData(response.results)
          setH1DTotalSize(response.count)
          if (response.errorCount > 0) {
            toast.error(
              `Failure to retrieve ${response.errorCount} out of ${response.totalPages} pages from API!`
            )
          }
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
        .finally(() => {
          setH1DLoading(false)
        })
    }

    const fetchH2D = () => {
      setH2DLoading(true)
      API.utils
        .genericFetchAllPages({
          apiMethod: API.histogram.list,
          params: {
            pageSize: defaultPageSizeTH2,
            dim: 2,
            datasetId,
            runNumber,
            lsNumber,
            fields: ['dataset_id', 'run_number', 'ls_number', 'me_id', 'me', 'data']
          },
        })
        .then((response) => {
          setH2DData(response.results)
          setH2DTotalSize(response.count)
          if (response.errorCount > 0) {
            toast.error(
              `Failure to retrieve ${response.errorCount} out of ${response.totalPages} pages from API!`
            )
          }
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
        .finally(() => {
          setH2DLoading(false)
        })
    }

    fetchDataset()
    fetchH1D()
    fetchH2D()
  }, [datasetId, runNumber, lsNumber])

  return (
    <>
      <Row className='mt-5 mb-3 m-3'>
        <Breadcrumb>
          <Breadcrumb.Item linkAs={Link} linkProps={{ to: '/runs' }}>
            All runs
          </Breadcrumb.Item>
          {isDatasetLoading ? (
            <Breadcrumb.Item active>Loading...</Breadcrumb.Item>
          ) : (
            <>
              <Breadcrumb.Item
                active
              >{`Dataset ${datasetId} (${dataset})`}</Breadcrumb.Item>
              <Breadcrumb.Item
                linkAs={Link}
                linkProps={{ to: `/runs/${datasetId}/${runNumber}` }}
              >{`Run ${runNumber}`}</Breadcrumb.Item>
              <Breadcrumb.Item
                active
              >{`Lumisection ${lsNumber}`}</Breadcrumb.Item>
            </>
          )}
        </Breadcrumb>
      </Row>
      <Row className='mt-1 mb-3 m-3'>
        <Col sm={9}>
          <Accordion>
            <Accordion.Item eventKey='0'>
              <Accordion.Header>
                {isH1DLoading
                  ? 'Loading 1D Histograms...'
                  : `1D Histograms - ${h1dTotalSize} monitoring elements`}
              </Accordion.Header>
              <Accordion.Body>
                {isH1DLoading ? (
                  <Spinner animation='border' role='status' />
                ) : (
                  h1dData.map(
                    (obj, index) =>
                      index % 3 === 0 && (
                        <Row key={index} className='mb-3'>
                          {h1dData
                            .slice(index, index + 3)
                            .map((hist, innerIndex) => {
                              const data = [
                                {
                                  y: hist.data,
                                  type: 'bar',
                                  marker: { color: '#0033A0' },
                                },
                              ]
                              const layout = {
                                margin: { t: 10, b: 10, l: 10, r: 10 },
                                yaxis: { visible: false },
                                xaxis: { visible: false },
                                bargap: 0,
                                paper_bgcolor: 'rgba(0,0,0,0)',
                                plot_bgcolor: 'rgba(0,0,0,0)',
                              }
                              return (
                                <Col key={innerIndex} sm={4}>
                                  <Card>
                                    <div className='card-img-top'>
                                      <Link
                                        to={`/histograms-1d/${hist.dataset_id}/${hist.run_number}/${hist.ls_number}/${hist.me_id}`}
                                      >
                                        <ResponsivePlot
                                          data={data}
                                          layout={layout}
                                          config={{ staticPlot: true }}
                                          style={{
                                            width: '100%',
                                            height: '100%',
                                          }}
                                        />
                                      </Link>
                                    </div>
                                    <Card.Body>
                                      <Card.Title>
                                        <Link
                                          to={`/histograms-1d/${hist.dataset_id}/${hist.run_number}/${hist.ls_number}/${hist.me_id}`}
                                        >
                                          {hist.me}
                                        </Link>
                                      </Card.Title>
                                    </Card.Body>
                                  </Card>
                                </Col>
                              )
                            })}
                        </Row>
                      )
                  )
                )}
              </Accordion.Body>
            </Accordion.Item>
            <Accordion.Item eventKey='1'>
              <Accordion.Header>
                {isH2DLoading
                  ? 'Loading 2D Histograms...'
                  : `2D Histograms - ${h2dTotalSize} monitoring elements`}
              </Accordion.Header>
              <Accordion.Body>
                {isH2DLoading ? (
                  <Spinner animation='border' role='status' />
                ) : (
                  h2dData.map(
                    (obj, index) =>
                      index % 3 === 0 && (
                        <Row key={index} className='mb-3'>
                          {h2dData
                            .slice(index, index + 3)
                            .map((hist, innerIndex) => {
                              const data = [
                                {
                                  z: hist.data,
                                  type: 'heatmap',
                                  colorscale: 'Viridis',
                                },
                              ]
                              const layout = {
                                margin: { t: 10, b: 10, l: 10, r: 10 },
                                yaxis: { visible: false },
                                xaxis: { visible: false },
                                bargap: 0,
                                paper_bgcolor: 'rgba(0,0,0,0)',
                                plot_bgcolor: 'rgba(0,0,0,0)',
                              }
                              return (
                                <Col key={innerIndex} sm={4}>
                                  <Card>
                                    <div className='card-img-top'>
                                      <Link
                                        to={`/histograms-2d/${hist.dataset_id}/${hist.run_number}/${hist.ls_number}/${hist.me_id}`}
                                      >
                                        <ResponsivePlot
                                          data={data}
                                          layout={layout}
                                          config={{ staticPlot: true }}
                                          style={{
                                            width: '100%',
                                            height: '100%',
                                          }}
                                        />
                                      </Link>
                                    </div>
                                    <Card.Body>
                                      <Card.Title>
                                        <Link
                                          to={`/histograms-2d/${hist.dataset_id}/${hist.run_number}/${hist.ls_number}/${hist.me_id}`}
                                        >
                                          {hist.me}
                                        </Link>
                                      </Card.Title>
                                    </Card.Body>
                                  </Card>
                                </Col>
                              )
                            })}
                        </Row>
                      )
                  )
                )}
              </Accordion.Body>
            </Accordion.Item>
          </Accordion>
        </Col>
        <Col sm={3}>
          <CMSOMSCard runNumber={runNumber} />
        </Col>
      </Row>
    </>
  )
}

export default Lumisection
