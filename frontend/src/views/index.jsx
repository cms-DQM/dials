import Home from './home'
import DataIngestion from './dataIngestion'
import {
  FileIndex,
  Runs,
  Run,
  Lumisections,
  Lumisection,
  Histograms1D,
  Histograms2D,
  Histogram,
} from './dataExplorer'

const Views = {
  Home: {
    Index: Home,
  },
  DataIngestion: {
    Index: DataIngestion,
  },
  DataExplorer: {
    FileIndex,
    Runs,
    Run,
    Lumisections,
    Lumisection,
    Histograms1D,
    Histograms2D,
    Histogram,
  },
}

export default Views
