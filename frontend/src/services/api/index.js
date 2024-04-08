import axios from 'axios'

import { sanitizedURLSearchParams } from '../../utils/sanitizer'
import { getPublicToken, getConfidentialToken } from '../../utils/userTokens'
import { API_URL, OIDC_USER_WORKSPACE } from '../../config/env'

const FILE_INDEX_STATUSES = [
  'INDEXED',
  'PENDING',
  'STARTED',
  'DOWNLOAD_ERROR',
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

const listFileIndex = async ({
  page,
  campaign,
  dataset,
  era,
  logicalFileName,
  minSize,
  status,
}) => {
  const endpoint = `${API_URL}/file-index/`
  const params = sanitizedURLSearchParams(
    {
      page,
      campaign,
      dataset,
      era,
      logical_file_name: logicalFileName,
      min_size: !isNaN(minSize) ? parseInt(minSize) * 1024 ** 2 : undefined, // Transforming from MB (user input) to B
      status,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const getRun = async ({ run }) => {
  const endpoint = `${API_URL}/run/${run}/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const listRuns = async ({ page, maxRun, minRun }) => {
  const endpoint = `${API_URL}/run/`
  const params = sanitizedURLSearchParams(
    {
      page,
      max_run_number: maxRun,
      min_run_number: minRun,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const getLumisection = async ({ id }) => {
  const endpoint = `${API_URL}/lumisection/${id}/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const listLumisections = async ({
  page,
  runNumber,
  ls,
  maxLs,
  minLs,
  maxRun,
  minRun,
}) => {
  const endpoint = `${API_URL}/lumisection/`
  const params = sanitizedURLSearchParams(
    {
      page,
      run_number: runNumber,
      ls_number: ls,
      max_ls_number: maxLs,
      max_run_number: maxRun,
      min_ls_number: minLs,
      min_run_number: minRun,
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
    run,
    ls,
    lsId,
    title,
    maxLs,
    minLs,
    maxRun,
    minRun,
    minEntries,
    titleContains,
    era,
    campaign,
    dataset,
    fileId,
  }
) => {
  const endpoint = `${API_URL}/lumisection-h${dim}d/`
  const params = sanitizedURLSearchParams(
    {
      page,
      run_number: run,
      ls_number: ls,
      lumisection_id: lsId,
      title,
      max_ls_number: maxLs,
      max_run_number: maxRun,
      min_ls_number: minLs,
      min_run_number: minRun,
      min_entries: minEntries,
      title_contains: titleContains,
      era,
      campaign,
      dataset,
      file_id: fileId,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const getHistogram = async (dim, id) => {
  const endpoint = `${API_URL}/lumisection-h${dim}d/${id}/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const getIngestedMonitoringElements = async (dim) => {
  const endpoint = `${API_URL}/lumisection-h${dim}d-mes/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const API = {
  auth: {
    exchange: exchangeToken,
  },
  fileIndex: {
    statusList: FILE_INDEX_STATUSES,
    list: listFileIndex,
  },
  lumisection: {
    get: getLumisection,
    list: listLumisections,
    listHistograms,
    getIngestedMEs: getIngestedMonitoringElements,
    getHistogram,
  },
  run: {
    get: getRun,
    list: listRuns,
  },
  config: {
    getWorkspaces,
  },
}

export default API
