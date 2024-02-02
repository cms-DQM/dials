import React from 'react'
import { Routes, Route } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'

import { Navbar } from './components'
import Views from './views'

const Root = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path='/' element={<Views.Home.Index />} />
        <Route path='/ingest' element={<Views.DataIngestion.Index />} />
        <Route path='/file-index' element={<Views.DataExplorer.FileIndex />} />
        <Route path='/runs'>
          <Route index element={<Views.DataExplorer.Runs />}/>
          <Route path=':runNumber' element={<Views.DataExplorer.Run />}/>
        </Route>
        <Route path='/lumisections'>
          <Route index element={<Views.DataExplorer.Lumisections />}/>
          <Route path=':id' element={<Views.DataExplorer.Lumisection />}/>
        </Route>
        <Route path='/histograms-1d'>
          <Route index element={<Views.DataExplorer.Histograms1D />}/>
          <Route path=':id' element={<Views.DataExplorer.Histogram dim={1} />}/>
        </Route>
        <Route path='/histograms-2d'>
          <Route index element={<Views.DataExplorer.Histograms2D />}/>
          <Route path=':id' element={<Views.DataExplorer.Histogram dim={2} />}/>
        </Route>
        <Route path='/create' element={<Views.MachineLearning.CreatePipelines />} />
        <Route path='/train' element={<Views.MachineLearning.RunPipelines />} />
        <Route path='/predict' element={<Views.MachineLearning.Predict />} />
      </Routes>
      <ToastContainer
        position='bottom-right'
      />
    </>
  )
}

export default Root
