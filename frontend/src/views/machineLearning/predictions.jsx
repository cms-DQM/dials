import React, { useState, useEffect } from 'react'

import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Card from 'react-bootstrap/Card'
import Form from 'react-bootstrap/Form'
import Select from 'react-select'
import { toast } from 'react-toastify'

import API from '../../services/api'
import { getNextToken } from '../../utils/sanitizer'

const Predictions = () => {
  const [isLoadingDatasets, setIsLoadingDatasets] = useState(false)
  const [datasets, setDatasets] = useState()
  const [selectedDataset, setSelectedDataset] = useState()

  const [isLoadingRuns, setIsLoadingRuns] = useState(false)
  const [runs, setRuns] = useState()
  const [selectedRuns, setSelectedRuns] = useState([])

  const genericFetchAllPages = async ({ apiMethod, params = {} }) => {
    const allData = []
    let nextPageExists = true
    let nextToken = null
    let errorCount = 0
    let totalPages = 0
    while (nextPageExists) {
      totalPages++
      try {
        const { results, next } = await apiMethod({
          nextToken,
          ...params,
        })
        results.forEach((e) => allData.unshift(e))
        nextPageExists = !(next === null)
        nextToken = getNextToken({ next }, 'next')
      } catch (err) {
        errorCount++
      }
    }

    return {
      results: allData,
      count: allData.length,
      error: errorCount,
      totalPages,
    }
  }

  useEffect(() => {
    const fetchDatasets = () => {
      setIsLoadingDatasets(true)
      genericFetchAllPages({ apiMethod: API.dataset.list })
        .then((response) => {
          const datasets = response.results
            .sort((a, b) =>
              a.dataset > b.dataset ? 1 : b.dataset > a.dataset ? -1 : 0
            )
            .map((item) => ({ value: item.dataset_id, label: item.dataset }))
          setDatasets(datasets)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
        .finally(() => {
          setIsLoadingDatasets(false)
        })
    }

    fetchDatasets()
  }, [])

  useEffect(() => {
    const fetchRuns = () => {
      setIsLoadingRuns(true)
      genericFetchAllPages({
        apiMethod: API.run.list,
        params: { datasetId: selectedDataset.value },
      })
        .then((response) => {
          const runs = response.results.map((item) => ({
            value: item.run_number,
            label: item.run_number,
          }))
          setRuns(runs)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
        .finally(() => {
          setIsLoadingRuns(false)
        })
    }

    if (selectedDataset !== undefined) {
      fetchRuns()
    }
  }, [selectedDataset])

  return (
    <Row className='mt-5 mb-3 m-3'>
      <Col sm={3}>
        <Card>
          <Card.Header className='text-center' as='h4'>
            Filters
          </Card.Header>
          <Card.Body>
            <Form.Group className='mb-3' controlId='formDatasetSelector'>
              <Form.Label>Dataset</Form.Label>
              <Select
                value={selectedDataset}
                onChange={(selectedOptions) => {
                  setSelectedDataset(selectedOptions)
                }}
                options={datasets}
                isDisabled={isLoadingDatasets}
              />
            </Form.Group>

            {selectedDataset && (
              <Form.Group className='mb-3' controlId='formRunSelector'>
                <Form.Label>Run numbers</Form.Label>
                <Select
                  isMulti
                  value={selectedRuns}
                  onChange={(selectedOptions) => {
                    setSelectedRuns(selectedOptions)
                  }}
                  options={runs}
                  isDisabled={isLoadingRuns}
                />
              </Form.Group>
            )}
          </Card.Body>
        </Card>
      </Col>
      <Col sm={9}>
        <Card className='text-center'>
          <Card.Header as='h4'>Predictions</Card.Header>
          <Card.Body>Hello World</Card.Body>
        </Card>
      </Col>
    </Row>
  )
}

export default Predictions
