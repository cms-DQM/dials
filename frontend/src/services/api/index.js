import workspacesApi from './workspaces'
import datasetIndexApi from './datasetIndex'
import fileIndexApi from './fileIndex'
import runApi from './run'
import lumisectionApi from './lumisection'
import histogramApi from './histogram'
import mesApi from './mes'
import mlModelsIndexApi from './mlModelsIndex'
import mlBadLumisectionApi from './mlBadLumisection'
import thirdPartyProxiesApi from './thirdPartyProxies'
import utilsApi from './utils'

const API = {
  ...workspacesApi,
  ...datasetIndexApi,
  ...fileIndexApi,
  ...runApi,
  ...lumisectionApi,
  ...histogramApi,
  ...mesApi,
  ...mlModelsIndexApi,
  ...mlBadLumisectionApi,
  ...thirdPartyProxiesApi,
  ...utilsApi,
}

export default API
