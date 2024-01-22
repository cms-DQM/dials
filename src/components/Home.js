import React from 'react';
import Container from 'react-bootstrap/Container';
import Carousel from 'react-bootstrap/Carousel';

import RawImg from '../assets/img/AnomalyDetection.jpg';
import AnomalyDetectedImg from '../assets/img/AnomalyDetectionV2.jpg';

const Home = () => {
  return (
    <Container>
      <Carousel fade controls={false} indicators={false} pause={false} interval={1000}>
        <Carousel.Item>
          <img
            src={RawImg}
            className="d-block pt-5 img-fluid mx-auto w-100"
            alt="Raw object"
          />
        </Carousel.Item>
        <Carousel.Item>
          <img
            src={AnomalyDetectedImg}
            className="d-block pt-5 img-fluid mx-auto w-100"
            alt="Anomaly detected!"
          />
        </Carousel.Item>
      </Carousel>
    </Container>
  )
};

export default Home;