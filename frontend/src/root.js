import React from 'react'
import { Routes, Route } from 'react-router-dom'

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
          <Route path=':lsNumber' element={<Views.dataExplorer.lumisection />}/>
        </Route>
        <Route path='/histograms-1d' element={<Views.dataExplorer.h1d />} />
        <Route path='/histograms-2d' element={<Views.dataExplorer.h2d />} />
        <Route path='/create' element={<Views.machineLearning.createPipelines />} />
        <Route path='/train' element={<Views.machineLearning.runPipelines />} />
        <Route path='/predict' element={<Views.machineLearning.predict />} />
      </Routes>
    </>
  )
}

export default Root
