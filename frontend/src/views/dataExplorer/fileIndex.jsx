import React, { useState, useEffect } from 'react'

import Col from 'react-bootstrap/Col'
import Row from 'react-bootstrap/Row'
import Card from 'react-bootstrap/Card'
import Form from 'react-bootstrap/Form'
import Button from 'react-bootstrap/Button'
import RangeSlider from 'react-bootstrap-range-slider'
import paginationFactory from 'react-bootstrap-table2-paginator'

import { Table } from '../../components'
import dateFormat from '../../utils/date'
import API from '../../services/api'
import { toast } from 'react-toastify'

const FileIndex = () => {
  const [isLoading, setLoading] = useState(true)
  const [currentPage, setCurrentPage] = useState(1)
  const [campaign, setCampaign] = useState()
  const [primaryDataset, setPrimaryDataset] = useState()
  const [era, setEra] = useState()
  const [logicalFileName, setLogicalFileName] = useState()
  const [minSize, setMinSize] = useState(0)
  const [fileStatus, setFileStatus] = useState()
  const [data, setData] = useState([])
  const [totalSize, setTotalSize] = useState()

  const columns = [
    { dataField: 'file_id', text: 'ID', type: 'number' },
    { dataField: 'file_size', text: 'Size (MB)', type: 'number' },
    { dataField: 'era', text: 'Era', type: 'string' },
    { dataField: 'campaign', text: 'Campaign', type: 'string' },
    { dataField: 'primary_dataset', text: 'Primary Dataset', type: 'string' },
    {
      dataField: 'last_modification_date',
      text: 'Last Modification Date',
      type: 'string',
    },
    {
      dataField: 'logical_file_name',
      text: 'Logical File Name',
      type: 'string',
    },
    { dataField: 'status', text: 'Status', type: 'string' },
  ]

  const fetchData = ({
    page,
    campaign,
    primaryDataset,
    era,
    logicalFileName,
    minSize,
    status,
  }) => {
    setLoading(true)
    API.fileIndex
      .list({
        page,
        campaign,
        primaryDataset,
        era,
        logicalFileName,
        minSize: minSize > 0 ? minSize : undefined,
        status,
      })
      .then((response) => {
        const results = response.results.map((item) => {
          return {
            ...item,
            last_modification_date: dateFormat(
              item.last_modification_date,
              'dd.MM.yyyy HH:mm:ss'
            ),
            file_size: (item.file_size / 1024 ** 2).toFixed(1),
          }
        })
        setData(results)
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
    fetchData({ page: 1 })
  }, [])

  return (
    <Row className='mt-5 mb-3 m-3'>
      <Col sm={3}>
        <Card>
          <Card.Header className='text-center' as='h4'>
            Filters
          </Card.Header>
          <Card.Body>
            <Form.Group className='mb-3' controlId='formCampaign'>
              <Form.Label>Campaign contains</Form.Label>
              <Form.Control
                type='string'
                placeholder='Enter campaign substring'
                value={campaign}
                onChange={(e) => setCampaign(e.target.value)}
              />
            </Form.Group>

            <Form.Group className='mb-3' controlId='formPrimaryDataset'>
              <Form.Label>Primary Dataset</Form.Label>
              <Form.Control
                type='string'
                placeholder='Enter primary dataset'
                value={primaryDataset}
                onChange={(e) => setPrimaryDataset(e.target.value)}
              />
            </Form.Group>

            <Form.Group className='mb-3' controlId='formEra'>
              <Form.Label>Era</Form.Label>
              <Form.Control
                type='string'
                placeholder='Enter era'
                value={era}
                onChange={(e) => setEra(e.target.value)}
              />
            </Form.Group>

            <Form.Group className='mb-3' controlId='formLogicalFileName'>
              <Form.Label>Logical file name contains</Form.Label>
              <Form.Control
                type='string'
                placeholder='Enter logical file name substring'
                value={logicalFileName}
                onChange={(e) => setLogicalFileName(e.target.value)}
              />
            </Form.Group>

            <Form.Group className='mb-3' controlId='formSizeRange' as={Row}>
              <Form.Label>Minimum size (MB)</Form.Label>
              <Col xs={3}>
                <Form.Control
                  type='number'
                  value={minSize}
                  onChange={(e) => setMinSize(e.target.value)}
                />
              </Col>
              <Col xs={9}>
                <RangeSlider
                  min={0}
                  max={1000}
                  value={minSize}
                  onChange={(e) => setMinSize(e.target.value)}
                />
              </Col>
            </Form.Group>

            <Form.Group className='mb-3' controlId='formFileStatus'>
              <Form.Label>Status</Form.Label>
              <Form.Select
                default='ANY'
                value={fileStatus}
                onChange={(e) =>
                  setFileStatus(
                    e.target.value === 'ANY' ? undefined : e.target.value
                  )
                }
              >
                <option key='ANY' value='ANY'>
                  ANY
                </option>
                {API.fileIndex.statusList.map((item) => {
                  return (
                    <option key={item} value={item}>
                      {item}
                    </option>
                  )
                })}
              </Form.Select>
            </Form.Group>

            <Button
              variant='primary'
              type='submit'
              onClick={() => {
                fetchData({
                  page: 1,
                  campaign,
                  primaryDataset,
                  era,
                  logicalFileName,
                  minSize,
                  status: fileStatus,
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
          <Card.Header as='h4'>Files</Card.Header>
          <Card.Body>
            <Table
              keyField='file_path'
              isLoading={isLoading}
              data={data}
              columns={columns}
              bordered={false}
              hover={true}
              remote
              onTableChange={(type, { page }) => {
                if (type === 'pagination') {
                  fetchData({
                    page,
                    campaign,
                    primaryDataset,
                    era,
                    logicalFileName,
                    minSize,
                    status: fileStatus,
                  })
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
    </Row>
  )
}

export default FileIndex
