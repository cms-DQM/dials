import React from 'react';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';

import LatestTasksCard from "./latestTasks";
import PendingTasksCard from "./pendingTasks";

const DataIngestion = () => {
  return (
    <Container>
      <Row className="px-4 my-5">
        <Col sm={8}>
          <LatestTasksCard />
        </Col>
        <Col sm={4}>
          <PendingTasksCard />
        </Col>
      </Row>
    </Container>
  )
}

export default DataIngestion;