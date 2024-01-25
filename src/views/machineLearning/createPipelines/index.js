import React, { useState } from 'react';

import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Card from 'react-bootstrap/Card';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';
import axios from 'axios';

import isGithubUrl from '../../../utils/githubUrl'

const CreatePipelines = () => {
  const [pipelineName, setPipelineName] = useState('');
  const [repoUrl, setRepoUrl] = useState(null);
  const [isRepoUrlValid, setIsRepoUrlValid] = useState(false);
  const [isRepoUrlInvalid, setIsRepoUrlInvalid] = useState(false);

  const getRepositoryContent = async () => {
    const username = repoUrl.split('/')[3];
    const repoName = repoUrl.split('/')[4];
    const contentsUrl = `https://api.github.com/repos/${username}/${repoName}/contents`;
    let repoExists = null;
    let data = null;
    
    try {
      const response = await axios.get(contentsUrl);
      repoExists = true;
      data = response.data;
    } catch(err) {
      repoExists = false;
    }

    return { data: data, repoExists: repoExists }
  }

  const validateRepoUrl = async () => {
    let isValid = null;
    let isInvalid = null;

    if (repoUrl === "" || repoUrl === null) {
      isValid = false;
      isInvalid = false;
    } else if (isGithubUrl(repoUrl, { repository: true })) {
      const { repoExists } = await getRepositoryContent()
      isValid = repoExists ? true : false;
      isInvalid = !isValid;
    } else {
      isValid = false;
      isInvalid = !isValid;
    }

    setIsRepoUrlValid(isValid)
    setIsRepoUrlInvalid(isInvalid)
  }

  const handleSubmit = async () => {
    validateRepoUrl()
  }

  return (
    <Container>

      <Row className="mt-5 mb-3">
        <Col sm={3}></Col>
        <Col sm={6} className='align-self-center'>
          <Card>
            <Card.Header as="h4" className='text-center'>Pipeline creation</Card.Header>
            <Card.Body>

              <Form.Label>Set a name to your pipeline</Form.Label>
              <Form.Control
                type='string'
                value={pipelineName}
                onChange={e => setPipelineName(e.target.value)}
              />

              <br />
              <Form.Label>GitHub repository url</Form.Label>
              <Form.Control
                type='string'
                value={repoUrl}
                onChange={e => setRepoUrl(e.target.value)}
                isValid={isRepoUrlValid}
                isInvalid={isRepoUrlInvalid}
              />
              <Form.Control.Feedback type="valid"></Form.Control.Feedback>
              <Form.Control.Feedback type="invalid">Please input a valid repository url</Form.Control.Feedback>

              <br />
              <Button onClick={handleSubmit}>Submit</Button>

            </Card.Body>
          </Card>
        </Col>
        <Col sm={3}></Col>
      </Row>

    </Container>
  )
}

export default CreatePipelines;