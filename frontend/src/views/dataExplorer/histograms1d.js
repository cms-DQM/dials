import React, { useState, useEffect } from 'react'

import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Card from 'react-bootstrap/Card'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import RangeSlider from 'react-bootstrap-range-slider'
import paginationFactory from 'react-bootstrap-table2-paginator'

import Table from '../../components/table'
import ResponsivePlot from '../../components/responsivePlot'
import API from '../../services/api'

const Histograms1D = () => {
  // Loading indicator and filter props
  const [isLoading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [titleContains, setTitleContains] = useState()
  const [lumisectionId, setLumisectionId] = useState()
  const [minEntries, setMinEntries] = useState(0)

  // Actual data after fetching
  const [data, setData] = useState([])
  const [totalSize, setTotalSize] = useState()

  // Boolean to trigger useEffect
  const [filterSubmited, setFilterSubmited] = useState(false)

  const columns = [
    { dataField: 'title', text: 'Title', type: 'string' },
    { dataField: 'entries', text: 'Entries', type: 'number' },
    { dataField: 'source_data_file', text: 'Source File Id', type: 'number' },
    { dataField: 'lumisection', text: 'Lumisection Id', type: 'number' },
    { dataField: 'plot', text: 'Plot' }
  ]
  const pagination = paginationFactory({ page, totalSize, hideSizePerPage: true })
  const remote = { pagination: true, filter: false, sort: false }

  const handleTableChange = (type, { page }) => {
    if (type === 'pagination') {
      setPage(page)
    }
  }

  useEffect(() => {
    const handleData = () => {
      setLoading(true)
      API.lumisection.getH1D({ page, titleContains, lumisectionId, minEntries })
        .then(response => {
          const results = response.results.map(item => {
            const data = [{ y: item.data, type: 'bar' }]
            const layout = {
              margin: { t: 10, b: 10, l: 10, r: 10 },
              yaxis: { visible: false },
              xaxis: { visible: false },
              bargap: 0,
              paper_bgcolor: 'rgba(0,0,0,0)',
              plot_bgcolor: 'rgba(0,0,0,0)'
            }
            return {
              ...item,
              plot: (
                <ResponsivePlot
                  data={data}
                  layout={layout}
                  config={{ staticPlot: true }}
                />
              )
            }
          })
          setData(results)
          setTotalSize(response.count)
        })
        .catch(error => {
          console.error(error)
        })
        .finally(() => {
          setLoading(false)
        })
    }
    handleData()
  }, [page, filterSubmited])

  return (
    <Row className='mt-5 mb-3 m-3'>
      <Col sm={3}>
      <Card>
      <Card.Header className='text-center' as='h4'>Filters</Card.Header>
      <Card.Body>
        <Form.Group className='mb-3' controlId='formTitleContains'>
          <Form.Label>Title contains</Form.Label>
          <Form.Control
            type='string'
            placeholder='Enter title substring'
            value={titleContains}
            onChange={e => setTitleContains(e.target.value)}
          />
        </Form.Group>

        <Form.Group className='mb-3' controlId='formLumisectionId'>
          <Form.Label>Lumisection Id</Form.Label>
          <Form.Control
            type='string'
            placeholder='Enter lumisection id'
            value={lumisectionId}
            onChange={e => setLumisectionId(e.target.value)}
          />
        </Form.Group>

        <Form.Group className='mb-3' controlId='formMinEntries' as={Row}>
          <Form.Label>Minimum number of entries</Form.Label>
          <Col xs={3}>
            <Form.Control
              type='number'
              value={minEntries}
              onChange={e => setMinEntries(e.target.value)}
            />
          </Col>
          <Col xs={9}>
            <RangeSlider
              min={0}
              max={100000}
              value={minEntries}
              onChange={e => setMinEntries(e.target.value)}
            />
          </Col>
        </Form.Group>

        <Button
          variant='primary'
          type='submit'
          onClick={() => {
            setPage(1)
            setFilterSubmited(!filterSubmited)
          }}
        >
          Submit
        </Button>
      </Card.Body>
    </Card>
      </Col>
      <Col sm={9}>
      <Card className='text-center'>
      <Card.Header as='h4'>Luminosity-granularity 1D histograms</Card.Header>
      <Card.Body>
        <Table
          keyField='file_path'
          isLoading={isLoading}
          data={data}
          columns={columns}
          bordered={false}
          hover={true}
          remote={remote}
          pagination={pagination}
          onTableChange={handleTableChange}
        />
      </Card.Body>
    </Card>
      </Col>
    </Row>
  )
}

export default Histograms1D
