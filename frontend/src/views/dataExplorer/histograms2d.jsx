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
import reverseCantorPairing from '../../utils/cantor'

const Histograms2D = () => {
  const [isLoading, setLoading] = useState(true)
  const [currentPage, setCurrentPage] = useState(1)
  const [minRun, setMinRun] = useState()
  const [maxRun, setMaxRun] = useState()
  const [minLs, setMinLs] = useState()
  const [maxLs, setMaxLs] = useState()
  const [titleContains, setTitleContains] = useState()
  const [minEntries, setMinEntries] = useState(0)
  const [campaign, setCampaign] = useState()
  const [dataset, setDataset] = useState()
  const [era, setEra] = useState()
  const [fileId, setFileId] = useState()
  const [data, setData] = useState([])
  const [totalSize, setTotalSize] = useState()

  const columns = [
    {
      dataField: 'run_number',
      text: 'Run',
      type: 'number',
      formatter: (cell, row) => {
        const linkTo = `/runs/${row.run_number}`
        return <Link to={linkTo}>{row.run_number}</Link>
      },
    },
    {
      dataField: 'ls_number',
      text: 'Lumisection',
      type: 'number',
      formatter: (cell, row) => {
        const linkTo = `/lumisections/${row.ls_id}`
        return <Link to={linkTo}>{row.ls_number}</Link>
      },
    },
    {
      dataField: 'title',
      text: 'Title',
      type: 'string',
      headerStyle: { 'min-width': '300px', 'word-break': 'break-all' },
      formatter: (cell, row) => {
        const linkTo = `/histograms-2d/${row.hist_id}`
        return <Link to={linkTo}>{row.title}</Link>
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
    minRun,
    maxRun,
    minLs,
    maxLs,
    titleContains,
    minEntries,
    era,
    campaign,
    dataset,
    fileId,
  }) => {
    setLoading(true)
    API.lumisection
      .listHistograms(2, {
        page,
        minRun,
        maxRun,
        minLs,
        maxLs,
        titleContains,
        minEntries: minEntries > 0 ? minEntries : undefined,
        era,
        campaign,
        dataset,
        fileId,
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
            ls_number: reverseCantorPairing(item.ls_id, item.run_number),
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

            <Form.Group className='mb-3' controlId='formLsRange'>
              <Form.Label>Lumisection Range</Form.Label>
              <Row>
                <Col xs={6}>
                  <Form.Control
                    type='number'
                    value={minLs}
                    placeholder='Min'
                    onChange={(e) => setMinLs(e.target.value)}
                  />
                </Col>
                <Col xs={6}>
                  <Form.Control
                    type='number'
                    value={maxLs}
                    placeholder='Max'
                    onChange={(e) => setMaxLs(e.target.value)}
                  />
                </Col>
              </Row>
            </Form.Group>

            <Form.Group className='mb-3' controlId='formTitleContains'>
              <Form.Label>Title contains</Form.Label>
              <Form.Control
                type='string'
                placeholder='Enter title substring'
                value={titleContains}
                onChange={(e) => setTitleContains(e.target.value)}
              />
            </Form.Group>

            <Form.Group className='mb-3' controlId='formMinEntries' as={Row}>
              <Form.Label>Minimum number of entries</Form.Label>
              <Col xs={3}>
                <Form.Control
                  type='number'
                  value={minEntries}
                  onChange={(e) => setMinEntries(e.target.value)}
                />
              </Col>
              <Col xs={9}>
                <RangeSlider
                  min={0}
                  max={100000}
                  value={minEntries}
                  onChange={(e) => setMinEntries(e.target.value)}
                />
              </Col>
            </Form.Group>

            <Form.Group className='mb-3' controlId='formCampaign'>
              <Form.Label>Campaign contains</Form.Label>
              <Form.Control
                type='string'
                placeholder='Enter campaign substring'
                value={campaign}
                onChange={(e) => setCampaign(e.target.value)}
              />
            </Form.Group>

            <Form.Group className='mb-3' controlId='formDataset'>
              <Form.Label>Dataset contains</Form.Label>
              <Form.Control
                type='string'
                placeholder='Enter dataset substring'
                value={dataset}
                onChange={(e) => setDataset(e.target.value)}
              />
            </Form.Group>

            <Form.Group className='mb-3' controlId='formEra'>
              <Form.Label>Era</Form.Label>
              <Form.Control
                type='string'
                placeholder='Enter era'
                value={era}
                onChange={(e) => setEra(e.target.value)}
              />
            </Form.Group>

            <Form.Group className='mb-3' controlId='formFileId'>
              <Form.Label>File ID</Form.Label>
              <Form.Control
                type='number'
                placeholder='Enter file id'
                value={fileId}
                onChange={(e) => setFileId(e.target.value)}
              />
            </Form.Group>

            <Button
              variant='primary'
              type='submit'
              onClick={() => {
                fetchData({
                  page: 1,
                  minRun,
                  maxRun,
                  minLs,
                  maxLs,
                  titleContains,
                  minEntries,
                  campaign,
                  dataset,
                  era,
                  fileId,
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
              keyField='id'
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
                    minRun,
                    maxRun,
                    minLs,
                    maxLs,
                    titleContains,
                    minEntries,
                    campaign,
                    dataset,
                    era,
                    fileId,
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
