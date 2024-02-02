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
        <Route path='/' element={<Views.home.index />} />
        <Route path='/ingest' element={<Views.dataIngestion.index />} />
        <Route path='/file-index' element={<Views.dataExplorer.fileIndex />} />
        <Route path='/runs'>
          <Route index element={<Views.dataExplorer.runs />}/>
          <Route path=':runNumber' element={<Views.dataExplorer.run />}/>
        </Route>
        <Route path='/lumisections'>
          <Route index element={<Views.dataExplorer.lumisections />}/>
          <Route path=':id' element={<Views.dataExplorer.lumisection />}/>
        </Route>
        <Route path='/histograms-1d'>
          <Route index element={<Views.dataExplorer.h1d />}/>
          <Route path=':id' element={<Views.dataExplorer.hist dim={1} />}/>
        </Route>
        <Route path='/histograms-2d'>
          <Route index element={<Views.dataExplorer.h2d />}/>
          <Route path=':id' element={<Views.dataExplorer.hist dim={2} />}/>
        </Route>
        <Route path='/create' element={<Views.machineLearning.createPipelines />} />
        <Route path='/train' element={<Views.machineLearning.runPipelines />} />
        <Route path='/predict' element={<Views.machineLearning.predict />} />
      </Routes>
      <ToastContainer
        position='bottom-right'
      />
    </>
  )
}

export default Root
