import React, { useState, useEffect } from 'react'

import Card from 'react-bootstrap/Card'
import paginationFactory from 'react-bootstrap-table2-paginator'

import Table from '../../../components/table'
import ResponsivePlot from '../../../components/responsivePlot'
import { getHistograms1DByPage } from '../../../services/api'

const Histograms1DViz = () => {
  const [page, setPage] = useState(1)
  const [data, setData] = useState([])
  const [totalSize, setTotalSize] = useState()
  const [isLoading, setLoading] = useState(true)

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
      getHistograms1DByPage(page)
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
  }, [page])

  return (
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
  )
}

export default Histograms1DViz
