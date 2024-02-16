import React, { useState, useEffect } from 'react'

import Card from 'react-bootstrap/Card'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import paginationFactory from 'react-bootstrap-table2-paginator'
import { toast } from 'react-toastify'

import Table from '../../components/table'
import API from '../../services/api'
import dateFormat from '../../utils/date'

const IngestionTasks = () => {
  const [page, setPage] = useState(1)
  const [tasks, setTasks] = useState([])
  const [totalSize, setTotalSize] = useState()
  const [isLoading, setIsLoading] = useState(false)

  const tasksColumns = [
    { dataField: 'task_id', text: 'ID', type: 'string' },
    { dataField: 'status', text: 'Status', type: 'string' },
    { dataField: 'task_name', text: 'Task name', type: 'string' },
    { dataField: 'worker', text: 'Task worker', type: 'string' },
    { dataField: 'date_created', text: 'Date created', type: 'string' },
    { dataField: 'date_done', text: 'Date done', type: 'string' },
    { dataField: 'elapsed_time', text: 'Elapsed time', type: 'number' }
  ]
  const pagination = paginationFactory({ page, totalSize, hideSizePerPage: true, showTotal: true })
  const remote = { pagination: true, filter: false, sort: false }

  const handleTableChange = (type, { page }) => {
    if (type === 'pagination') {
      setPage(page)
    }
  }

  useEffect(() => {
    const fetchData = () => {
      setIsLoading(true)
      API.jobQueue.list({ page, status: ['STARTED'] })
        .then(response => {
          const result = response.results.map(item => {
            return {
              ...item,
              date_created: dateFormat(item.date_created, 'dd.MM.yyyy HH:mm:ss'),
              date_done: dateFormat(item.date_done, 'dd.MM.yyyy HH:mm:ss')
            }
          })
          setTasks(result)
          setTotalSize(response.count)
          setIsLoading(false)
        })
        .catch(err => {
          console.error(err)
          toast.error('Failure to communicate with the API!')
        })
    }

    fetchData()
  }, [page])

  return (
    <Row className='mb-3'>
      <Col sm={12}>
        <Card className='text-center'>
          <Card.Header>Job Queue</Card.Header>
          <Card.Body>
            <Table
              keyField='task_id'
              isLoading={isLoading}
              data={tasks}
              columns={tasksColumns}
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

export default IngestionTasks
