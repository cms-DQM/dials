import React from 'react'

import Spinner from 'react-bootstrap/Spinner'
import BootstrapTable from 'react-bootstrap-table-next'

const Table = (props) => {
  return (
    <>
      {
        props.isLoading
          ? (
          <Spinner
            animation='border'
            role='status'
          />
            )
          : (
          <BootstrapTable
            keyField={props.keyField}
            data={props.data}
            columns={props.columns}
            bordered={props?.bordered}
            hover={props?.hover}
            pagination={props?.pagination}
            remote={props?.remote}
            onTableChange={props?.onTableChange}
          />
            )
      }
    </>
  )
}

export default Table
