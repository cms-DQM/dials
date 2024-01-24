import React from 'react';

import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import Card from 'react-bootstrap/Card';
import ResponsivePlot from '../../components/responsivePlot';

const IngestionStatistics = () => {

  const totalFiles = 13548
  const totalRuns = 56
  const totalLumisections = 1235

  const indexedFilesByStatus = [
    { "label": "INDEXED", "count": 7500 },
    { "label": "PENDING", "count": 5000 },
    { "label": "RUNNING", "count": 1 },
    { "label": "OK", "count": 847 },
    { "label": "FAILED", "count": 200 }
  ]
  const dataFilesPlot = [
    { 
      y: indexedFilesByStatus.map(item => item.count),
      x: indexedFilesByStatus.map(item => item.label),
      type: 'bar',
      text: indexedFilesByStatus.map(item => item.count)
    }
  ]

  const ingestedH1DBySubsytem = [
    { "subsytem": "EcalBarrel", "count": 1386 },
    { "subsytem": "EcalEndcap", "count": 1406 },
    { "subsytem": "HLT", "count": 1376 },
    { "subsytem": "JetMET", "count": 32038 },
    { "subsytem": "OfflinePV", "count": 5464 },
    { "subsytem": "PixelPhase1", "count": 32904 },
    { "subsytem": "SiStrip", "count": 97076 },
    { "subsytem": "Tracking", "count": 5464 }
  ]
  const dataH1DPlot = [
    {
      values: ingestedH1DBySubsytem.map(item => item.count),
      labels: ingestedH1DBySubsytem.map(item => item.subsytem),
      type: 'pie',
      textinfo: 'value+percent'
    }
  ]
  const layoutH1DPlot = {
    title: {
      text: `Total: ${ingestedH1DBySubsytem.map(item => item.count).reduce((partialSum, a) => partialSum + a, 0)}`
    }
  }

  const ingestedH2DBySubsytem = [
    { "subsytem": "EcalEndcap", "count": 396 },
    { "subsytem": "JetMET", "count": 10 },
    { "subsytem": "PixelPhase1", "count": 2068 },
    { "subsytem": "EcalBarrel", "count": 558 },
    { "subsytem": "Hcal", "count": 3008 },
  ]
  const dataH2DPlot = [
    {
      values: ingestedH2DBySubsytem.map(item => item.count),
      labels: ingestedH2DBySubsytem.map(item => item.subsytem),
      type: 'pie',
      textinfo: 'value+percent'
    }
  ]
  const layoutH2DPlot = {
    title: {
      text: `Total: ${ingestedH2DBySubsytem.map(item => item.count).reduce((partialSum, a) => partialSum + a, 0)}`
    }
  }

  return (
    <>
      <Row className="px-4 my-5">
        <Col sm={4}>
          <Card className="text-center">
            <Card.Header>Files</Card.Header>
            <Card.Body><h1>{totalFiles}</h1></Card.Body>
          </Card>
        </Col>
        <Col sm={4}>
          <Card className="text-center">
            <Card.Header>Runs</Card.Header>
            <Card.Body><h1>{totalRuns}</h1></Card.Body>
          </Card>
        </Col>
        <Col sm={4}>
          <Card className="text-center">
            <Card.Header>Lumisections</Card.Header>
            <Card.Body><h1>{totalLumisections}</h1></Card.Body>
          </Card>
        </Col>
      </Row >

      <Row className="px-4 my-5">
        <Col>
          <Card className="text-center">
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

      <Row className="px-4 my-5">
        <Col sm={6}>
          <Card className="text-center">
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
          <Card className="text-center">
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

export default IngestionStatistics;