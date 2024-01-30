import React from 'react'
import { useResizeDetector } from 'react-resize-detector'
import Plot from 'react-plotly.js'

const ResponsivePlot = (props) => {
  const { width, height, ref } = useResizeDetector()
  const { data, layout, config } = props

  return (
    <div ref={ref} style={{ display: 'flex', height: '100%' }}>
      <Plot
        data={data}
        layout={{
          ...layout,
          ...{
            width,
            height
          }
        }}
        config={config}
      />
    </div>
  )
}

export default ResponsivePlot
