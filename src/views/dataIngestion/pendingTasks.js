import React, { useState, useEffect } from 'react';

import Card from 'react-bootstrap/Card';
import Spinner from 'react-bootstrap/Spinner';
import BootstrapTable from 'react-bootstrap-table-next';
import paginationFactory from 'react-bootstrap-table2-paginator';

import { getPendingTasks } from '../../services/api';

const PendingTasksCard = () => {
  const [pendingTasks, setPendingTasks] = useState([]);
  const [isLoadingTasks, setLoadingTasks] = useState(true);

  const tasksColumns = [
    { dataField: "id", text: "ID", type: "string" },
    { dataField: "queue", text: "Queue", type: "string" }
  ]

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
        {
          isLoadingTasks ? (
            <Spinner animation="border" role="status" />
          ) : (
            <>
              <Card.Text>Entries are updated each 30 seconds</Card.Text>
              <BootstrapTable
                keyField='id'
                data={pendingTasks}
                columns={tasksColumns}
                bordered={false}
                pagination={
                  paginationFactory({sizePerPage: 5, paginationSize: 2, hideSizePerPage: true})
                }
              />
            </>
          )
        }
      </Card.Body>
    </Card>
  )
};

export default PendingTasksCard;