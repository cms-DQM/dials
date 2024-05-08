import React from 'react'

import Plot from 'react-plotly.js'
import Spinner from 'react-bootstrap/Spinner'

const ResponsivePlot = (props) => {
  const { data, layout, config, style, isLoading } = props
  return (
    <>
      {isLoading ? (
        <Spinner animation='border' role='status' />
      ) : (
        <Plot
          data={data}
          layout={layout}
          config={config}
          useResizeHandler={true}
          style={style}
        />
      )}
    </>
  )
}

export default ResponsivePlot
