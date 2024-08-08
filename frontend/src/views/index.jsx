import Home from './home'
import Overview from './overview'
import Browser from './browser'
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
  Home,
  Overview,
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
