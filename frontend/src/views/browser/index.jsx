import React, { useState, useEffect } from 'react'

import { toast } from 'react-toastify'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Select from 'react-select'

import { TreeGrid } from './tree'
import API from '../../services/api'
import { buildTree } from '../../utils/ops'

const Browser = () => {
  const [isLoadingDatasets, setIsLoadingDatasets] = useState(true)
  const [datasets, setDatasets] = useState()
  const [selectedDataset, setSelectedDataset] = useState()

  const [isLoadingRuns, setIsLoadingRuns] = useState(true)
  const [runs, setRuns] = useState()
  const [selectedRun, setSelectedRun] = useState()

  const [isLoadingLumisections, setIsLoadingLumisections] = useState(true)
  const [lumisections, setLumisections] = useState()
  const [selectedLumisection, setSelectedLumisection] = useState()

  const [isLoadingMEs, setIsLoadingMEs] = useState(true)
  const [fullTree, setFullTree] = useState([])

  useEffect(() => {
    const fetchDatasets = () => {
      setIsLoadingDatasets(true)
      API.utils
        .genericFetchAllPages({ apiMethod: API.dataset.list })
        .then((response) => {
          const datasets = response.results
            .sort((a, b) =>
              a.dataset < b.dataset ? 1 : b.dataset < a.dataset ? -1 : 0
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
      API.utils
        .genericFetchAllPages({
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

  useEffect(() => {
    const fetchLumisections = ({ datasetId, runNumber }) => {
      setIsLoadingLumisections(true)
      API.utils
        .genericFetchAllPages({
          apiMethod: API.lumisection.list,
          params: { datasetId, runNumber },
        })
        .then((response) => {
          const lumisections = response.results
            .sort((a, b) =>
              a.ls_number > b.ls_number ? 1 : b.ls_number > a.ls_number ? -1 : 0
            )
            .map((item) => ({ value: item.ls_number, label: item.ls_number }))
          setLumisections(lumisections)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
        .finally(() => {
          setIsLoadingLumisections(false)
        })
    }

    const fetchMEs = ({ datasetId, runNumber }) => {
      setIsLoadingMEs(true)
      API.mes
        .listByRun({ datasetId, runNumber })
        .then((data) => {
          setFullTree(buildTree(data))
        })
        .catch((err) => {
          console.error(err)
          toast.error('Failure to communicate with the API!')
        })
        .finally(() => {
          setIsLoadingMEs(false)
        })
    }

    if (selectedDataset !== undefined && selectedRun !== undefined) {
      fetchMEs({
        datasetId: selectedDataset.value,
        runNumber: selectedRun.value,
      })
      fetchLumisections({
        datasetId: selectedDataset.value,
        runNumber: selectedRun.value,
      })
    }
  }, [selectedDataset, selectedRun])

  const handlePrevious = () => {
    const currentIndex = lumisections.findIndex(
      (option) => option.value === selectedLumisection.value
    )
    if (currentIndex > 0) {
      setSelectedLumisection(lumisections[currentIndex - 1])
    }
  }

  const handleNext = () => {
    const currentIndex = lumisections.findIndex(
      (option) => option.value === selectedLumisection.value
    )
    if (currentIndex < lumisections.length - 1) {
      setSelectedLumisection(lumisections[currentIndex + 1])
    }
  }

  return (
    <Container fluid>
      <Row className='mt-3 mb-3 m-3'>
        <Col md={4}>
          <Form.Group controlId='formDatasetSelector'>
            <Select
              value={selectedDataset}
              onChange={(selectedOptions) => {
                setSelectedDataset(selectedOptions)
              }}
              placeholder='Select a dataset...'
              options={datasets}
              isDisabled={isLoadingDatasets}
            />
          </Form.Group>
        </Col>
        <Col md={3}>
          <Form.Group controlId='formRunSelector'>
            <Select
              value={selectedRun}
              onChange={(selectedOptions) => {
                setSelectedRun(selectedOptions)
              }}
              placeholder='Select a run...'
              options={runs}
              isDisabled={isLoadingRuns}
            />
          </Form.Group>
        </Col>
        <Col md={3}>
          <Form.Group controlId='formLumisectionSelector'>
            <Select
              value={selectedLumisection}
              onChange={(selectedOptions) => {
                setSelectedLumisection(selectedOptions)
              }}
              placeholder='Select a lumisection...'
              options={lumisections}
              isDisabled={isLoadingLumisections}
            />
          </Form.Group>
        </Col>
        <Col md={2}>
          <Button
            variant='primary'
            disabled={selectedLumisection === undefined}
            onClick={handlePrevious}
            className='me-2'
          >
            Previous
          </Button>
          <Button
            variant='primary'
            disabled={selectedLumisection === undefined}
            onClick={handleNext}
          >
            Next
          </Button>
        </Col>
      </Row>
      <hr />
      <Row className='mt-3 mb-3 m-3'>
        {!isLoadingMEs && selectedLumisection !== undefined && (
          <TreeGrid
            fullTree={fullTree}
            datasetId={selectedDataset.value}
            runNumber={selectedRun.value}
            lsNumber={selectedLumisection.value}
          />
        )}
      </Row>
    </Container>
  )
}

export default Browser
