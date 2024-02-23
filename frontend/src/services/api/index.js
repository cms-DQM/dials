import axios from 'axios'

import { toUndefined, sanitizedURLSearchParams } from '../../utils/sanitizer'
import { getPublicToken, getConfidentialToken } from '../../utils/userTokens'
import { API_URL } from '../../config/env'

const FILE_INDEX_STATUSES = [
  'INDEXED',
  'PENDING',
  'RUNNING',
  'PROCESSED',
  'FAILED'
]

const axiosApiInstance = axios.create()

axiosApiInstance.interceptors.request.use(
  async config => {
    const oidc = getConfidentialToken()
    config.headers = {
      Authorization: `${oidc.tokenType} ${oidc.accessToken}`,
      Accept: 'application/json'
    }
    return config
  },
  error => {
    Promise.reject(error)
  })

const exchangeToken = async ({ subjectToken }) => {
  const oidc = getPublicToken()
  const endpoint = `${API_URL}/auth/exchange-token/`
  const response = await axios.post(endpoint, {
    subject_token: subjectToken
  },
  {
    headers: {
      Authorization: `${oidc.tokenType} ${oidc.accessToken}`,
      Accept: 'application/json'
    }
  }
  )
  return response.data
}

const listFileIndex = async ({ page, era, minSize, pathContains, status }) => {
  const endpoint = `${API_URL}/file-index/`
  const params = sanitizedURLSearchParams({
    page,
    era,
    status,
    min_size: !isNaN(minSize) ? parseInt(minSize) * (1024 ** 2) : undefined, // Transforming from MB (user input) to B
    path_contains: pathContains
  }, { repeatMode: false })
  const response = await axiosApiInstance.get(endpoint, {
    params
  })
  return response.data
}

const listBadFileIndex = async ({ page, era, minSize, pathContains }) => {
  const endpoint = `${API_URL}/bad-file-index/`
  const params = sanitizedURLSearchParams({
    page,
    era,
    min_size: !isNaN(minSize) ? parseInt(minSize) * (1024 ** 2) : undefined, // Transforming from MB (user input) to B
    path_contains: pathContains
  }, { repeatMode: false })
  const response = await axiosApiInstance.get(endpoint, {
    params
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
  const params = sanitizedURLSearchParams({
    page,
    max_run_number: maxRun,
    min_run_number: minRun
  }, { repeatMode: false })
  const response = await axiosApiInstance.get(endpoint, {
    params
  })
  return response.data
}

const listLumisectionsInRun = async ({ page, runNumber }) => {
  const endpoint = `${API_URL}/run/${runNumber}/lumisections/`
  const params = sanitizedURLSearchParams({ page }, { repeatMode: false })
  const response = await axiosApiInstance.get(endpoint, {
    params
  })
  return response.data
}

const getLumisection = async ({ id }) => {
  const endpoint = `${API_URL}/lumisection/${id}/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const listLumisections = async ({ page, run, ls, maxLs, minLs, maxRun, minRun }) => {
  const endpoint = `${API_URL}/lumisection/`
  const params = sanitizedURLSearchParams({
    page,
    run_number: run,
    ls_number: ls,
    max_ls_number: maxLs,
    max_run_number: maxRun,
    min_ls_number: minLs,
    min_run_number: minRun
  }, { repeatMode: false })
  const response = await axiosApiInstance.get(endpoint, {
    params
  })
  return response.data
}

const listHistograms = async (dim, { page, run, ls, lsId, title, maxLs, minLs, maxRun, minRun, minEntries, titleContains }) => {
  const endpoint = `${API_URL}/lumisection-h${dim}d/`
  const params = sanitizedURLSearchParams({
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
    title_contains: titleContains
  }, { repeatMode: false })
  const response = await axiosApiInstance.get(endpoint, {
    params
  })
  return response.data
}

const getHistogram = async (dim, id) => {
  const endpoint = `${API_URL}/lumisection-h${dim}d/${id}/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const getIngestedSubsystems = async (dim) => {
  const endpoint = `${API_URL}/lumisection-h${dim}d/count-by-subsystem/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const listTasks = async ({ page, status, taskName, worker, minDateCreated, maxDateCreated, minDateDone, maxDateDone }) => {
  const endpoint = `${API_URL}/celery-tasks/`
  const params = sanitizedURLSearchParams({
    page,
    status,
    task_name: taskName,
    worker,
    min_date_created: minDateCreated,
    max_date_created: maxDateCreated,
    min_date_done: minDateDone,
    max_date_done: maxDateDone
  }, { repeatMode: true })
  const response = await axiosApiInstance.get(endpoint, {
    params
  })
  return response.data
}

const API = {
  auth: {
    exchange: exchangeToken
  },
  fileIndex: {
    statusList: FILE_INDEX_STATUSES,
    list: listFileIndex
  },
  badFileIndex: {
    list: listBadFileIndex
  },
  lumisection: {
    get: getLumisection,
    list: listLumisections,
    listHistograms,
    getSubsystemCount: getIngestedSubsystems,
    getHistogram
  },
  run: {
    get: getRun,
    list: listRuns,
    listLumisections: listLumisectionsInRun
  },
  jobQueue: {
    list: listTasks
  }
}

export default API
