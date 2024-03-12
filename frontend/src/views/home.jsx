import React from 'react'

import Image from 'react-bootstrap/Image'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Card from 'react-bootstrap/Card'

import logo from '../assets/img/logo.png'

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
              <h3>DIALS: Data Inspector for Anomalous Lumi-Sections</h3>
              <br />
              {`
              During a Run, the CMS Experiment collects particle collision data in Lumisection time-frame and the experiment
              subsystem health is monitored by shifters using DQMGUI. Multiple shifters for many subsystems monitor the most
              recent lumisection of the current run plots to check a subsystem\'s health, but given the number of plots and
              the limited manpower it is not possible to closely pay attention to all plots during the lumisection time-frame.
              On the other hand, using certified data it is possible to extract knowledge from old runs (at lumisection-level) to
              help shifters get a glimpse of detector\'s health on past runs.
              `}
              <br />
              <br />
              {`
              DIALS is an application designed to be an access point to DQMIO per-LS monitoring elements.
              It is responsible for indexing, storing pre-processed DQMIO data and serving via a WEB UI and
              REST Api, so that it could be used by any CMS sub-group for exploratory analysis, statistical learning and machine learning.
              `}
              <br />
              <br />
              {`
              This application was born in CMS Tracker ML as a prototype under the name "MLPlayground" and
              was centralized in CMS DQM-DC to be a common access point for every system.
              `}
            </Card.Body>
          </Card>
        </Col>
      </Row>
    </Container>
  )
}

export default Home
