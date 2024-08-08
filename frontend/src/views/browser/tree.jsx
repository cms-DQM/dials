import React, { useState, useEffect } from 'react'

import { Link } from 'react-router-dom'
import { toast } from 'react-toastify'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Card from 'react-bootstrap/Card'
import Breadcrumb from 'react-bootstrap/Breadcrumb'

import API from '../../services/api'
import directoryIcon from '../../assets/img/dir.png'
import { ResponsivePlot } from '../components'

export const TreeNode = ({
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

export const TreeGrid = ({ fullTree, datasetId, runNumber, lsNumber }) => {
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
