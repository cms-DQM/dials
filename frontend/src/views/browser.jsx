import React, { useState, useEffect } from 'react'

import { Link } from 'react-router-dom'
import { toast } from 'react-toastify'
import Container from 'react-bootstrap/Container'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Form from 'react-bootstrap/Form'
import Card from 'react-bootstrap/Card'
import Breadcrumb from 'react-bootstrap/Breadcrumb'
import Button from 'react-bootstrap/Button'
import Select from 'react-select'

import API from '../services/api'
import directoryIcon from '../assets/img/dir.png'
import { ResponsivePlot } from '../components'
import { getNextToken } from '../utils/sanitizer'

const TreeNode = ({
  datasetId,
  runNumber,
  lsNumber,
  index,
  node,
  navigateTo,
}) => {
  const [isLoading, setIsLoading] = useState(true)
  const [data, setData] = useState(null)

  useEffect(() => {
    const fetchData = ({ dim, datasetId, runNumber, lsNumber, meId }) => {
      setIsLoading(true)
      API.histogram
        .get({
          dim,
          datasetId,
          runNumber,
          lsNumber,
          meId,
        })
        .then((response) => {
          if (dim === 1) {
            setData([
              {
                y: response.data,
                type: 'bar',
                marker: { color: '#0033A0' },
              },
            ])
          } else {
            setData([
              {
                z: response.data,
                type: 'heatmap',
                marker: { color: 'Viridis' },
              },
            ])
          }
        })
        .catch((err) => {
          console.error(err)
          toast.error('Failure to communicate with the API!')
        })
        .finally(() => {
          setIsLoading(false)
        })
    }
    if (node.type !== 'directory') {
      fetchData({
        dim: node.dim,
        datasetId,
        runNumber,
        lsNumber,
        meId: node.me_id,
      })
    }
  }, [datasetId, runNumber, lsNumber, node])

  return (
    <Card
      key={index}
      onClick={() => node.type === 'directory' && navigateTo(node.name)}
    >
      {node.type === 'directory' ? (
        <Card.Img
          style={{ height: 'auto', width: '100%' }}
          variant='top'
          src={directoryIcon}
        />
      ) : (
        <div className='card-img-top' style={{ height: '280px' }}>
          <Link
            to={`/histograms-${node.dim}d/${datasetId}/${runNumber}/${lsNumber}/${node.me_id}`}
          >
            <ResponsivePlot
              isLoading={isLoading}
              data={data}
              layout={{
                margin: { t: 10, b: 10, l: 10, r: 10 },
                yaxis: { visible: false },
                xaxis: { visible: false },
                bargap: 0,
                paper_bgcolor: 'rgba(0,0,0,0)',
                plot_bgcolor: 'rgba(0,0,0,0)',
              }}
              config={{ staticPlot: true }}
              style={{
                width: '100%',
                height: '100%',
              }}
            />
          </Link>
        </div>
      )}
      <Card.Body>
        <Card.Title>
          {node.type === 'directory' ? (
            `${node.name} (${node.children.length} ${node.children.length > 1 ? 'items' : 'item'})`
          ) : (
            <Link
              to={`/histograms-${node.dim}d/${datasetId}/${runNumber}/${lsNumber}/${node.me_id}`}
            >
              {node.name}
            </Link>
          )}
        </Card.Title>
      </Card.Body>
    </Card>
  )
}

const TreeGrid = ({ fullTree, datasetId, runNumber, lsNumber }) => {
  const [currentPath, setCurrentPath] = useState([])
  const [currentTree, setCurrentTree] = useState(fullTree)

  const navigateTo = (dir) => {
    const newPath = [...currentPath, dir]
    const newTree = getCurrentTree(newPath, fullTree)
    setCurrentPath(newPath)
    setCurrentTree(newTree)
  }

  const navigateToPath = (index) => {
    if (index === -1) {
      setCurrentPath([])
      setCurrentTree(fullTree)
    } else {
      const newPath = currentPath.slice(0, index + 1)
      const newTree = getCurrentTree(newPath, fullTree)
      setCurrentPath(newPath)
      setCurrentTree(newTree)
    }
  }

  const getCurrentTree = (path, tree) => {
    return path.reduce((current, part) => {
      const found = current.find((node) => node.name === part)
      return found ? found.children : []
    }, tree)
  }

  return (
    <div>
      <Breadcrumb>
        <Breadcrumb.Item
          disabled={currentPath.length === 0}
          active={currentPath.length === 0}
          onClick={() => navigateToPath(-1)}
        >
          Root
        </Breadcrumb.Item>
        {currentPath.map((dir, index) => (
          <Breadcrumb.Item
            disabled={index === currentPath.length - 1}
            active={index === currentPath.length - 1}
            key={index}
            onClick={() => navigateToPath(index)}
          >
            {dir}
          </Breadcrumb.Item>
        ))}
      </Breadcrumb>
      {currentTree.map(
        (obj, index) =>
          index % 6 === 0 && (
            <Row key={index} className='mb-3'>
              {currentTree.slice(index, index + 6).map((node, innerIndex) => {
                return (
                  <Col key={innerIndex} sm={2}>
                    <TreeNode
                      datasetId={datasetId}
                      runNumber={runNumber}
                      lsNumber={lsNumber}
                      index={index}
                      node={node}
                      navigateTo={navigateTo}
                    />
                  </Col>
                )
              })}
            </Row>
          )
      )}
    </div>
  )
}

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

  const buildTree = (items) => {
    const tree = []
    items.forEach((item) => {
      const path = item.me
      const parts = path.split('/')
      let currentLevel = tree
      parts.forEach((part, index) => {
        let existingPath = currentLevel.find((node) => node.name === part)
        if (!existingPath) {
          existingPath = {
            name: part,
            type: index === parts.length - 1 ? 'file' : 'directory',
            children: [],
            me_id: index === parts.length - 1 ? item.me_id : undefined,
            count: index === parts.length - 1 ? item.count : undefined,
            dim: index === parts.length - 1 ? item.dim : undefined,
          }
          currentLevel.push(existingPath)
        }
        currentLevel = existingPath.children
      })
    })
    return tree
  }

  useEffect(() => {
    const fetchDatasets = () => {
      setIsLoadingDatasets(true)
      genericFetchAllPages({ apiMethod: API.dataset.list })
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

  useEffect(() => {
    const fetchLumisections = ({ datasetId, runNumber }) => {
      setIsLoadingLumisections(true)
      genericFetchAllPages({
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
          console.log(data)
          console.log(buildTree(data))
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
