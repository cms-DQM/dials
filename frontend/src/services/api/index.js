import axios from 'axios'

import { sanitizedURLSearchParams } from '../../utils/sanitizer'
import { getPublicToken, getConfidentialToken } from '../../utils/userTokens'
import { API_URL, OIDC_USER_WORKSPACE } from '../../config/env'

const FILE_INDEX_STATUSES = [
  'PENDING',
  'DOWNLOAD_STARTED',
  'DOWNLOAD_ERROR',
  'DOWNLOAD_FILE_NOT_AVAILABLE',
  'DOWNLOAD_FINISHED',
  'INGESTION_STARTED',
  'INGESTION_COPY_ERROR',
  'INGESTION_ROOTFILE_ERROR',
  'INGESTION_PARSING_ERROR',
  'FINISHED',
]

const axiosApiInstance = axios.create()

axiosApiInstance.interceptors.request.use(
  async (config) => {
    const workspace = localStorage.getItem(OIDC_USER_WORKSPACE)
    const oidc = getConfidentialToken()
    config.headers = {
      Authorization: `${oidc.tokenType} ${oidc.accessToken}`,
      Accept: 'application/json',
      Workspace: workspace,
    }
    return config
  },
  (error) => {
    Promise.reject(error)
  }
)

const getWorkspaces = async () => {
  const endpoint = `${API_URL}/auth/workspaces/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const exchangeToken = async () => {
  const oidc = getPublicToken()
  const endpoint = `${API_URL}/auth/exchange-token/`
  const response = await axios.post(
    endpoint,
    {},
    {
      headers: {
        Authorization: `${oidc.tokenType} ${oidc.accessToken}`,
        Accept: 'application/json',
      },
    }
  )
  return response.data
}

const getDataset = async ({ datasetId }) => {
  const endpoint = `${API_URL}/dataset-index/${datasetId}/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const listDatasets = async ({ nextToken, dataset, datasetRegex }) => {
  const endpoint = `${API_URL}/dataset-index/`
  const params = sanitizedURLSearchParams(
    {
      next_token: nextToken,
      dataset,
      dataset__regex: datasetRegex,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const listFileIndex = async ({
  nextToken,
  logicalFileName,
  logicalFileNameRegex,
  status,
  minSize,
  dataset,
  datasetRegex,
}) => {
  const endpoint = `${API_URL}/file-index/`
  const params = sanitizedURLSearchParams(
    {
      next_token: nextToken,
      logical_file_name: logicalFileName,
      logical_file_name__regex: logicalFileNameRegex,
      status,
      min_size: !isNaN(minSize) ? parseInt(minSize) * 1024 ** 2 : undefined, // Transforming from MB (user input) to B
      dataset,
      dataset__regex: datasetRegex,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const countFileIndex = async ({
  logicalFileName,
  logicalFileNameRegex,
  status,
  minSize,
  dataset,
  datasetRegex,
}) => {
  const endpoint = `${API_URL}/file-index/count/`
  const params = sanitizedURLSearchParams(
    {
      logical_file_name: logicalFileName,
      logical_file_name__regex: logicalFileNameRegex,
      status,
      min_size: !isNaN(minSize) ? parseInt(minSize) * 1024 ** 2 : undefined, // Transforming from MB (user input) to B
      dataset,
      dataset__regex: datasetRegex,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const getRun = async ({ datasetId, runNumber }) => {
  const endpoint = `${API_URL}/run/${datasetId}/${runNumber}/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const listRuns = async ({
  nextToken,
  datasetId,
  runNumber,
  runNumberLte,
  runNumberGte,
  dataset,
  datasetRegex,
}) => {
  const endpoint = `${API_URL}/run/`
  const params = sanitizedURLSearchParams(
    {
      next_token: nextToken,
      dataset_id: datasetId,
      run_number: runNumber,
      run_number__lte: runNumberLte,
      run_number__gte: runNumberGte,
      dataset,
      dataset__regex: datasetRegex,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const countRuns = async ({
  datasetId,
  runNumber,
  runNumberLte,
  runNumberGte,
  dataset,
  datasetRegex,
}) => {
  const endpoint = `${API_URL}/run/count/`
  const params = sanitizedURLSearchParams(
    {
      dataset_id: datasetId,
      run_number: runNumber,
      run_number__lte: runNumberLte,
      run_number__gte: runNumberGte,
      dataset,
      dataset__regex: datasetRegex,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const getLumisection = async ({ datasetId, runNumber, lsNumber }) => {
  const endpoint = `${API_URL}/run/${datasetId}/${runNumber}/${lsNumber}/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const listLumisections = async ({
  nextToken,
  datasetId,
  runNumber,
  runNumberLte,
  runNumberGte,
  lsNumber,
  lsNumberLte,
  lsNumberGte,
  dataset,
  datasetRegex,
}) => {
  const endpoint = `${API_URL}/lumisection/`
  const params = sanitizedURLSearchParams(
    {
      next_token: nextToken,
      dataset_id: datasetId,
      run_number: runNumber,
      run_number__lte: runNumberLte,
      run_number__gte: runNumberGte,
      ls_number: lsNumber,
      ls_number__lte: lsNumberLte,
      ls_number__gte: lsNumberGte,
      dataset,
      dataset__regex: datasetRegex,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const countLumisections = async ({
  datasetId,
  runNumber,
  runNumberLte,
  runNumberGte,
  lsNumber,
  lsNumberLte,
  lsNumberGte,
  dataset,
  datasetRegex,
}) => {
  const endpoint = `${API_URL}/lumisection/count/`
  const params = sanitizedURLSearchParams(
    {
      dataset_id: datasetId,
      run_number: runNumber,
      run_number__lte: runNumberLte,
      run_number__gte: runNumberGte,
      ls_number: lsNumber,
      ls_number__lte: lsNumberLte,
      ls_number__gte: lsNumberGte,
      dataset,
      dataset__regex: datasetRegex,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const listHistograms = async (
  dim,
  {
    nextToken,
    datasetId,
    fileId,
    runNumber,
    runNumberLte,
    runNumberGte,
    lsNumber,
    lsNumberLte,
    lsNumberGte,
    meId,
    entriesGte,
    dataset,
    datasetRegex,
    logicalFileName,
    logicalFileNameRegex,
    me,
    meRegex,
  }
) => {
  const endpoint = `${API_URL}/th${dim}/`
  const params = sanitizedURLSearchParams(
    {
      next_token: nextToken,
      dataset_id: datasetId,
      file_id: fileId,
      run_number: runNumber,
      run_number__lte: runNumberLte,
      run_number__gte: runNumberGte,
      ls_number: lsNumber,
      ls_number__lte: lsNumberLte,
      ls_number__gte: lsNumberGte,
      me_id: meId,
      entries__gte: entriesGte,
      dataset,
      dataset__regex: datasetRegex,
      logical_file_name: logicalFileName,
      logical_file_name__regex: logicalFileNameRegex,
      me,
      me__regex: meRegex,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const getHistogram = async ({ dim, datasetId, runNumber, lsNumber, meId }) => {
  const endpoint = `${API_URL}/th${dim}/${datasetId}/${runNumber}/${lsNumber}/${meId}/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const listMEs = async ({ me, meRegex, dim }) => {
  const endpoint = `${API_URL}/mes/`
  const params = sanitizedURLSearchParams(
    {
      me,
      me__regex: meRegex,
      dim,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, { params })
  return response.data
}

const listMLModelsIndex = async ({
  nextToken,
  modelId,
  modelIdIn,
  filename,
  filenameRegex,
  targetMe,
  targetMeRegex,
  active,
}) => {
  const endpoint = `${API_URL}/ml-models-index/`
  const params = sanitizedURLSearchParams(
    {
      next_token: nextToken,
      model_id: modelId,
      model_id__in: modelIdIn,
      filename,
      filename__regex: filenameRegex,
      targetMe,
      target_me__regex: targetMeRegex,
      active,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const listMLBadLumisections = async ({
  nextToken,
  modelId,
  modelIdIn,
  dataset,
  datasetRegex,
  me,
  meRegex,
  runNumber,
  runNumberIn,
  lsNumber,
}) => {
  const endpoint = `${API_URL}/ml-bad-lumisection/`
  const params = sanitizedURLSearchParams(
    {
      next_token: nextToken,
      model_id: modelId,
      model_id__in: modelIdIn,
      dataset,
      dataset__regex: datasetRegex,
      me,
      me__regex: meRegex,
      run_number: runNumber,
      run_number__in: runNumberIn,
      ls_number: lsNumber,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const getMLCertificationJson = async ({
  modelIdIn,
  datasetId,
  runNumberIn,
}) => {
  const endpoint = `${API_URL}/ml-bad-lumisection/cert-json`
  const params = sanitizedURLSearchParams(
    {
      model_id__in: modelIdIn,
      dataset_id: datasetId,
      run_number__in: runNumberIn,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const getMLGoldenJson = async ({ modelIdIn, datasetId, runNumberIn }) => {
  const endpoint = `${API_URL}/ml-bad-lumisection/golden-json`
  const params = sanitizedURLSearchParams(
    {
      model_id__in: modelIdIn,
      dataset_id: datasetId,
      run_number__in: runNumberIn,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const API = {
  auth: {
    exchange: exchangeToken,
  },
  config: {
    getWorkspaces,
  },
  dataset: {
    get: getDataset,
    list: listDatasets,
  },
  fileIndex: {
    statusList: FILE_INDEX_STATUSES,
    list: listFileIndex,
    count: countFileIndex,
  },
  run: {
    get: getRun,
    list: listRuns,
    count: countRuns,
  },
  lumisection: {
    get: getLumisection,
    list: listLumisections,
    count: countLumisections,
  },
  mes: {
    list: listMEs,
  },
  histogram: {
    get: getHistogram,
    list: listHistograms,
  },
  mlModelsIndex: {
    list: listMLModelsIndex,
  },
  mlBadLumis: {
    list: listMLBadLumisections,
    certJson: getMLCertificationJson,
    goldenJson: getMLGoldenJson,
  },
}

export default API
