import React from 'react'

import { Routes, Route } from 'react-router-dom'

import Home from './components/home'
import Overview from './components/overview'
import FileIndex from './dataExplorer/fileIndex'
import Runs from './dataExplorer/runs'
import Run from './dataExplorer/run'
import Lumisections from './dataExplorer/lumisections'
import Lumisection from './dataExplorer/lumisection'
import Histograms1D from './dataExplorer/histograms1d'
import Histograms2D from './dataExplorer/histograms2d'
import Histogram from './dataExplorer/histogram'
import Browser from './browser'
import Predictions from './machineLearning/predictions'
import JsonPortal from './machineLearning/jsonPortal'

const AppRoutes = () => {
  return (
    <Routes>
      <Route path='/' element={<Home />} />
      <Route path='/overview' element={<Overview />} />
      <Route path='/file-index' element={<FileIndex />} />
      <Route path='/runs'>
        <Route index element={<Runs />} />
        <Route
          path=':datasetId/:runNumber'
          element={<Run />}
        />
      </Route>
      <Route path='/lumisections'>
        <Route index element={<Lumisections />} />
        <Route
          path=':datasetId/:runNumber/:lsNumber'
          element={<Lumisection />}
        />
      </Route>
      <Route path='/histograms-1d'>
        <Route index element={<Histograms1D />} />
        <Route
          path=':datasetId/:runNumber/:lsNumber/:meId'
          element={<Histogram dim={1} />}
        />
      </Route>
      <Route path='/histograms-2d'>
        <Route index element={<Histograms2D />} />
        <Route
          path=':datasetId/:runNumber/:lsNumber/:meId'
          element={<Histogram dim={2} />}
        />
      </Route>
      <Route path='/browser' element={<Browser />} />
      <Route
        path='/predictions'
        element={<Predictions />}
      />
      <Route
        path='/json-portal'
        element={<JsonPortal />}
      />
    </Routes>
  )
}

export default AppRoutes
