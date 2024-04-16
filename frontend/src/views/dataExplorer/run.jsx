import React, { useState, useEffect } from 'react'

import { useParams, Link } from 'react-router-dom'
import Breadcrumb from 'react-bootstrap/Breadcrumb'
import Row from 'react-bootstrap/Row'
import Col from 'react-bootstrap/Col'
import Card from 'react-bootstrap/Card'
import paginationFactory from 'react-bootstrap-table2-paginator'
import { toast } from 'react-toastify'

import API from '../../services/api'
import { CMSOMSCard, Table } from '../../components'

const Run = () => {
  const { runNumber } = useParams()

  const [isLoading, setLoading] = useState(true)
  const [currentPage, setCurrentPage] = useState(1)
  const [data, setData] = useState([])
  const [totalSize, setTotalSize] = useState()

  const columns = [
    {
      dataField: 'ls_number',
      text: 'Lumisection',
      type: 'number',
      formatter: (cell, row) => {
        const linkTo = `/lumisections/${row.ls_id}`
        return <Link to={linkTo}>{row.ls_number}</Link>
      },
    },
    { dataField: 'th1_count', text: '1D Histograms', type: 'number' },
    { dataField: 'th2_count', text: '2D Histograms', type: 'number' },
    { dataField: 'int_lumi', text: 'Initial Luminosity', type: 'number' },
    {
      dataField: 'oms_zerobias_rate',
      text: 'OMS ZeroBias Rate',
      type: 'number',
    },
  ]

  const fetchData = ({ page, runNumber }) => {
    setLoading(true)
    API.lumisection
      .list({ page, runNumber })
      .then((response) => {
        setData(response.results)
        setTotalSize(response.count)
        setCurrentPage(page)
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
    fetchData({ page: 1, runNumber })
  }, [runNumber])

  return (
    <>
      <Row className='mt-5 mb-3 m-3'>
        <Breadcrumb>
          <Breadcrumb.Item linkAs={Link} linkProps={{ to: '/runs' }}>
            All runs
          </Breadcrumb.Item>
          <Breadcrumb.Item active>{`Run ${runNumber}`}</Breadcrumb.Item>
        </Breadcrumb>
      </Row>
      <Row className='mt-1 mb-3 m-3'>
        <Col sm={9}>
          <Card className='text-center'>
            <Card.Header as='h4'>
              {isLoading
                ? 'Loading run...'
                : `This run has ${totalSize} lumisections`}
            </Card.Header>
            <Card.Body>
              <Table
                keyField='id'
                isLoading={isLoading}
                data={data}
                columns={columns}
                bordered={false}
                hover={true}
                remote
                onTableChange={(type, { page }) => {
                  if (type === 'pagination') {
                    fetchData({ page, runNumber })
                  }
                }}
                pagination={paginationFactory({
                  totalSize,
                  page: currentPage,
                  hideSizePerPage: true,
                  showTotal: true,
                })}
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
