import React, { useState } from 'react';

import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

const RunsFilter = () => {
  const [minRun, setMinRun] = useState();
  const [maxRun, setMaxRun] = useState();

  const handleClick = () => { }

  return (
    <Card>
      <Card.Header className="text-center"><h4>Filter</h4></Card.Header>
      <Card.Body>
        <Form.Group className="mb-3" controlId="formMinRun">
          <Form.Label>Minimum Run Number</Form.Label>
          <Form.Control
            type="number"
            value={minRun}
            onChange={e => setMinRun(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formMaxRun">
          <Form.Label>Maximum Run Number</Form.Label>
          <Form.Control
            type="number"
            value={maxRun}
            onChange={e => setMaxRun(e.target.value)}
          />
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