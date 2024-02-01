import Home from './home'
import DataIngestion from './dataIngestion'
import {
  FileIndex,
  Runs,
  Run,
  Lumisections,
  Lumisection,
  Histograms1D,
  Histograms2D
} from './dataExplorer'
import {
  CreatePipelines,
  RunPipelines,
  ModelPredict
} from './machineLearning'

const Views = {
  home: {
    index: Home
  },
  dataIngestion: {
    index: DataIngestion
  },
  dataExplorer: {
    fileIndex: FileIndex,
    runs: Runs,
    run: Run,
    lumisections: Lumisections,
    lumisection: Lumisection,
    h1d: Histograms1D,
    h2d: Histograms2D
  },
  machineLearning: {
    createPipelines: CreatePipelines,
    runPipelines: RunPipelines,
    predict: ModelPredict
  }
}

export default Views
