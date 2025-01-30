import React, { useState, useEffect } from 'react'

import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Card from 'react-bootstrap/Card'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import Select from 'react-select'
import { Link } from 'react-router-dom'
import { toast } from 'react-toastify'

import API from '../../services/api'
import { getNextToken } from '../../utils'
import Table from '../components/table'

const Predictions = () => {
  const defaultPageSize = 500

  const [isLoadingDatasets, setIsLoadingDatasets] = useState(false)
  const [datasets, setDatasets] = useState()
  const [selectedDatasets, setSelectedDatasets] = useState()

  const [isLoadingRuns, setIsLoadingRuns] = useState(false)
  const [runs, setRuns] = useState()
  const [selectedRuns, setSelectedRuns] = useState([])

  const [isLoadingModels, setIsLoadingModels] = useState(false)
  const [models, setModels] = useState()
  const [selectedModels, setSelectedModels] = useState([])

  const [isLoadingData, setIsLoadingData] = useState(false)
  const [flaggedBadLumis, setFlaggedBadLumis] = useState()
  const [nextToken, setNextToken] = useState(null)
  const [previousToken, setPreviousToken] = useState(null)

  const columns = [
    { dataField: 'filename', text: 'Model', type: 'string' },
    {
      dataField: 'run_number',
      text: 'Run',
      type: 'number',
      formatter: (cell, row) => {
        const linkTo = `/runs/${row.dataset_id}/${row.run_number}`
        return <Link to={linkTo}>{row.run_number}</Link>
      },
    },
    {
      dataField: 'ls_number',
      text: 'Lumisection',
      type: 'number',
      formatter: (cell, row) => {
        const linkTo = `/lumisections/${row.dataset_id}/${row.run_number}/${row.ls_number}`
        return <Link to={linkTo}>{row.ls_number}</Link>
      },
    },
    {
      dataField: 'me',
      text: 'ME',
      type: 'string',
      headerStyle: { 'min-width': '300px', 'word-break': 'break-all' },
      formatter: (cell, row) => {
        const linkTo = `/histograms-${row.dim}d/${row.dataset_id}/${row.run_number}/${row.ls_number}/${row.me_id}`
        return <Link to={linkTo}>{row.me}</Link>
      },
    },
    {
      dataField: 'mse',
      text: 'MSE',
      type: 'number',
    },
  ]

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
          params: {
            pageSize: defaultPageSize,
            datasetIdIn: selectedDatasets.map((item) => item.value),
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

    const fetchModels = () => {
      setIsLoadingModels(true)
      API.utils
        .genericFetchAllPages({
          apiMethod: API.mlModelsIndex.list,
          params: {
            pageSize: defaultPageSize,
            fields: ['model_id', 'filename', 'target_me'],
          },
        })
        .then((response) => {
          const models = response.results.map((item) => ({
            value: item.model_id,
            label: item.filename,
            targetMe: item.target_me,
          }))
          setModels(models)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
        .finally(() => {
          setIsLoadingModels(false)
        })
    }

    if (selectedDatasets !== undefined) {
      fetchRuns()
      fetchModels()
    }
  }, [selectedDatasets])

  const fetchFlaggedBadLumis = ({
    nextToken,
    datasetIdIn,
    runNumberIn,
    modelIdIn,
  }) => {
    setIsLoadingData(true)
    API.mlBadLumis
      .list({
        pageSize: defaultPageSize,
        nextToken,
        datasetIdIn,
        runNumberIn,
        modelIdIn,
      })
      .then((response) => {
        API.mes
          .list({})
          .then((mesResponse) => {
            const results = response.results.map((item) => {
              const model = models.find(
                (regModel) => regModel.value === item.model_id
              )
              const me = mesResponse.find((regMe) => regMe.me_id === item.me_id)
              return {
                ...item,
                filename: model.label,
                me: model.targetMe,
                dim: me.dim,
                keyField: `${item.model_id}_${item.dataset_id}_${item.file_id}_${item.run_number}_${item.ls_number}_${item.me_id}`,
              }
            })
            const nextToken = getNextToken(response, 'next')
            const previousToken = getNextToken(response, 'previous')
            setNextToken(nextToken)
            setPreviousToken(previousToken)
            setFlaggedBadLumis(results)
          })
          .catch((error) => {
            console.error(error)
            toast.error('Failure to communicate with the API!')
          })
      })
      .catch((error) => {
        console.error(error)
        toast.error('Failure to communicate with the API!')
      })
      .finally(() => {
        setIsLoadingData(false)
      })
  }

  const handleJsonDownload = async ({
    apiMethod,
    fileName,
    datasetIdIn,
    runNumberIn,
    modelIdIn,
  }) => {
    try {
      const response = await apiMethod({
        datasetIdIn,
        runNumberIn,
        modelIdIn,
      })

      // Create a Blob from the JSON data
      const blob = new Blob([JSON.stringify(response)], {
        type: 'application/json',
      })

      // Create a URL for the Blob
      const url = URL.createObjectURL(blob)

      // Create a link element and simulate a click to download the file
      const link = document.createElement('a')
      link.href = url
      link.download = fileName
      document.body.appendChild(link)
      link.click()

      // Clean up by revoking the object URL and removing the link
      URL.revokeObjectURL(url)
      document.body.removeChild(link)
    } catch (error) {
      console.error('Error downloading JSON:', error)
    }
  }

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
                isMulti
                value={selectedDatasets}
                onChange={(selectedOptions) => {
                  setSelectedDatasets(selectedOptions)
                }}
                options={datasets}
                isDisabled={isLoadingDatasets}
              />
            </Form.Group>

            {selectedDatasets && (
              <Form.Group className='mb-3' controlId='formRunsSelector'>
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

            {selectedDatasets && (
              <Form.Group className='mb-3' controlId='formModelsSelector'>
                <Form.Label>Registered models</Form.Label>
                <Select
                  isMulti
                  value={selectedModels}
                  onChange={(selectedOptions) => {
                    setSelectedModels(selectedOptions)
                  }}
                  options={models}
                  isDisabled={isLoadingModels}
                />
              </Form.Group>
            )}

            <Button
              variant='primary'
              type='submit'
              onClick={() => {
                fetchFlaggedBadLumis({
                  datasetIdIn: selectedDatasets.map((item) => item.value),
                  runNumberIn: selectedRuns.map((item) => item.value),
                  modelIdIn: selectedModels.map((item) => item.value),
                })
              }}
            >
              Submit
            </Button>
          </Card.Body>
        </Card>
      </Col>
      <Col sm={9}>
        <Card className='text-center'>
          <Card.Header as='h4'>Predictions</Card.Header>
          <Card.Body>
            {flaggedBadLumis ? (
              <>
                <Button
                  variant='primary'
                  type='submit'
                  onClick={() => {
                    handleJsonDownload({
                      apiMethod: API.mlBadLumis.certJson,
                      fileName: 'mlCertJson.json',
                      datasetIdIn: selectedDatasets.map((item) => item.value),
                      runNumberIn: selectedRuns.map((item) => item.value),
                      modelIdIn: selectedModels.map((item) => item.value),
                    })
                  }}
                >
                  Download certification json
                </Button>
                <Button
                  variant='primary'
                  type='submit'
                  onClick={() => {
                    handleJsonDownload({
                      apiMethod: API.mlBadLumis.goldenJson,
                      fileName: 'mlGoldenJson.json',
                      datasetIdIn: selectedDatasets.map((item) => item.value),
                      runNumberIn: selectedRuns.map((item) => item.value),
                      modelIdIn: selectedModels.map((item) => item.value),
                    })
                  }}
                >
                  Download golden json
                </Button>
                <Table
                  keyField='keyField'
                  isLoading={isLoadingData}
                  data={flaggedBadLumis}
                  columns={columns}
                  bordered={false}
                  hover={true}
                  remote
                  cursorPagination={true}
                  previousToken={previousToken}
                  nextToken={nextToken}
                  previousOnClick={() => {
                    fetchFlaggedBadLumis({
                      nextToken: previousToken,
                      datasetIdIn: selectedDatasets.map((item) => item.value),
                      runNumberIn: selectedRuns.map((item) => item.value),
                      modelIdIn: selectedModels.map((item) => item.value),
                    })
                  }}
                  nextOnClick={() => {
                    fetchFlaggedBadLumis({
                      nextToken,
                      datasetIdIn: selectedDatasets.map((item) => item.value),
                      runNumberIn: selectedRuns.map((item) => item.value),
                      modelIdIn: selectedModels.map((item) => item.value),
                    })
                  }}
                />
              </>
            ) : (
              <p>Waiting for inputs...</p>
            )}
          </Card.Body>
        </Card>
      </Col>
    </Row>
  )
}

export default Predictions
