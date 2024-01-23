import React, { useState } from 'react';

import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import RangeSlider from 'react-bootstrap-range-slider';

const Histograms1DFilter = () => {
  const [titleContains, setTitleContains] = useState();
  const [lumisectionId, setLumisectionId] = useState();
  const [minEntries, setMinEntries] = useState(0);

  const handleClick = () => { }

  return (
    <Card>
      <Card.Header className="text-center"><h4>Filter</h4></Card.Header>
      <Card.Body>
        <Form.Group className="mb-3" controlId="formTitleContains">
          <Form.Label>Title contains</Form.Label>
          <Form.Control
            type="string"
            placeholder="Enter title substring"
            value={titleContains}
            onChange={e => setTitleContains(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formLumisectionId">
          <Form.Label>Lumisection Id</Form.Label>
          <Form.Control
            type="string"
            placeholder="Enter lumisection id"
            value={lumisectionId}
            onChange={e => setLumisectionId(e.target.value)}
          />
        </Form.Group>

        <Form.Group className="mb-3" controlId="formMinEntries" as={Row}>
          <Form.Label>Minimum number of entries</Form.Label>
          <Col xs={3}>
            <Form.Control
              type="number"
              value={minEntries}
              onChange={e => setMinEntries(e.target.value)}
            />
          </Col>
          <Col xs={9}>
            <RangeSlider
              min={0}
              max={100000}
              value={minEntries}
              onChange={e => setMinEntries(e.target.value)}
            />
          </Col>
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

export default Histograms1DFilter;