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
  Histogram
} from './dataExplorer'
import {
  CreatePipelines,
  RunPipelines,
  ModelPredict
} from './machineLearning'

const Views = {
  Home: {
    Index: Home
  },
  DataIngestion: {
    Index: DataIngestion
  },
  DataExplorer: {
    FileIndex,
    Runs,
    Run,
    Lumisections,
    Lumisection,
    Histograms1D,
    Histograms2D,
    Histogram
  },
  MachineLearning: {
    CreatePipelines,
    RunPipelines,
    ModelPredict
  }
}

export default Views
