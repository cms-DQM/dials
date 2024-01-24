import React, { useState } from 'react';

import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

const LumisectionsSearch = () => {
  const [lumisectionNumber, setLumisectionNumber] = useState();
  const [runNumber, setRunNumber] = useState();

  const handleClick = () => { }

  return (
    <Card>
      <Card.Header className="text-center"><h4>Search</h4></Card.Header>
      <Card.Body>
        <Form.Group className="mb-3" controlId="formRunNumber">
          <Form.Label>Lumisection Number</Form.Label>
          <Form.Control
            type="number"
            value={lumisectionNumber}
            onChange={e => setLumisectionNumber(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formRunNumber">
          <Form.Label>Run Number</Form.Label>
          <Form.Control
            type="number"
            value={runNumber}
            onChange={e => setRunNumber(e.target.value)}
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

export default LumisectionsSearch;