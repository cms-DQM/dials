import React, { useState, useEffect } from 'react'

import { useParams, useLocation, Link } from 'react-router-dom'
import Breadcrumb from 'react-bootstrap/Breadcrumb'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Card from 'react-bootstrap/Card'
import Accordion from 'react-bootstrap/Accordion'
import Spinner from 'react-bootstrap/Spinner'

import API from '../../services/api'
import ResponsivePlot from '../../components/responsivePlot'
import CMSOMSCard from '../../components/cmsOMSCard'

const Lumisection = () => {
  const { lsNumber } = useParams()
  const location = useLocation()
  const runNumber = new URLSearchParams(location.search).get('runNumber')

  const [isH1DLoading, setH1DLoading] = useState(true)
  const [isH2DLoading, setH2DLoading] = useState(true)
  const [h1dData, setH1DData] = useState([])
  const [h2dData, setH2DData] = useState([])
  const [h1dTotalSize, setH1DTotalSize] = useState()
  const [h2dTotalSize, setH2DTotalSize] = useState()

  useEffect(() => {
    const genericFetchAllPages = async (dim) => {
      const allData = []
      let nextPageExists = true
      let page = 0
      while (nextPageExists) {
        page++
        const { results, next } = await API.lumisection.listHistograms(dim, { page, run: runNumber, ls: lsNumber })
        results.forEach(e => allData.unshift(e))
        nextPageExists = !(next === null)
      }
      return { results: allData, count: allData.length }
    }
    const handleH1D = () => {
      setH1DLoading(true)
      genericFetchAllPages(1)
        .then(response => {
          setH1DData(response.results)
          setH1DTotalSize(response.count)
        })
        .catch(error => {
          console.error(error)
        })
        .finally(() => {
          setH1DLoading(false)
        })
    }
    const handleH2D = () => {
      setH2DLoading(true)
      genericFetchAllPages(2)
        .then(response => {
          setH2DData(response.results)
          setH2DTotalSize(response.count)
        })
        .catch(error => {
          console.error(error)
        })
        .finally(() => {
          setH2DLoading(false)
        })
    }

    handleH1D()
    handleH2D()
  }, [])

  return (
    <>
      <Row className='mt-5 mb-3 m-3'>
        <Breadcrumb>
          <Breadcrumb.Item linkAs={Link} linkProps={{ to: '/runs' }}>All runs</Breadcrumb.Item>
          <Breadcrumb.Item linkAs={Link} linkProps={{ to: `/runs/${runNumber}` }}>{`Run ${runNumber}`}</Breadcrumb.Item>
          <Breadcrumb.Item active>{`Lumisection ${lsNumber}`}</Breadcrumb.Item>
        </Breadcrumb>
      </Row>
      <Row className='mt-1 mb-3 m-3'>
        <Col sm={9}>
          <Accordion>
            <Accordion.Item eventKey='0'>
              <Accordion.Header>{`1D Histograms - ${h1dTotalSize} monitoring elements`}</Accordion.Header>
              <Accordion.Body>
                {
                  isH1DLoading
                    ? (
                      <Spinner
                        animation='border'
                        role='status'
                      />
                      )
                    : (
                        h1dData.map((obj, index) => (
                          index % 3 === 0 && (
                          <Row key={index} className='mb-3'>
                            {h1dData.slice(index, index + 3).map((hist, innerIndex) => {
                              const data = [{ y: hist.data, type: 'bar', marker: { color: '#0033A0' } }]
                              const layout = {
                                margin: { t: 10, b: 10, l: 10, r: 10 },
                                yaxis: { visible: false },
                                xaxis: { visible: false },
                                bargap: 0,
                                paper_bgcolor: 'rgba(0,0,0,0)',
                                plot_bgcolor: 'rgba(0,0,0,0)'
                              }
                              return (
                                <Col key={innerIndex} sm={4}>
                                  <Card>
                                    <div className='card-img-top'>
                                      <ResponsivePlot
                                        data={data}
                                        layout={layout}
                                        config={{ staticPlot: true }}
                                        boxHeight={'200pt'}
                                      />
                                    </div>
                                    <Card.Body>
                                      <Card.Title>{hist.title}</Card.Title>
                                    </Card.Body>
                                  </Card>
                                </Col>
                              )
                            })}
                          </Row>
                          )
                        ))
                      )
                }
              </Accordion.Body>
            </Accordion.Item>
            <Accordion.Item eventKey='1'>
              <Accordion.Header>{`2D Histograms - ${h2dTotalSize} monitoring elements`}</Accordion.Header>
              <Accordion.Body>
                {
                  isH2DLoading
                    ? (
                      <Spinner
                        animation='border'
                        role='status'
                      />
                      )
                    : (
                        h2dData.map((obj, index) => (
                          index % 3 === 0 && (
                          <Row key={index} className='mb-3'>
                            {h2dData.slice(index, index + 3).map((hist, innerIndex) => {
                              const data = [{ z: hist.data, type: 'heatmap', colorscale: 'Viridis' }]
                              const layout = {
                                margin: { t: 10, b: 10, l: 10, r: 10 },
                                yaxis: { visible: false },
                                xaxis: { visible: false },
                                bargap: 0,
                                paper_bgcolor: 'rgba(0,0,0,0)',
                                plot_bgcolor: 'rgba(0,0,0,0)'
                              }
                              return (
                                <Col key={innerIndex} sm={4}>
                                  <Card>
                                    <div className='card-img-top'>
                                      <ResponsivePlot
                                        data={data}
                                        layout={layout}
                                        config={{ staticPlot: true }}
                                        boxHeight={'200pt'}
                                      />
                                    </div>
                                    <Card.Body>
                                      <Card.Title>{hist.title}</Card.Title>
                                    </Card.Body>
                                  </Card>
                                </Col>
                              )
                            })}
                          </Row>
                          )
                        ))
                      )
                }
              </Accordion.Body>
            </Accordion.Item>
          </Accordion>
        </Col>
        <Col sm={3}>
          <CMSOMSCard runNumber={runNumber}/>
        </Col>
      </Row>
    </>
  )
}

export default Lumisection
