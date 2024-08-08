import Home from './home'
import Browser from './browser'
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
import { Predictions } from './machineLearning'

const Views = {
  Home: {
    Index: Home,
  },
  DataIngestion: {
    Index: DataIngestion,
  },
  Browser,
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
  MachineLearning: {
    Predictions,
  },
}

export default Views
