import React, { useState, useEffect } from 'react';

import Card from 'react-bootstrap/Card';
import paginationFactory from 'react-bootstrap-table2-paginator';

import Table from '../../components/table';
import { getPendingTasks } from '../../services/api';

const PendingTasksCard = () => {
  const [pendingTasks, setPendingTasks] = useState([]);
  const [isLoadingTasks, setLoadingTasks] = useState(true);

  const tasksColumns = [
    { dataField: "id", text: "ID", type: "string" },
    { dataField: "queue", text: "Queue", type: "string" }
  ]
  const pagination = paginationFactory({ sizePerPage: 5, paginationSize: 2, hideSizePerPage: true })

  const handlePendingTasks = () => {
    setLoadingTasks(true)
    getPendingTasks()
      .then(tasks => {
        setPendingTasks(tasks)
      })
      .catch(error => {
        console.error(error)
      })
      .finally(() => {
        setLoadingTasks(false)
      })
  }

  useEffect(() => {
    handlePendingTasks()
    const interval = setInterval(() => handlePendingTasks(), 30000)
    return () => {
      clearInterval(interval);
    }

  }, [])

  return (
    <Card className="text-center">
      <Card.Header><h4>Pending tasks in queues</h4></Card.Header>
      <Card.Body>
        <Table
          keyField='id'
          isLoading={isLoadingTasks}
          data={pendingTasks}
          columns={tasksColumns}
          bordered={false}
          hover={true}
          pagination={pagination}
        />
      </Card.Body>
    </Card>
  )
};

export default PendingTasksCard;