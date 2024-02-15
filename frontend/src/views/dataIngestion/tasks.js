import React, { useState, useEffect } from 'react'

import Card from 'react-bootstrap/Card'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import paginationFactory from 'react-bootstrap-table2-paginator'

import Table from '../../components/table'
import API from '../../services/api'
import dateFormat from '../../utils/date'

const IngestionTasks = () => {
  const [latestTasks, setLatestTasks] = useState([])
  const [pendingTasks, setPendingTasks] = useState([])
  const [isLoadingLatestTasks, setLoadingLatestTasks] = useState(true)
  const [isLoadingPedingTasks, setLoadingPendingTasks] = useState(true)

  const latestTasksColumns = [
    { dataField: 'task_id', text: 'ID', type: 'string' },
    { dataField: 'status', text: 'Status', type: 'string' },
    { dataField: 'date_created', text: 'Date started', type: 'string' },
    { dataField: 'elapsed_time', text: 'Elapsed time', type: 'number' }
  ]
  const pendingTasksColumns = [
    { dataField: 'id', text: 'ID', type: 'string' },
    { dataField: 'queue', text: 'Queue', type: 'string' }
  ]
  const pagination = paginationFactory({
    sizePerPage: 5, paginationSize: 2, hideSizePerPage: true
  })

  useEffect(() => {
    const handleTrackedTasks = async () => {
      const response = await API.jobQueue.tracked({})
      const result = response.results.slice(0, 5).map(item => {
        return { ...item, date_created: dateFormat(item.date_created, 'dd.MM.yyyy HH:mm:ss') }
      })
      setLatestTasks(result)
      setLoadingLatestTasks(false)
    }

    const handleEnqueuedTasks = async () => {
      const response = await API.jobQueue.enqueued()
      setPendingTasks(response)
      setLoadingPendingTasks(false)
    }

    handleTrackedTasks()
    handleEnqueuedTasks()
  }, [])

  return (
    <Row className='mb-3'>
      <Col sm={7}>
        <Card className='text-center'>
          <Card.Header>Latest tasks in queues</Card.Header>
          <Card.Body>
            <Table
              keyField='task_id'
              isLoading={isLoadingLatestTasks}
              data={latestTasks}
              columns={latestTasksColumns}
              bordered={false}
              hover={true}
            />
          </Card.Body>
        </Card>
      </Col>
      <Col sm={5}>
        <Card className='text-center'>
          <Card.Header>Pending tasks in queues</Card.Header>
          <Card.Body>
            <Table
              keyField='id'
              isLoading={isLoadingPedingTasks}
              data={pendingTasks}
              columns={pendingTasksColumns}
              bordered={false}
              hover={true}
              pagination={pagination}
            />
          </Card.Body>
        </Card>
      </Col>
    </Row>
  )
}

export default IngestionTasks
