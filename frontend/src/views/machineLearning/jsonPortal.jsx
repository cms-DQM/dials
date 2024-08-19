import React, { useEffect, useState } from 'react'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Form from 'react-bootstrap/Form'
import AceEditor from 'react-ace'
import { toast } from 'react-toastify'

import 'ace-builds/src-noconflict/mode-java'
import 'ace-builds/src-noconflict/theme-github'
import 'ace-builds/src-noconflict/ext-language_tools'

import API from '../../services/api'
import { listToRange, rangeToList } from '../../utils/goldenJson'

const JsonPortal = () => {
  const currentYear = new Date().getFullYear()
  const datasetRegex = `/.*/Run${currentYear}.*-PromptReco.*/DQMIO`
  const rrClassName = `Collisions${currentYear.toString().slice(2)}`
  const rrDatasetName = `/PromptReco/Collisions${currentYear}/DQM`

  const [mergeDCSAndML, setMergeDCSAndML] = useState(true)
  const [activeModels, setActiveModels] = useState()
  const [datasetIds, setDatasetIds] = useState()
  const [rrOpenRuns, setRROpenRuns] = useState()
  const [goldenJson, setGoldenJson] = useState()
  const [dcsJson, setDCSJson] = useState()
  const [mlGoldenJson, setMLGoldenJson] = useState()

  useEffect(() => {
    const fetchRROpenRuns = () => {
      API.runregistry
        .getOpenRuns({ className: rrClassName, datasetName: rrDatasetName })
        .then((response) => {
          setRROpenRuns(response)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
    }

    const fetchCAFJson = ({ kind, setStateCallback }) => {
      API.caf
        .get({ className: rrClassName, kind })
        .then((response) => {
          setStateCallback(response)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
    }

    const fetchModels = () => {
      API.utils
        .genericFetchAllPages({
          apiMethod: API.mlModelsIndex.list,
          params: { active: true },
        })
        .then((response) => {
          setActiveModels(response.results)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
    }

    const fetchDatasetIds = () => {
      API.utils
        .genericFetchAllPages({
          apiMethod: API.dataset.list,
          params: { datasetRegex },
        })
        .then((response) => {
          setDatasetIds(response.results.map((item) => item.dataset_id))
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
    }

    fetchRROpenRuns()
    fetchCAFJson({ kind: 'golden', setStateCallback: setGoldenJson })
    fetchCAFJson({ kind: 'dcs', setStateCallback: setDCSJson })
    fetchModels()
    fetchDatasetIds()
  }, [datasetRegex, rrClassName, rrDatasetName])

  useEffect(() => {
    const fetchMLJson = () => {
      API.mlBadLumis
        .goldenJson({
          datasetIdIn: datasetIds,
          runNumberIn: rrOpenRuns,
          modelIdIn: activeModels.map((item) => item.model_id),
        })
        .then((response) => {
          setMLGoldenJson(response)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
    }

    if (
      datasetIds !== undefined &&
      activeModels !== undefined &&
      rrOpenRuns !== undefined
    ) {
      fetchMLJson()
    }
  }, [datasetIds, activeModels, rrOpenRuns])

  const triggerDownload = ({ filename, obj }) => {
    const blob = new Blob([JSON.stringify(obj)], {
      type: 'application/json',
    })
    const url = URL.createObjectURL(blob)

    // Create a link element and simulate a click to download the file
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()

    // Clean up by revoking the object URL and removing the link
    URL.revokeObjectURL(url)
    document.body.removeChild(link)
  }

  const mergeAndDownload = () => {
    let mergedJson
    if (mergeDCSAndML) {
      const expandedMLJson = Object.keys(mlGoldenJson).reduce((acc, key) => {
        acc[key] = rangeToList(mlGoldenJson[key])
        return acc
      }, {})
      const expandedDCSJson = Object.keys(dcsJson.content).reduce(
        (acc, key) => {
          acc[key] = rangeToList(dcsJson.content[key])
          return acc
        },
        {}
      )
      const filteredMLJson = Object.keys(expandedMLJson).reduce((acc, key) => {
        acc[key] = Object.keys(expandedDCSJson).includes(key)
          ? expandedMLJson[key].filter((value) =>
              expandedDCSJson[key].includes(value)
            )
          : expandedMLJson[key]
        return acc
      }, {})
      const compactMLJson = Object.keys(filteredMLJson).reduce((acc, key) => {
        acc[key] = [...listToRange(filteredMLJson[key])]
        return acc
      }, {})
      mergedJson = { ...goldenJson.content, ...compactMLJson }
    } else {
      mergedJson = { ...goldenJson.content, ...mlGoldenJson }
    }
    const minRun = Math.min(...Object.keys(mergedJson))
    const maxRun = Math.max(...Object.keys(mergedJson))
    const fileBaseName = mergeDCSAndML
      ? 'ml_dcs_golden_Merged'
      : 'ml_golden_Merged'
    const filename = `${fileBaseName}_Collisions${currentYear}_${minRun}_${maxRun}_Golden.json`
    triggerDownload({ filename, obj: mergedJson })
  }

  return (
    <Container fluid>
      <Row className='mt-3'>
        <Col md={5} />
        <Col md={2} className='text-center'>
          <Button
            variant='primary'
            type='submit'
            disabled={
              goldenJson === undefined ||
              dcsJson === undefined ||
              mlGoldenJson === undefined
            }
            onClick={mergeAndDownload}
          >
            Merge and download
          </Button>
        </Col>
        <Col md={5} />
      </Row>
      <Row className='mt-2'>
        <Col md={5} />
        <Col md={2} className='text-center'>
          <Card>
            <Card.Body>
              <Form>
                <Form.Check
                  defaultChecked={true}
                  type='checkbox'
                  label='Remove offline DCS bits from ML JSON'
                  value={mergeDCSAndML}
                  onChange={(e) => {
                    setMergeDCSAndML(e.target.checked)
                  }}
                />
              </Form>
            </Card.Body>
          </Card>
        </Col>
        <Col md={5} />
      </Row>
      <hr />
      <Row className='mt-3'>
        <Col md={4}>
          <div className='text-center'>
            <strong>
              <a
                href='#'
                onClick={() =>
                  triggerDownload({
                    filename: goldenJson.name,
                    obj: goldenJson.download,
                  })
                }
              >
                {goldenJson === undefined
                  ? 'Golden JSON'
                  : `${goldenJson.name} (generated at: ${goldenJson.last_modified})`}
              </a>
            </strong>
          </div>
          <div style={{ border: '3px solid #ddd', padding: '10px' }}>
            {goldenJson === undefined ? (
              <Spinner animation='border' role='status' />
            ) : (
              <AceEditor
                mode='javascript'
                theme='github'
                readOnly={true}
                height='50vh'
                width='100%'
                fontSize={15}
                wrapEnabled={true}
                value={JSON.stringify(goldenJson.content)}
              />
            )}
          </div>
        </Col>
        <Col md={4}>
          <div className='text-center'>
            <strong>
              <a
                href='#'
                onClick={() =>
                  triggerDownload({
                    filename: dcsJson.name,
                    obj: dcsJson.download,
                  })
                }
              >
                {dcsJson === undefined
                  ? 'DCS JSON'
                  : `${dcsJson.name} (generated at: ${dcsJson.last_modified})`}
              </a>
            </strong>
          </div>
          <div style={{ border: '3px solid #ddd', padding: '10px' }}>
            {dcsJson === undefined ? (
              <Spinner animation='border' role='status' />
            ) : (
              <AceEditor
                mode='javascript'
                theme='github'
                readOnly={true}
                height='50vh'
                width='100%'
                fontSize={15}
                wrapEnabled={true}
                value={JSON.stringify(dcsJson.content)}
              />
            )}
          </div>
        </Col>
        <Col md={4}>
          <div className='text-center'>
            <strong>
              <a
                href='#'
                onClick={() => {
                  const minRun = Math.min(...Object.keys(mlGoldenJson))
                  const maxRun = Math.max(...Object.keys(mlGoldenJson))
                  const filename = `mlOnly_Collisions${currentYear}_${minRun}_${maxRun}_Golden.json`
                  triggerDownload({ filename, obj: mlGoldenJson })
                }}
              >
                ML JSON
              </a>
            </strong>
          </div>
          <div style={{ border: '3px solid #ddd', padding: '10px' }}>
            {rrOpenRuns === undefined && (
              <div>
                <Spinner animation='border' role='status' />
                <span className='ms-1'>{`Fetching OPEN runs in Run Registry for (${rrClassName}, ${rrDatasetName})`}</span>
              </div>
            )}
            {activeModels === undefined && (
              <div>
                <Spinner animation='border' role='status' />
                <span className='ms-1'>Fetching the active ML models...</span>
              </div>
            )}
            {datasetIds === undefined && (
              <div>
                <Spinner animation='border' role='status' />
                <span className='ms-1'>{`Fetching data ids for pattern: ${datasetRegex}`}</span>
              </div>
            )}
            {mlGoldenJson === undefined ? (
              <div>
                <Spinner animation='border' role='status' />
                <span className='ms-1'>Generating the ML JSON</span>
              </div>
            ) : (
              <AceEditor
                mode='javascript'
                theme='github'
                readOnly={true}
                height='50vh'
                width='100%'
                fontSize={15}
                wrapEnabled={true}
                value={JSON.stringify(mlGoldenJson)}
              />
            )}
          </div>
        </Col>
      </Row>
    </Container>
  )
}

export default JsonPortal
