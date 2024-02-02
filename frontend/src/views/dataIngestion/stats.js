import React, { useState, useEffect } from 'react'

import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'

import Card from 'react-bootstrap/Card'
import ResponsivePlot from '../../components/responsivePlot'
import API from '../../services/api'

const IngestionStatistics = () => {
  const [totalFiles, setTotalFiles] = useState(0)
  const [totalRuns, setTotalRuns] = useState(0)
  const [totalLumisections, setTOtalLumisection] = useState(0)
  const [dataFilesPlot, setDataFilesPlot] = useState([])
  const [dataH1DPlot, setDataH1DPlot] = useState([])
  const [dataH2DPlot, setDataH2DPlot] = useState([])
  const [layoutH1DPlot, setLayoutH1DPlot] = useState({})
  const [layoutH2DPlot, setLayoutH2DPlot] = useState({})

  useEffect(() => {
    const handleCountTotals = () => {
      API.fileIndex.list({}).then(response => setTotalFiles(response.count))
      API.lumisection.list({}).then(response => setTOtalLumisection(response.count))
      API.run.list({}).then(response => setTotalRuns(response.count))
    }

    const handleFilesPlot = async () => {
      const data = await Promise.all(API.fileIndex.statusList.map(async item => {
        const data = await API.fileIndex.list({ status: item })
        return {
          status: item,
          count: data.count
        }
      }))
      setDataFilesPlot([
        {
          y: data.map(item => item.count),
          x: data.map(item => item.status),
          type: 'bar',
          text: data.map(item => item.count)
        }
      ])
    }

    const handleH1DCounts = async () => {
      const data = await API.lumisection.getSubsystemCount(1)
      setDataH1DPlot([
        {
          values: data.map(item => item.count),
          labels: data.map(item => item.subsystem),
          type: 'pie',
          textinfo: 'value+percent'
        }
      ])
      setLayoutH1DPlot({
        title: {
          text: `Total: ${data.map(item => item.count).reduce((partialSum, a) => partialSum + a, 0)}`
        }
      })
    }

    const handleH2DCounts = async () => {
      const data = await API.lumisection.getSubsystemCount(2)
      setDataH2DPlot([
        {
          values: data.map(item => item.count),
          labels: data.map(item => item.subsystem),
          type: 'pie',
          textinfo: 'value+percent'
        }
      ])
      setLayoutH2DPlot({
        title: {
          text: `Total: ${data.map(item => item.count).reduce((partialSum, a) => partialSum + a, 0)}`
        }
      })
    }

    handleCountTotals()
    handleFilesPlot()
    handleH1DCounts()
    handleH2DCounts()
  }, [])

  return (
    <>
      <Row className='mt-5 mb-3'>
        <Col sm={4}>
          <Card className='text-center'>
            <Card.Header>Files</Card.Header>
            <Card.Body><h1>{totalFiles}</h1></Card.Body>
          </Card>
        </Col>
        <Col sm={4}>
          <Card className='text-center'>
            <Card.Header>Runs</Card.Header>
            <Card.Body><h1>{totalRuns}</h1></Card.Body>
          </Card>
        </Col>
        <Col sm={4}>
          <Card className='text-center'>
            <Card.Header>Lumisections</Card.Header>
            <Card.Body><h1>{totalLumisections}</h1></Card.Body>
          </Card>
        </Col>
      </Row >

      <Row className='mb-3'>
        <Col>
          <Card className='text-center'>
            <Card.Header>Indexed files by status</Card.Header>
            <Card.Body>
              <ResponsivePlot
                data={dataFilesPlot}
                config={{ staticPlot: true }}
              />
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className='mb-3'>
        <Col sm={6}>
          <Card className='text-center'>
            <Card.Header>1D Histograms by subsystem</Card.Header>
            <Card.Body>
              <ResponsivePlot
                data={dataH1DPlot}
                layout={layoutH1DPlot}
                config={{ staticPlot: true }}
              />
            </Card.Body>
          </Card>
        </Col>
        <Col sm={6}>
          <Card className='text-center'>
            <Card.Header>2D Histograms by subsystem</Card.Header>
            <Card.Body>
              <ResponsivePlot
                data={dataH2DPlot}
                layout={layoutH2DPlot}
                config={{ staticPlot: true }}
              />
            </Card.Body>
          </Card>
        </Col>
      </Row >
    </>
  )
}

export default IngestionStatistics
