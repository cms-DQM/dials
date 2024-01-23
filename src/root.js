import { Routes, Route } from 'react-router-dom';

import { Navbar } from './components';
import { Home, DataIngestion } from './views';

const Root = () => {
  return (
    <>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/ingest" element={<DataIngestion />} />
      </Routes>
    </>
  );
}

export default Root;
