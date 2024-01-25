import { Routes, Route } from 'react-router-dom';

import { Navbar } from './components';
import {
  Home,
  DataIngestion,
  FileIndex,
  Histograms1D,
  Histograms2D,
  Runs,
  Lumisections,
  CreatePipelines,
  RunPipelines
} from './views';

const Root = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ingest" element={<DataIngestion />} />
        <Route path="/file-index" element={<FileIndex />} />
        <Route path="/histograms-1d" element={<Histograms1D />} />
        <Route path="/histograms-2d" element={<Histograms2D />} />
        <Route path="/runs" element={<Runs />} />
        <Route path="/lumisections" element={<Lumisections />} />
        <Route path="/create" element={<CreatePipelines />} />
        <Route path="/train" element={<RunPipelines />} />
      </Routes>
    </>
  );
}

export default Root;
