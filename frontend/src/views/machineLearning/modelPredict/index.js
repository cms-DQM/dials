import React, { useState } from 'react';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

const ModelPredict = () => {
  const [modelName, setModelName] = useState(null);
  const [infra, setInfra] = useState(null);

  const availablePipelines = [
    'polarisationclassifier',
    'polarisation-classification',
    'inspire-classifier-pipeline-gpu-v2',
    'inspire-classifier-pipeline-gpu-v1',
    'inspire-classifier-pipeline-gpu',
    'test-job-salt',
    'jec-pipeline-particle-net-regressor-open-3be925'
  ]

  const availableInfrastructures = [
    'HTCondor',
    'OKD',
    'Kubeflow'
  ]

  return (
    <Container>

      <Row className="mt-5 mb-3">
        <Col sm={3}></Col>
        <Col sm={6} className='align-self-center'>
          <Card>
            <Card.Header as="h4" className='text-center'>Model predict</Card.Header>
            <Card.Body>

              <Form.Group className="mb-3">
                <Form.Label>Select a model</Form.Label>
                <Form.Select
                  default=''
                  value={modelName}
                  onChange={e => setModelName(e.target.value)}
                >
                  <option key='blankChoice' hidden value />
                  {
                    availablePipelines.map(item => {
                      return (<option value={item}>{item}</option>)
                    })
                  }
                </Form.Select>
              </Form.Group>

              <Form.Group className="mb-3">
                <Form.Label>Select a infrastructure</Form.Label>
                <Form.Select
                  default=''
                  value={infra}
                  onChange={e => setInfra(e.target.value)}
                >
                  <option key='blankChoice' hidden value />
                  {
                    availableInfrastructures.map(item => {
                      return (<option value={item}>{item}</option>)
                    })
                  }
                </Form.Select>
              </Form.Group>

              <Button>Submit</Button>

            </Card.Body>
          </Card>
        </Col>
        <Col sm={3}></Col>
      </Row>

    </Container>
  )
}

export default ModelPredict;