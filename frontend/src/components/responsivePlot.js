import React from 'react'
import { useResizeDetector } from 'react-resize-detector'
import Plot from 'react-plotly.js'

const ResponsivePlot = (props) => {
  const { width: resizedWidth, height: resizedHeight, ref } = useResizeDetector()
  const { data, layout, config, boxWidth, boxHeight } = props
  const divStyle = (boxHeight && boxWidth) ? { height: boxHeight, width: boxWidth } : { display: 'flex', height: '100%' }

  return (
    <div ref={ref} style={divStyle}>
      <Plot
        data={data}
        layout={{
          ...layout,
          ...{
            width: resizedWidth,
            height: resizedHeight
          }
        }}
        config={config}
      />
    </div>
  )
}

export default ResponsivePlot
