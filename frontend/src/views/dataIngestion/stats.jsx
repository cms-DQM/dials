import React, { useState, useEffect } from 'react'

import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import { toast } from 'react-toastify'

import Card from 'react-bootstrap/Card'
import { ResponsivePlot } from '../components'
import API from '../../services/api'

const groupBySplitME = (data) => {
  const groupedData = data.reduce((acc, item) => {
    const [firstPart, secondPart] = item.me.split('/')
    const key = `${firstPart}/${secondPart.split('/')[0]}`

    if (!acc[key]) {
      acc[key] = {
        me: key,
        count: item.count,
      }
    } else {
      acc[key].count += item.count
    }

    return acc
  }, {})

  return Object.values(groupedData)
}

const IngestionStatistics = () => {
  const [totalFiles, setTotalFiles] = useState(0)
  const [totalRuns, setTotalRuns] = useState(0)
  const [totalLumisections, setTotalLumisection] = useState(0)
  const [dataFilesPlot, setDataFilesPlot] = useState([])
  const [dataH1DPlot, setDataH1DPlot] = useState([])
  const [dataH2DPlot, setDataH2DPlot] = useState([])
  const [layoutFilesPlot, setLayoutFilesPlot] = useState({})
  const [layoutH1DPlot, setLayoutH1DPlot] = useState({})
  const [layoutH2DPlot, setLayoutH2DPlot] = useState({})

  const [isLoadingFiles, setIsLoadingFiles] = useState(true)
  const [isLoadingH1D, setIsLoadingH1D] = useState(true)
  const [isLoadingH2D, setIsLoadingH2D] = useState(true)

  useEffect(() => {
    const fetchTotalIndexedFiles = () => {
      API.fileIndex
        .count({})
        .then((response) => {
          setTotalFiles(response.count)
        })
        .catch((err) => {
          console.error(err)
          toast.error('Failure to communicate with the API!')
        })
    }

    const fetchTotalIngestedRuns = () => {
      API.run
        .count({})
        .then((response) => {
          setTotalRuns(response.count)
        })
        .catch((err) => {
          console.error(err)
          toast.error('Failure to communicate with the API!')
        })
    }

    const fetchTotalIngestedLumis = () => {
      API.lumisection
        .count({})
        .then((response) => {
          setTotalLumisection(response.count)
        })
        .catch((err) => {
          console.error(err)
          toast.error('Failure to communicate with the API!')
        })
    }

    const fatchStatusData = async () => {
      setIsLoadingFiles(true)
      try {
        const data = await Promise.all(
          API.fileIndex.statusList.map(async (item) => {
            const data = await API.fileIndex.count({ status: item })
            return {
              status: item,
              count: data.count,
            }
          })
        )
        const plotData = [
          {
            y: data.map((item) => item.count),
            x: data.map((item) => item.status),
            type: 'bar',
            text: data.map((item) => item.count),
            textposition: 'outside',
          },
        ]
        const maxY = Math.max(...data.map((item) => item.count))
        const yMaxRange = maxY * 1.1
        const layout = {
          yaxis: {
            range: [0, yMaxRange],
          },
        }
        setDataFilesPlot(plotData)
        setLayoutFilesPlot(layout)
        setIsLoadingFiles(false)
      } catch (err) {
        console.error(err)
        toast.error('Failure to communicate with the API!')
      }
    }

    const fetchH1DCount = () => {
      setIsLoadingH1D(true)
      API.mes
        .list({ dim: 1 })
        .then((data) => {
          const groupedData = groupBySplitME(data)
          setDataH1DPlot([
            {
              values: groupedData.map((item) => item.count),
              labels: groupedData.map((item) => item.me),
              type: 'pie',
              textinfo: 'value+percent',
            },
          ])
          setLayoutH1DPlot({
            title: {
              text: `Total: ${groupedData.map((item) => item.count).reduce((partialSum, a) => partialSum + a, 0)}`,
            },
          })
          setIsLoadingH1D(false)
        })
        .catch((err) => {
          console.error(err)
          toast.error('Failure to communicate with the API!')
        })
    }

    const fetchH2DCount = () => {
      setIsLoadingH2D(true)
      API.mes
        .list({ dim: 2 })
        .then((data) => {
          const groupedData = groupBySplitME(data)
          setDataH2DPlot([
            {
              values: groupedData.map((item) => item.count),
              labels: groupedData.map((item) => item.me),
              type: 'pie',
              textinfo: 'value+percent',
            },
          ])
          setLayoutH2DPlot({
            title: {
              text: `Total: ${groupedData.map((item) => item.count).reduce((partialSum, a) => partialSum + a, 0)}`,
            },
          })
          setIsLoadingH2D(false)
        })
        .catch((err) => {
          console.error(err)
          toast.error('Failure to communicate with the API!')
        })
    }

    fetchTotalIndexedFiles()
    fetchTotalIngestedRuns()
    fetchTotalIngestedLumis()
    fatchStatusData()
    fetchH1DCount()
    fetchH2DCount()
  }, [])

  return (
    <>
      <Row className='mt-5 mb-3'>
        <Col sm={4}>
          <Card className='text-center'>
            <Card.Header>Files</Card.Header>
            <Card.Body>
              <h1>{totalFiles}</h1>
            </Card.Body>
          </Card>
        </Col>
        <Col sm={4}>
          <Card className='text-center'>
            <Card.Header>Runs</Card.Header>
            <Card.Body>
              <h1>{totalRuns}</h1>
            </Card.Body>
          </Card>
        </Col>
        <Col sm={4}>
          <Card className='text-center'>
            <Card.Header>Lumisections</Card.Header>
            <Card.Body>
              <h1>{totalLumisections}</h1>
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className='mb-3'>
        <Col sm={6}>
          <Card className='text-center'>
            <Card.Header>Ingested 1D MEs</Card.Header>
            <Card.Body>
              <ResponsivePlot
                data={dataH1DPlot}
                layout={layoutH1DPlot}
                config={{ staticPlot: true }}
                isLoading={isLoadingH1D}
                style={{ width: '100%', height: '100%' }}
              />
            </Card.Body>
          </Card>
        </Col>
        <Col sm={6}>
          <Card className='text-center'>
            <Card.Header>Ingested 2D MEs</Card.Header>
            <Card.Body>
              <ResponsivePlot
                data={dataH2DPlot}
                layout={layoutH2DPlot}
                config={{ staticPlot: true }}
                isLoading={isLoadingH2D}
                style={{ width: '100%', height: '100%' }}
              />
            </Card.Body>
          </Card>
        </Col>
      </Row>

      <Row className='mb-3'>
        <Col>
          <Card className='text-center'>
            <Card.Header>Indexed files by status</Card.Header>
            <Card.Body>
              <ResponsivePlot
                data={dataFilesPlot}
                layout={layoutFilesPlot}
                config={{ staticPlot: true }}
                isLoading={isLoadingFiles}
                style={{ width: '100%', height: '100%' }}
              />
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </>
  )
}

export default IngestionStatistics
