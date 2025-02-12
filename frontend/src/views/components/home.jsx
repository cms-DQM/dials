import React from 'react'

import { Link } from 'react-router-dom'
import Image from 'react-bootstrap/Image'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Card from 'react-bootstrap/Card'

import logo from '../../assets/img/logo.png'

const Home = () => {
  return (
    <Container>
      <Row className='mt-5 mb-3 align-items-center'>
        <Col md={4} className='text-center'>
          <Image src={logo} alt='' />
        </Col>
        <Col md={8}>
          <Card>
            <Card.Body>
              <h3><strong>DIALS</strong>: <strong>D</strong>ata <strong>I</strong>nspector for <strong>A</strong>nomalous <strong>L</strong>umi-<strong>S</strong>ections</h3>
              <br />
              {`
              DIALS is an application that serves as a gateway to DQM per-LS monitoring elements.
              Its primary functions include indexing and storing pre-processed DQMIO data,
              as well as lumisections flagged as anomalous by pre-trained machine learning models.
              Conveniently, data is served through this web UI and a dedicated REST API.
              `}
              <br />
              <hr/>
              <h4>Quick Links</h4>
              <ul>
                <li><Link to='/runs'>Runs</Link>: explore the available data given a known run.</li>
                <li><Link to='/browser'>Browser</Link>: Interactively explore the data, starting from a dataset.</li>
                <li><Link to='/json-portal'>JSON Portal</Link>: Generate a Golden+DCS+ML JSON for data still awaiting certification during data taking.</li>
                <li><Link to='/predictions'>Predictions</Link>: Check lumisections flagged as anomalous by one or many ML models.</li>
                <li>
                  <a
                    href='https://github.com/cms-DQM/dials-py'
                    target='_blank'
                    rel='noopener noreferrer'
                  >dials-py</a>: The Python api client interface to DIALS service.
                </li>
              </ul>
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default Home
