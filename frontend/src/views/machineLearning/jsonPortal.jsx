import React, { useEffect, useState } from 'react'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Spinner from 'react-bootstrap/Spinner'
import Button from 'react-bootstrap/Button'
import Card from 'react-bootstrap/Card'
import Form from 'react-bootstrap/Form'
import Alert from 'react-bootstrap/Alert'
import AceEditor from 'react-ace'
import { toast } from 'react-toastify'

import 'ace-builds/src-noconflict/mode-java'
import 'ace-builds/src-noconflict/theme-github'
import 'ace-builds/src-noconflict/ext-language_tools'

import API from '../../services/api'
import { listToRange, rangeToList } from '../../utils/goldenJson'

const JsonPortal = () => {
  const defaultPageSize = 500
  const currentYear = new Date().getFullYear()
  const datasetRegex = `/.*/Run${currentYear}.*-PromptReco.*/DQMIO`
  const rrClassName = `Collisions${currentYear.toString().slice(2)}`
  const rrDatasetName = `/PromptReco/Collisions${currentYear}/DQM`
  const rrGlobalState = 'OPEN'
  const brilBeamStatus = '"STABLE BEAMS"'
  const brilAModeTag = 'PROTPHYS'
  const brilNormTag =
    '/cvmfs/cms-bril.cern.ch/cms-lumi-pog/Normtags/normtag_BRIL.json'
  const brilConnect = 'web'
  const brilUnit = '/nb'
  const brilLowLumiRule = 80.0

  const [validWorkspaces, setValidWorkspaces] = useState()
  const [mergeDCSAndML, setMergeDCSAndML] = useState(true)
  const [activeModels, setActiveModels] = useState()
  const [datasetIds, setDatasetIds] = useState()
  const [rrOpenRuns, setRROpenRuns] = useState()
  const [brilRuns, setBrilRuns] = useState()
  const [goldenJson, setGoldenJson] = useState()
  const [dcsJson, setDCSJson] = useState()
  const [goldenJsonNotFound, setGoldenJsonNotFound] = useState(false)
  const [dcsJsonNotFound, setDCSJsonNotFound] = useState(false)
  const [mlGoldenJson, setMLGoldenJson] = useState()

  useEffect(() => {
    const fetchWorkspaces = async () => {
      API.config
        .getWorkspaces()
        .then((response) => {
          setValidWorkspaces(response.workspaces.filter(item => !item.includes('staging')))
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
    }

    fetchWorkspaces()
  }, [])

  useEffect(() => {
    const fetchModels = () => {
      const promises = validWorkspaces.map(async ws => {
        return API.utils
          .genericFetchAllPages({
            apiMethod: API.mlModelsIndex.list,
            params: { pageSize: defaultPageSize, active: true, workspace: ws },
          })
          .then((response) => {
            return {[ws]: response.results}
          })
      })

      Promise.all(promises)
        .then(response => {
          const mergedResponse = response.reduce((acc, obj) => {
            return {...acc, ...obj}
          }, {})
          const result = Object.entries(mergedResponse).reduce((acc, [ws, models]) => {
            return models.length !== 0 ? {...acc, [ws]: models} : acc
          }, {})
          setActiveModels(result)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
    }

    if (validWorkspaces !== undefined) {
      fetchModels()
    }
  }, [validWorkspaces])

  useEffect(() => {
    const fetchRROpenRuns = () => {
      API.runregistry.editableDatasets
        .list({
          className: rrClassName,
          datasetName: rrDatasetName,
          globalState: rrGlobalState,
        })
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
          if (error.response && error.response.status === 404) {
            if (kind === 'golden') {
              setGoldenJsonNotFound(true)
            } else if (kind === 'dcs') {
              setDCSJsonNotFound(true)
            }
            setStateCallback({})
          } else {
            console.error(error)
            toast.error('Failure to communicate with the API!')
          }
        })
    }

    const fetchDatasetIds = () => {
      const promises = Object.keys(activeModels).map(async ws => {
        return API.utils
          .genericFetchAllPages({
            apiMethod: API.dataset.list,
            params: { pageSize: defaultPageSize, datasetRegex, workspace: ws, fields: ['dataset_id'] },
          })
          .then((response) => {
            return {[ws]: response.results.map(item => item.dataset_id)}
          })
      })

      Promise.all(promises)
        .then(response => {
          const mergedResponse = response.reduce((acc, obj) => {
            return {...acc, ...obj}
          }, {})
          const result = Object.entries(mergedResponse).reduce((acc, [ws, datasets]) => {
            return datasets.length !== 0 ? {...acc, [ws]: datasets} : acc
          }, {})
          setDatasetIds(result)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
    }

    if (activeModels !== undefined && Object.keys(activeModels)?.length > 0) {
      fetchRROpenRuns()
      fetchCAFJson({ kind: 'golden', setStateCallback: setGoldenJson })
      fetchCAFJson({ kind: 'dcs', setStateCallback: setDCSJson })
      fetchDatasetIds()
    }
  }, [activeModels, datasetRegex, rrClassName, rrDatasetName])

  useEffect(() => {
    const fetchElegibleBrilRuns = () => {
      API.brilws.brilcalc
        .lumi({
          beamStatus: brilBeamStatus,
          aModeTag: brilAModeTag,
          normTag: brilNormTag,
          connect: brilConnect,
          unit: brilUnit,
          scope: 'detailed', // Do not let the user edit this :)
          begin: Math.min(...rrOpenRuns),
          end: Math.max(...rrOpenRuns),
        })
        .then((response) => {
          const result = response
            .filter((item) => rrOpenRuns.includes(item.run))
            .filter((item) => item[`recorded(${brilUnit})`] > brilLowLumiRule)
            .map((item) => item.run)
          setBrilRuns(result)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
    }

    if (rrOpenRuns !== undefined && rrOpenRuns.length > 0) {
      fetchElegibleBrilRuns()
    }
  }, [rrOpenRuns])

  useEffect(() => {
    const fetchMLJson = (runList) => {
      const promises = Object.keys(datasetIds).map(async ws => {
        return API.mlBadLumis
          .goldenJson({
            datasetIdIn: datasetIds[ws],
            runNumberIn: runList,
            modelIdIn: activeModels[ws].map(item => item.model_id),
            workspace: ws
          })
      })

      Promise.all(promises)
        .then(response => {
          const mergedWorkspacesMLJson = response.reduce((acc, wsJson) => {
            for (const run in wsJson) {
              const expandedRun = rangeToList(wsJson[run])
              acc[run] = Object.hasOwn(acc, run) ? acc[run].filter(value => expandedRun.includes(value)) : expandedRun
            }
            return acc
          }, {})
          const result = Object.keys(mergedWorkspacesMLJson).reduce((acc, key) => {
            acc[key] = [...listToRange(mergedWorkspacesMLJson[key])]
            return acc
          }, {})
          setMLGoldenJson(result)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
    }

    if (
      datasetIds !== undefined &&
      activeModels !== undefined &&
      brilRuns !== undefined
    ) {
      if (Object.keys(datasetIds).length === 0 || brilRuns.length === 0) {
        setMLGoldenJson({})
      } else {
        fetchMLJson(brilRuns)
      }
    }
  }, [datasetIds, activeModels, brilRuns])

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
              activeModels?.length === 0 ||
              goldenJson === undefined ||
              dcsJson === undefined ||
              mlGoldenJson === undefined ||
              goldenJsonNotFound ||
              dcsJsonNotFound
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
              <p><strong>Info</strong>: Considering all active models in all non-staging workspaces.</p>
              <hr/>
              <Form>
                <Form.Check
                  defaultChecked={true}
                  type='checkbox'
                  label='Filter ML JSON with DCS JSON'
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
      {activeModels?.length === 0 && (
        <Row className='mt-3'>
          <Col md={4} />
          <Col md={4} className='text-center'>
            <Alert variant='danger'>
              <Alert.Heading>Oh snap! Where are the models?</Alert.Heading>
              <p>There are no active models set in any workspace.</p>
            </Alert>
          </Col>
          <Col md={4} />
        </Row>
      )}
      <hr />
      <Row className='mt-3'>
        <Col md={4}>
          <div className='text-center'>
            <strong>
              {goldenJson === undefined || goldenJsonNotFound ? (
                <div>Golden JSON</div>
              ) : (
                <a
                  href='#'
                  onClick={() =>
                    triggerDownload({
                      filename: goldenJson.name,
                      obj: goldenJson.download,
                    })
                  }
                >
                  {`${goldenJson.name} (generated at: ${goldenJson.last_modified})`}
                </a>
              )}
            </strong>
          </div>
          <div style={{ border: '3px solid #ddd', padding: '10px' }}>
            {goldenJson === undefined && (
              <Spinner animation='border' role='status' />
            )}
            {goldenJson !== undefined && goldenJsonNotFound && (
              <div>
                <span className='ms-1'>{`There are no Golden json files available in CAF for (${rrClassName}), therefore no JSON will be generated.`}</span>
              </div>
            )}
            {goldenJson !== undefined && !goldenJsonNotFound && (
              <AceEditor
                mode='javascript'
                theme='github'
                readOnly={true}
                height='50vh'
                width='100%'
                fontSize={15}
                wrapEnabled={true}
                value={JSON.stringify(goldenJson.content)}
                setOptions={{
                  useWorker: false
                }}
              />
            )}
          </div>
        </Col>
        <Col md={4}>
          <div className='text-center'>
            <strong>
              {dcsJson === undefined || dcsJsonNotFound ? (
                <div>DCS JSON</div>
              ) : (
                <a
                  href='#'
                  onClick={() =>
                    triggerDownload({
                      filename: dcsJson.name,
                      obj: dcsJson.download,
                    })
                  }
                >
                  {`${dcsJson.name} (generated at: ${dcsJson.last_modified})`}
                </a>
              )}
            </strong>
          </div>
          <div style={{ border: '3px solid #ddd', padding: '10px' }}>
            {dcsJson === undefined && (
              <Spinner animation='border' role='status' />
            )}
            {dcsJson !== undefined && dcsJsonNotFound && (
              <div>
                <span className='ms-1'>{`There are no DCS json files available in CAF for (${rrClassName}), therefore no JSON will be generated.`}</span>
              </div>
            )}
            {dcsJson !== undefined && !dcsJsonNotFound && (
              <AceEditor
                mode='javascript'
                theme='github'
                readOnly={true}
                height='50vh'
                width='100%'
                fontSize={15}
                wrapEnabled={true}
                value={JSON.stringify(dcsJson.content)}
                setOptions={{
                  useWorker: false
                }}
              />
            )}
          </div>
        </Col>
        <Col md={4}>
          <div className='text-center'>
            <strong>
              {mlGoldenJson === undefined ? (
                <div>ML JSON</div>
              ) : (
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
              )}
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
                <span className='ms-1'>Fetching active ML models...</span>
              </div>
            )}
            {datasetIds === undefined && (
              <div>
                <Spinner animation='border' role='status' />
                <span className='ms-1'>{`Fetching dataset ids for pattern: ${datasetRegex}`}</span>
              </div>
            )}
            {rrOpenRuns !== undefined && rrOpenRuns.length === 0 && (
              <div>
                <span className='ms-1'>{`There are no OPEN runs in Run Registry for (${rrClassName}, ${rrDatasetName}), therefore no ML JSON will be generated.`}</span>
              </div>
            )}
            {rrOpenRuns !== undefined && rrOpenRuns.length > 0 && brilRuns === undefined && (
              <div>
                <Spinner animation='border' role='status' />
                <span className='ms-1'>{`Fetching luminosity data from Bril for ${rrOpenRuns.length} ${rrOpenRuns.length === 1 ? 'run' : 'runs'}.`}</span>
              </div>
            )}
            {brilRuns !== undefined && brilRuns.length === 0 && (
              <div>
                <span className='ms-1'>{`There are no OPEN runs in Run Registry for (${rrClassName}, ${rrDatasetName}) with luminosity greater than ${brilLowLumiRule} ${brilUnit} in Bril, therefore no ML JSON will be generated.`}</span>
              </div>
            )}
            {brilRuns !== undefined && brilRuns.length > 0 && mlGoldenJson === undefined && (
              <div>
                <Spinner animation='border' role='status' />
                <span className='ms-1'>Generating the ML JSON</span>
              </div>
            )}
            {brilRuns!== undefined && brilRuns.length > 0 && mlGoldenJson !== undefined && (
              <AceEditor
                mode='javascript'
                theme='github'
                readOnly={true}
                height='50vh'
                width='100%'
                fontSize={15}
                wrapEnabled={true}
                value={JSON.stringify(mlGoldenJson)}
                setOptions={{
                  useWorker: false
                }}
              />
            )}
          </div>
        </Col>
      </Row>
    </Container>
  )
}

export default JsonPortal
