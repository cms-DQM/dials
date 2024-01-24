import React, { useState, useEffect } from 'react';

import Card from 'react-bootstrap/Card';
import paginationFactory from 'react-bootstrap-table2-paginator';

import Table from '../../../components/table';
import { getRunsByPage } from '../../../services/api';

const RunsViz = () => {
  const [page, setPage] = useState(1);
  const [data, setData] = useState([]);
  const [totalSize, setTotalSize] = useState();
  const [isLoading, setLoading] = useState(true);

  const columns = [
    { dataField: "run_number", text: "Run", type: "string" },
    { dataField: "year", text: "Year", type: "string" },
    { dataField: "period", text: "Period", type: "string" },
    { dataField: "oms_fill", text: "OMS Fill", type: "string" },
    { dataField: "oms_lumisections", text: "OMS Lumisections", type: "string" },
    { dataField: "oms_initial_lumi", text: "OMS Initial Lumi", type: "string" },
    { dataField: "oms_end_lumi", text: "OMS End Lumi", type: "string" }
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
      getRunsByPage(page)
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
    <Card className="text-center">
      <Card.Header><h4>Runs</h4></Card.Header>
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

export default RunsViz;