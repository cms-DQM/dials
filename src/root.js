import { Routes, Route } from 'react-router-dom';

import { Navbar } from './components';
import { Home, DataIngestion, FileIndex } from './views';

const Root = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ingest" element={<DataIngestion />} />
        <Route path="/file-index" element={<FileIndex />} />
      </Routes>
    </>
  );
}

export default Root;
