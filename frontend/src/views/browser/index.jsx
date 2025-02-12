import React, { useState, useEffect } from 'react'

import { useSearchParams } from 'react-router-dom'
import { toast } from 'react-toastify'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Select from 'react-select'

import API from '../../services/api'
import { buildTree } from './utils'
import TreeGrid from './tree'

const Browser = () => {
  const defaultPageSize = 500

  const [searchParams, setSearchParams] = useSearchParams()
  const initialDatasetId = searchParams.get('dataset')
    ? Number(searchParams.get('dataset'))
    : null
  const initialRun = searchParams.get('run')
    ? Number(searchParams.get('run'))
    : null
  const initialLumisection = searchParams.get('lumi')
    ? Number(searchParams.get('lumi'))
    : null
  const initialTreePath = searchParams.get('path')
    ? searchParams.get('path').split('/')
    : []

  // Populate dropdowns
  const [isLoadingDatasets, setIsLoadingDatasets] = useState(true)
  const [isLoadingRuns, setIsLoadingRuns] = useState(true)
  const [isLoadingLumisections, setIsLoadingLumisections] = useState(true)
  const [datasets, setDatasets] = useState()
  const [runs, setRuns] = useState()
  const [lumisections, setLumisections] = useState()

  // User-selected parameters
  const [selectedDataset, setSelectedDataset] = useState(null)
  const [selectedRun, setSelectedRun] = useState(
    initialRun ? { value: initialRun, label: initialRun } : null
  )
  const [selectedLumisection, setSelectedLumisection] = useState(
    initialLumisection
      ? { value: initialLumisection, label: initialLumisection }
      : null
  )

  // Populate browser
  const [isLoadingMEs, setIsLoadingMEs] = useState(true)
  const [fullTree, setFullTree] = useState([])

  useEffect(() => {
    const fetchDatasets = () => {
      setIsLoadingDatasets(true)
      API.utils
        .genericFetchAllPages({
          apiMethod: API.dataset.list,
          params: {
            pageSize: defaultPageSize,
            fields: ['dataset_id', 'dataset'],
          },
        })
        .then((response) => {
          const datasets = response.results
            .sort((a, b) =>
              a.dataset < b.dataset ? 1 : b.dataset < a.dataset ? -1 : 0
            )
            .map((item) => ({ value: item.dataset_id, label: item.dataset }))
          setDatasets(datasets)

          // Set initial dataset if URL contains a dataset ID
          if (initialDatasetId) {
            const initialDataset = datasets.find(
              (d) => d.value === initialDatasetId
            )
            if (initialDataset) {
              setSelectedDataset(initialDataset)
            }
          }
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
  }, [initialDatasetId])

  useEffect(() => {
    if (!selectedDataset) return

    const fetchRuns = () => {
      setIsLoadingRuns(true)
      API.utils
        .genericFetchAllPages({
          apiMethod: API.run.list,
          params: {
            datasetId: selectedDataset.value,
            pageSize: defaultPageSize,
            fields: ['run_number'],
          },
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

    fetchRuns()
  }, [selectedDataset])

  useEffect(() => {
    if (!selectedDataset || !selectedRun) return

    const fetchLumisections = ({ datasetId, runNumber }) => {
      setIsLoadingLumisections(true)
      API.utils
        .genericFetchAllPages({
          apiMethod: API.lumisection.list,
          params: {
            datasetId,
            runNumber,
            pageSize: defaultPageSize,
            fields: ['ls_number'],
          },
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

    fetchMEs({
      datasetId: selectedDataset.value,
      runNumber: selectedRun.value,
    })
    fetchLumisections({
      datasetId: selectedDataset.value,
      runNumber: selectedRun.value,
    })
  }, [selectedDataset, selectedRun])

  const handleDatasetChange = (selectedOptions) => {
    setSelectedDataset(selectedOptions)
    setRuns([])
    setSelectedRun(null)
    setLumisections([])
    setSelectedLumisection(null)
    searchParams.set('dataset', selectedOptions.value)
    searchParams.delete('run')
    searchParams.delete('lumi')
    setSearchParams(searchParams)
  }

  const handleRunChange = (selectedOptions) => {
    setSelectedRun(selectedOptions)
    setLumisections([])
    setSelectedLumisection(null)
    searchParams.set('run', selectedOptions.value)
    searchParams.delete('lumi')
    setSearchParams(searchParams)
  }

  const handleLumisectionChange = (selectedOptions) => {
    setSelectedLumisection(selectedOptions)
    searchParams.set('lumi', selectedOptions.value)
    setSearchParams(searchParams)
  }

  const handlePrevious = () => {
    const currentIndex = lumisections.findIndex(
      (option) => option.value === selectedLumisection.value
    )
    if (currentIndex > 0) {
      const prevLumi = lumisections[currentIndex - 1]
      setSelectedLumisection(prevLumi)
      searchParams.set('lumi', prevLumi.value)
      setSearchParams(searchParams)
    }
  }

  const handleNext = () => {
    const currentIndex = lumisections.findIndex(
      (option) => option.value === selectedLumisection.value
    )
    if (currentIndex < lumisections.length - 1) {
      const nextLumi = lumisections[currentIndex + 1]
      setSelectedLumisection(nextLumi)
      searchParams.set('lumi', nextLumi.value)
      setSearchParams(searchParams)
    }
  }

  return (
    <Container fluid>
      <Row className='mt-3 mb-3 m-3'>
        <Col md={4}>
          <Form.Group controlId='formDatasetSelector'>
            <Select
              value={selectedDataset}
              onChange={handleDatasetChange}
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
              onChange={handleRunChange}
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
              onChange={handleLumisectionChange}
              placeholder='Select a lumisection...'
              options={lumisections}
              isDisabled={isLoadingLumisections}
            />
          </Form.Group>
        </Col>
        <Col md={2}>
          <Button
            variant='primary'
            disabled={!selectedLumisection}
            onClick={handlePrevious}
            className='me-2'
          >
            Previous
          </Button>
          <Button
            variant='primary'
            disabled={!selectedLumisection}
            onClick={handleNext}
          >
            Next
          </Button>
        </Col>
      </Row>
      <hr />
      <Row className='mt-3 mb-3 m-3'>
        {!isLoadingMEs && selectedLumisection && (
          <TreeGrid
            fullTree={fullTree}
            initialPath={initialTreePath}
            datasetId={selectedDataset.value}
            runNumber={selectedRun.value}
            lsNumber={selectedLumisection.value}
            onChange={(currentPath) => {
              if (currentPath) {
                const path = currentPath.join('/')
                searchParams.set('path', path)
              } else {
                searchParams.delete('path')
              }
              setSearchParams(searchParams)
            }}
          />
        )}
      </Row>
    </Container>
  )
}

export default Browser
