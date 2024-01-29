import React, { useState, useEffect } from 'react';

import Card from 'react-bootstrap/Card';
import paginationFactory from 'react-bootstrap-table2-paginator';

import Table from '../../../components/table';
import dateFormat from '../../../utils/date';
import { getFileIndexByPage } from '../../../services/api';

const FileIndexViz = () => {
  const [page, setPage] = useState(1);
  const [data, setData] = useState([]);
  const [totalSize, setTotalSize] = useState();
  const [isLoading, setLoading] = useState(true);

  const columns = [
    { dataField: "file_path", text: "Path", type: "string" },
    { dataField: "data_era", text: "Era", type: "string" },
    { dataField: "st_size", text: "Size (MB)", type: "number" },
    { dataField: "st_ctime", text: "Created at", type: "string" },
    { dataField: "st_itime", text: "Indexed at", type: "string" },
    { dataField: "status_h1d", text: "Status", type: "string"}
  ]
  const pagination = paginationFactory({ page: page, totalSize: totalSize, hideSizePerPage: true })
  const remote = { pagination: true, filter: false, sort: false }

  const handleTableChange = (type, { page }) => {
    if (type === "pagination") {
      setPage(page)
    }
  }

  useEffect(() => {
    const handleData = () => {
      setLoading(true)
      getFileIndexByPage(page)
        .then(response => {
          const results = response.results.map(item => {
            return {
              ...item,
              st_ctime: dateFormat(item.st_ctime, 'dd.MM.yyyy HH:mm:ss'),
              st_itime: dateFormat(item.st_itime, 'dd.MM.yyyy HH:mm:ss'),
              st_size: (item.st_size/1024**2).toFixed(1)
            }
          })
          setData(results)
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
    <Card className="text-center">
      <Card.Header as='h4'>Files</Card.Header>
      <Card.Body>
        <Table
          keyField='file_path'
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
  )
};

export default FileIndexViz;