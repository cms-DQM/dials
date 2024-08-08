import React from 'react'

import Plot from 'react-plotly.js'
import { useResizeDetector } from 'react-resize-detector'
import Spinner from 'react-bootstrap/Spinner'

const ResponsivePlot = (props) => {
  const { width, height, ref } = useResizeDetector({})
  const { data, layout, config, style, isLoading } = props
  return (
    <>
      {isLoading ? (
        <Spinner animation='border' role='status' />
      ) : (
        <div ref={ref} style={{ display: 'flex', height: '100%' }}>
          <Plot
            data={data}
            layout={{ ...layout, width, height }}
            config={config}
            useResizeHandler={true}
            style={style}
          />
        </div>
      )}
    </>
  )
}

export default ResponsivePlot
