import React, { useState, useEffect } from 'react'

import { Link } from 'react-router-dom'
import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Card from 'react-bootstrap/Card'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import RangeSlider from 'react-bootstrap-range-slider'
import paginationFactory from 'react-bootstrap-table2-paginator'
import { toast } from 'react-toastify'

import { ResponsivePlot, Table } from '../../components'
import API from '../../services/api'

const Histograms2D = () => {
  const [isLoading, setLoading] = useState(true)

  // Filters
  const [currentPage, setCurrentPage] = useState(1)
  const [dataset, setDataset] = useState()
  const [datasetRegex, setDatasetRegex] = useState()
  const [logicalFileName, setLogicalFileName] = useState()
  const [logicalFileNameRegex, setLogicalFileNameRegex] = useState()
  const [runNumber, setRunNumber] = useState()
  const [runNumberLte, setRunNumberLte] = useState()
  const [runNumberGte, setRunNumberGte] = useState()
  const [lsNumber, setLsNumber] = useState()
  const [lsNumberLte, setLsNumberNumberLte] = useState()
  const [lsNumberGte, setLsNumberNumberGte] = useState()
  const [me, setMe] = useState()
  const [meRegex, setMeRegex] = useState()
  const [entriesGte, setEntriesGte] = useState(0)

  // API results
  const [data, setData] = useState([])
  const [totalSize, setTotalSize] = useState()

  const columns = [
    {
      dataField: 'dataset_id',
      text: 'Dataset Id',
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
      dataField: 'me_id',
      text: 'ME Id',
      type: 'string',
      headerStyle: { 'min-width': '300px', 'word-break': 'break-all' },
      formatter: (cell, row) => {
        const linkTo = `/histograms-2d/${row.hist_id}`
        return <Link to={linkTo}>{row.me_id}</Link>
      },
    },
    { dataField: 'entries', text: 'Entries', type: 'number' },
    {
      dataField: 'plot',
      text: 'Plot',
      formatter: (cell, row) => {
        const linkTo = `/histograms-2d/${row.hist_id}`
        return <Link to={linkTo}>{cell}</Link>
      },
    },
  ]

  const fetchData = ({
    page,
    runNumber,
    runNumberLte,
    runNumberGte,
    lsNumber,
    lsNumberLte,
    lsNumberGte,
    entriesGte,
    dataset,
    datasetRegex,
    logicalFileName,
    logicalFileNameRegex,
    me,
    meRegex,
  }) => {
    setLoading(true)
    API.histogram
      .list(2, {
        page,
        runNumber,
        runNumberLte,
        runNumberGte,
        lsNumber,
        lsNumberLte,
        lsNumberGte,
        entriesGte: entriesGte > 0 ? entriesGte : undefined,
        dataset,
        datasetRegex,
        logicalFileName,
        logicalFileNameRegex,
        me,
        meRegex,
      })
      .then((response) => {
        const results = response.results.map((item) => {
          const data = [
            { z: item.data, type: 'heatmap', colorscale: 'Viridis' },
          ]
          const layout = {
            margin: { t: 10, b: 10, l: 10, r: 10 },
            yaxis: { visible: false },
            xaxis: { visible: false },
            bargap: 0,
            paper_bgcolor: 'rgba(0,0,0,0)',
            plot_bgcolor: 'rgba(0,0,0,0)',
          }
          return {
            ...item,
            plot: (
              <ResponsivePlot
                data={data}
                layout={layout}
                config={{ staticPlot: true }}
                boxWidth={'200pt'}
                boxHeight={'100pt'}
              />
            ),
          }
        })
        setData(results)
        setTotalSize(response.count)
        setCurrentPage(page)
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
    fetchData({ page: 1 })
  }, [])

  return (
    <Row className='mt-5 mb-3 m-3'>
      <Col sm={3}>
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

            <Form.Group className='mb-3' controlId='formLogicalFileName'>
              <Form.Label>Logical file name</Form.Label>
              <Form.Control
                type='string'
                placeholder='Enter logical file name'
                value={logicalFileName}
                onChange={(e) => setLogicalFileName(e.target.value)}
              />
            </Form.Group>

            <Form.Group className='mb-3' controlId='formLogicalFileNameRegex'>
              <Form.Label>Logical file name regex</Form.Label>
              <Form.Control
                type='string'
                placeholder='Enter logical file name regex'
                value={logicalFileNameRegex}
                onChange={(e) => setLogicalFileNameRegex(e.target.value)}
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

            <Form.Group className='mb-3' controlId='formMe'>
              <Form.Label>Monitoring element</Form.Label>
              <Form.Control
                type='string'
                placeholder='Enter monitoring element'
                value={me}
                onChange={(e) => setMe(e.target.value)}
              />
            </Form.Group>

            <Form.Group className='mb-3' controlId='formMeRegex'>
              <Form.Label>Monitoring element regex</Form.Label>
              <Form.Control
                type='string'
                placeholder='Enter monitoring element regex'
                value={meRegex}
                onChange={(e) => setMeRegex(e.target.value)}
              />
            </Form.Group>

            <Form.Group className='mb-3' controlId='formEntriesGte' as={Row}>
              <Form.Label>Minimum number of entries</Form.Label>
              <Col xs={3}>
                <Form.Control
                  type='number'
                  value={entriesGte}
                  onChange={(e) => setEntriesGte(e.target.value)}
                />
              </Col>
              <Col xs={9}>
                <RangeSlider
                  min={0}
                  max={100000}
                  value={entriesGte}
                  onChange={(e) => setEntriesGte(e.target.value)}
                />
              </Col>
            </Form.Group>

            <Button
              variant='primary'
              type='submit'
              onClick={() => {
                fetchData({
                  page: 1,
                  runNumber,
                  runNumberLte,
                  runNumberGte,
                  lsNumber,
                  lsNumberLte,
                  lsNumberGte,
                  entriesGte,
                  dataset,
                  datasetRegex,
                  logicalFileName,
                  logicalFileNameRegex,
                  me,
                  meRegex,
                })
              }}
            >
              Submit
            </Button>
          </Card.Body>
        </Card>
      </Col>
      <Col sm={9}>
        <Card className='text-center'>
          <Card.Header as='h4'>
            Luminosity-granularity 2D histograms
          </Card.Header>
          <Card.Body>
            <Table
              keyField='hist_id'
              isLoading={isLoading}
              data={data}
              columns={columns}
              bordered={false}
              hover={true}
              remote
              onTableChange={(type, { page }) => {
                if (type === 'pagination') {
                  fetchData({
                    page,
                    runNumber,
                    runNumberLte,
                    runNumberGte,
                    lsNumber,
                    lsNumberLte,
                    lsNumberGte,
                    entriesGte,
                    dataset,
                    datasetRegex,
                    logicalFileName,
                    logicalFileNameRegex,
                    me,
                    meRegex,
                  })
                }
              }}
              pagination={paginationFactory({
                totalSize,
                page: currentPage,
                hideSizePerPage: true,
                showTotal: true,
              })}
            />
          </Card.Body>
        </Card>
      </Col>
    </Row>
  )
}

export default Histograms2D
