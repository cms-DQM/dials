import React, { useState, useEffect } from 'react';

import Card from 'react-bootstrap/Card';
import Spinner from 'react-bootstrap/Spinner';
import BootstrapTable from 'react-bootstrap-table-next';

import { getLatestTasks } from '../../services/api';

const LatestTasksCard = () => {
  const [latestTasks, setLatestTasks] = useState([]);
  const [isLoadingTasks, setLoadingTasks] = useState(true);

  const tasksColumns = [
    { dataField: "task_id", text: "ID", type: "string" },
    { dataField: "status", text: "Status", type: "string" },
    { dataField: "date_created", text: "Date started", type: "string" },
    { dataField: "elapsed_time", text: "Elapsed time", type: "number" }
  ]

  const handleLatestTasks = () => {
    setLoadingTasks(true)
    getLatestTasks()
      .then(tasks => {
        setLatestTasks(tasks)
      })
      .catch(error => {
        console.error(error)
      })
      .finally(() => {
        setLoadingTasks(false)
      })
  }

  useEffect(() => {
    handleLatestTasks()
    const interval = setInterval(() => handleLatestTasks(), 30000)
    return () => {
      clearInterval(interval);
    }

  }, [])

  return (
    <Card className="text-center">
      <Card.Header><h4>Latest tasks in queues</h4></Card.Header>
      <Card.Body>
        {
          isLoadingTasks ? (
            <Spinner animation="border" role="status" />
          ) : (
            <>
              <Card.Text>Entries are updated each 30 seconds</Card.Text>
              <BootstrapTable keyField='id' data={latestTasks} columns={tasksColumns} bordered={false} />
            </>
          )
        }
      </Card.Body>
    </Card>
  )
};

export default LatestTasksCard;