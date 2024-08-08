import React, { useState, useEffect } from 'react'

import { useParams, Link } from 'react-router-dom'
import Breadcrumb from 'react-bootstrap/Breadcrumb'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Card from 'react-bootstrap/Card'
import { toast } from 'react-toastify'

import API from '../../services/api'
import { CMSOMSCard, Table } from '../components'
import { getNextToken } from '../../utils/sanitizer'

const Run = () => {
  const { datasetId, runNumber } = useParams()
  const [isLoading, setLoading] = useState(true)

  // API results
  const [dataset, setDataset] = useState()
  const [data, setData] = useState([])
  const [nextToken, setNextToken] = useState(null)
  const [previousToken, setPreviousToken] = useState(null)

  const columns = [
    {
      dataField: 'ls_number',
      text: 'Lumisection',
      type: 'number',
      formatter: (cell, row) => {
        const linkTo = `/lumisections/${row.dataset_id}/${row.run_number}/${row.ls_number}`
        return <Link to={linkTo}>{row.ls_number}</Link>
      },
    },
    { dataField: 'th1_count', text: '1D Histograms', type: 'number' },
    { dataField: 'th2_count', text: '2D Histograms', type: 'number' },
  ]

  const fetchData = ({ nextToken, datasetId, runNumber }) => {
    setLoading(true)
    API.lumisection
      .list({ nextToken, datasetId, runNumber })
      .then((response) => {
        const results = response.results.map((item) => {
          return {
            ...item,
            keyField: `${item.dataset_id}_${item.run_number}_${item.ls_number}`,
          }
        })
        const dataset = response.results?.[0]?.dataset
        const nextToken = getNextToken(response, 'next')
        const previousToken = getNextToken(response, 'previous')
        setData(results)
        setDataset(dataset)
        setNextToken(nextToken)
        setPreviousToken(previousToken)
      })
      .catch((error) => {
        console.error(error)
        toast.error('Failure to communicate with the API!')
      })
      .finally(() => {
        setLoading(false)
      })
  }

  useEffect(() => {
    fetchData({ datasetId, runNumber })
  }, [datasetId, runNumber])

  return (
    <>
      <Row className='mt-5 mb-3 m-3'>
        <Breadcrumb>
          <Breadcrumb.Item linkAs={Link} linkProps={{ to: '/runs' }}>
            All runs
          </Breadcrumb.Item>
          {isLoading ? (
            <Breadcrumb.Item active>Loading...</Breadcrumb.Item>
          ) : (
            <>
              <Breadcrumb.Item
                active
              >{`Dataset ${datasetId} (${dataset})`}</Breadcrumb.Item>
              <Breadcrumb.Item active>{`Run ${runNumber}`}</Breadcrumb.Item>
            </>
          )}
        </Breadcrumb>
      </Row>
      <Row className='mt-1 mb-3 m-3'>
        <Col sm={9}>
          <Card className='text-center'>
            <Card.Header as='h4'>
              {isLoading
                ? 'Loading run...'
                : `Lumisections found in Run #${runNumber}`}
            </Card.Header>
            <Card.Body>
              <Table
                keyField='keyField'
                isLoading={isLoading}
                data={data}
                columns={columns}
                bordered={false}
                hover={true}
                remote
                cursorPagination={true}
                previousToken={previousToken}
                nextToken={nextToken}
                previousOnClick={() => {
                  fetchData({
                    nextToken: previousToken,
                    datasetId,
                    runNumber,
                  })
                }}
                nextOnClick={() => {
                  fetchData({
                    nextToken,
                    datasetId,
                    runNumber,
                  })
                }}
              />
            </Card.Body>
          </Card>
        </Col>
        <Col sm={3}>
          <CMSOMSCard isLoading={isLoading} runNumber={runNumber} />
        </Col>
      </Row>
    </>
  )
}

export default Run
