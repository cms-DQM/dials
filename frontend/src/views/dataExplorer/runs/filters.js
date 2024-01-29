import React, { useState } from 'react';

import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

const RunsFilter = () => {
  const [minRun, setMinRun] = useState();
  const [maxRun, setMaxRun] = useState();

  const handleClick = () => { }

  return (
    <Card>
      <Card.Header className="text-center" as='h4'>Filters</Card.Header>
      <Card.Body>
        <Form.Group className="mb-3" controlId="formMinRun">
          <Form.Label>Run Range</Form.Label>
          <Row>
            <Col xs={6}>
              <Form.Control
                type="number"
                value={minRun}
                placeholder='Min'
                onChange={e => setMinRun(e.target.value)}
              />
            </Col>
            <Col xs={6}>
              <Form.Control
                type="number"
                value={maxRun}
                placeholder='Max'
                onChange={e => setMaxRun(e.target.value)}
              />
            </Col>
          </Row>
        </Form.Group>

        <Button
          variant="primary"
          type="submit"
          onClick={handleClick}
        >
          Submit
        </Button>
      </Card.Body>
    </Card>
  )
};

export default RunsFilter;