import { Routes, Route } from 'react-router-dom';

import { Navbar } from './components';
import { Home, DataIngestion, FileIndex, Histograms1D } from './views';

const Root = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ingest" element={<DataIngestion />} />
        <Route path="/file-index" element={<FileIndex />} />
        <Route path="/histograms-1d" element={<Histograms1D />} />
      </Routes>
    </>
  );
}

export default Root;
