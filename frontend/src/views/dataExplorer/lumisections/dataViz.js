import React, { useState, useEffect } from 'react'

import Card from 'react-bootstrap/Card'
import paginationFactory from 'react-bootstrap-table2-paginator'

import Table from '../../../components/table'
import { getLumisectionsByPage } from '../../../services/api'

const LumisectionsViz = () => {
  const [page, setPage] = useState(1)
  const [data, setData] = useState([])
  const [totalSize, setTotalSize] = useState()
  const [isLoading, setLoading] = useState(true)

  const columns = [
    { dataField: 'ls_number', text: 'Lumisection', type: 'number' },
    { dataField: 'run', text: 'Run', type: 'number' },
    { dataField: 'oms_zerobias_rate', text: 'OMS ZeroBias Rate', type: 'string' }
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
      getLumisectionsByPage(page)
        .then(response => {
          setData(response.results)
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
      <Card.Header as='h4'>Lumisections</Card.Header>
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

export default LumisectionsViz
