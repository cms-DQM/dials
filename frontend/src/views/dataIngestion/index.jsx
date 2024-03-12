import React from 'react'
import Container from 'react-bootstrap/Container'

import IngestionStatistics from './stats'
import IngestionTasks from './tasks'

const DataIngestion = () => {
  return (
    <Container>
      <IngestionStatistics />
      <IngestionTasks />
    </Container>
  )
}

export default DataIngestion
