import React from 'react'

import { Routes, Route } from 'react-router-dom'

import Views from './index'

const AppRoutes = () => {
  return (
    <Routes>
      <Route path='/' element={<Views.Home />} />
      <Route path='/overview' element={<Views.Overview />} />
      <Route path='/file-index' element={<Views.DataExplorer.FileIndex />} />
      <Route path='/runs'>
        <Route index element={<Views.DataExplorer.Runs />} />
        <Route
          path=':datasetId/:runNumber'
          element={<Views.DataExplorer.Run />}
        />
      </Route>
      <Route path='/lumisections'>
        <Route index element={<Views.DataExplorer.Lumisections />} />
        <Route
          path=':datasetId/:runNumber/:lsNumber'
          element={<Views.DataExplorer.Lumisection />}
        />
      </Route>
      <Route path='/histograms-1d'>
        <Route index element={<Views.DataExplorer.Histograms1D />} />
        <Route
          path=':datasetId/:runNumber/:lsNumber/:meId'
          element={<Views.DataExplorer.Histogram dim={1} />}
        />
      </Route>
      <Route path='/histograms-2d'>
        <Route index element={<Views.DataExplorer.Histograms2D />} />
        <Route
          path=':datasetId/:runNumber/:lsNumber/:meId'
          element={<Views.DataExplorer.Histogram dim={2} />}
        />
      </Route>
      <Route path='/browser' element={<Views.Browser />} />
      <Route
        path='/predictions'
        element={<Views.MachineLearning.Predictions />}
      />
      <Route
        path='/json-portal'
        element={<Views.MachineLearning.JsonPortal />}
      />
    </Routes>
  )
}

export default AppRoutes
