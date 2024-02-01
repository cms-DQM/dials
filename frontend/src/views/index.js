import Home from './home'
import DataIngestion from './dataIngestion'
import {
  FileIndex,
  Histograms1D,
  Histograms2D,
  Runs,
  Lumisections,
  Run
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
    lumisections: Lumisections,
    h1d: Histograms1D,
    h2d: Histograms2D,
    run: Run
  },
  machineLearning: {
    createPipelines: CreatePipelines,
    runPipelines: RunPipelines,
    predict: ModelPredict
  }
}

export default Views
