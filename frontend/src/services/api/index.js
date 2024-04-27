import axios from 'axios'

import { sanitizedURLSearchParams } from '../../utils/sanitizer'
import { getPublicToken, getConfidentialToken } from '../../utils/userTokens'
import { API_URL, OIDC_USER_WORKSPACE } from '../../config/env'

const FILE_INDEX_STATUSES = [
  'PENDING',
  'DOWNLOAD_STARTED',
  'DOWNLOAD_ERROR',
  'DOWNLOAD_FINISHED',
  'INGESTION_STARTED',
  'COPY_ERROR',
  'ROOTFILE_ERROR',
  'PARSING_ERROR',
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

const exchangeToken = async ({ subjectToken }) => {
  const oidc = getPublicToken()
  const endpoint = `${API_URL}/auth/exchange-token/`
  const response = await axios.post(
    endpoint,
    {
      subject_token: subjectToken,
    },
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

const listDatasets = async ({ page, dataset, datasetRegex }) => {
  const endpoint = `${API_URL}/dataset-index/`
  const params = sanitizedURLSearchParams(
    {
      page,
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
  page,
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
      page,
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
  page,
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
      page,
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
  page,
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
      page,
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
    page,
    datasetId,
    fileId,
    runNumber,
    runNumberLte,
    runNumberGte,
    lsNumber,
    lsNumberLte,
    lsNumberGte,
    meId,
    lsId,
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
      page,
      dataset_id: datasetId,
      file_id: fileId,
      run_number: runNumber,
      run_number__lte: runNumberLte,
      run_number__gte: runNumberGte,
      ls_number: lsNumber,
      ls_number__lte: lsNumberLte,
      ls_number__gte: lsNumberGte,
      me_id: meId,
      ls_id: lsId,
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

const getHistogram = async (dim, histId) => {
  const endpoint = `${API_URL}/th${dim}/${histId}/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const listMEs = async (dim) => {
  const endpoint = `${API_URL}/mes/`
  const params = sanitizedURLSearchParams(
    {
      dim,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, { params })
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
  },
  run: {
    get: getRun,
    list: listRuns,
  },
  lumisection: {
    get: getLumisection,
    list: listLumisections,
  },
  mes: {
    list: listMEs,
  },
  histogram: {
    get: getHistogram,
    list: listHistograms,
  },
}

export default API
