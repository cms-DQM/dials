import React from 'react';
import Container from 'react-bootstrap/Container';
import Carousel from 'react-bootstrap/Carousel';
import Image from 'react-bootstrap/Image';

import RawImg from '../assets/img/AnomalyDetection.jpg';
import AnomalyDetectedDogImg from '../assets/img/AnomalyDetectionDog.jpg';
import AnomalyDetectedPonyImg from '../assets/img/AnomalyDetectionPony.jpg';
import AnomalyDetectedPersonImg from '../assets/img/AnomalyDetectionPerson.jpg';
import AnomalyDetectedHiggsImg from '../assets/img/AnomalyDetectionHiggs.jpg';

const Home = () => {
  return (
    <Container>
      <Carousel fade controls={false} indicators={false} pause={false} interval={3000}>
        <Carousel.Item>
          <Image src={RawImg} className="d-block pt-5 img-fluid mx-auto w-100" alt="Raw object"></Image>
        </Carousel.Item>
        <Carousel.Item>
          <Image src={AnomalyDetectedDogImg} className="d-block pt-5 img-fluid mx-auto w-100" alt="Dog anomaly detected!"></Image>
        </Carousel.Item>
        <Carousel.Item>
          <Image src={AnomalyDetectedPonyImg} className="d-block pt-5 img-fluid mx-auto w-100" alt="Pony anomaly detected!"></Image>
        </Carousel.Item>
        <Carousel.Item>
          <Image src={AnomalyDetectedPersonImg} className="d-block pt-5 img-fluid mx-auto w-100" alt="Person anomaly detected!"></Image>
        </Carousel.Item>
        <Carousel.Item>
          <Image src={AnomalyDetectedHiggsImg} className="d-block pt-5 img-fluid mx-auto w-100" alt="Higgs anomaly detected!"></Image>
        </Carousel.Item>
      </Carousel>
    </Container>
  )
};

export default Home;