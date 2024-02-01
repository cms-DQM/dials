import React, { useState, useEffect } from 'react'

import { useParams, Link } from 'react-router-dom'
import Breadcrumb from 'react-bootstrap/Breadcrumb'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Card from 'react-bootstrap/Card'
import paginationFactory from 'react-bootstrap-table2-paginator'

import Table from '../../components/table'
import API from '../../services/api'
import CMSOMSCard from '../../components/cmsOMSCard'

const Run = () => {
  const { runNumber } = useParams()
  const [isLoading, setLoading] = useState(true)
  const [page, setPage] = useState(1)
  const [data, setData] = useState([])
  const [totalSize, setTotalSize] = useState()

  const columns = [
    {
      dataField: 'ls_number',
      text: 'Lumisection',
      type: 'number',
      formatter: (cell, row) => {
        const linkTo = {
          pathname: `/lumisections/${row.ls_number}`,
          search: `?runNumber=${runNumber}`
        }
        return (
          <Link to={linkTo}>{row.ls_number}</Link>
        )
      }
    },
    { dataField: 'hist1d_count', text: '1D Histograms', type: 'number' },
    { dataField: 'hist2d_count', text: '2D Histograms', type: 'number' },
    { dataField: 'int_lumi', text: 'Initial Luminosity', type: 'number' },
    { dataField: 'oms_zerobias_rate', text: 'OMS ZeroBias Rate', type: 'number' }
  ]

  const pagination = paginationFactory({ page, totalSize, hideSizePerPage: true })
  const remote = { pagination: true, filter: false, sort: false }

  const handleTableChange = (type, { page }) => {
    if (type === 'pagination') {
      setPage(page)
    }
  }

  useEffect(() => {
    const handleData = () => {
      setLoading(true)
      API.run.getLumis({ page, runNumber })
        .then(response => {
          setData(response.results)
          setTotalSize(response.count)
        })
        .catch(error => {
          console.error(error)
        })
        .finally(() => {
          setLoading(false)
        })
    }
    handleData()
  }, [page])

  return (
    <>
      <Row className='mt-5 mb-3 m-3'>
        <Breadcrumb>
          <Breadcrumb.Item linkAs={Link} linkProps={{ to: '/runs' }}>All runs</Breadcrumb.Item>
          <Breadcrumb.Item active>{`Run ${runNumber}`}</Breadcrumb.Item>
        </Breadcrumb>
      </Row>
      <Row className='mt-1 mb-3 m-3'>
        <Col sm={9}>
          <Card className='text-center'>
            <Card.Header as='h4'>{`This run has ${totalSize} lumisections`}</Card.Header>
            <Card.Body>
              <Table
                keyField='id'
                isLoading={isLoading}
                data={data}
                columns={columns}
                bordered={false}
                hover={true}
                remote={remote}
                pagination={pagination}
                onTableChange={handleTableChange}
              />
            </Card.Body>
          </Card>
        </Col>
        <Col sm={3}>
          <CMSOMSCard runNumber={runNumber}/>
        </Col>
      </Row>
    </>
  )
}

export default Run
