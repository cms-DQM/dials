import axios from 'axios'

import { toUndefined } from '../../utils/sanitizer'
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
  const endpoint = `${API_URL}/exchange-token/`
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
  const response = await axiosApiInstance.get(endpoint, {
    params: {
      page,
      era: toUndefined(era, ''),
      status: toUndefined(status, ''),
      min_size: !isNaN(minSize) ? parseInt(minSize) * (1024 ** 2) : undefined, // Transforming from MB (user input) to B
      path_contains: toUndefined(pathContains, '')
    }
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
  const response = await axiosApiInstance.get(endpoint, {
    params: {
      page,
      max_run_number: toUndefined(maxRun, ''),
      min_run_number: toUndefined(minRun, '')
    }
  })
  return response.data
}

const listLumisectionsInRun = async ({ page, runNumber }) => {
  const endpoint = `${API_URL}/run/${runNumber}/lumisections/`
  const response = await axiosApiInstance.get(endpoint, {
    params: {
      page
    }
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
  const response = await axiosApiInstance.get(endpoint, {
    params: {
      page,
      run_number: toUndefined(run, ''),
      ls_number: toUndefined(ls, ''),
      max_ls_number: toUndefined(maxLs, ''),
      max_run_number: toUndefined(maxRun, ''),
      min_ls_number: toUndefined(minLs, ''),
      min_run_number: toUndefined(minRun, '')
    }
  })
  return response.data
}

const listHistograms = async (dim, { page, run, ls, lsId, title, maxLs, minLs, maxRun, minRun, minEntries, titleContains }) => {
  const endpoint = `${API_URL}/lumisection-h${dim}d/`
  const response = await axiosApiInstance.get(endpoint, {
    params: {
      page,
      run_number: toUndefined(run, ''),
      ls_number: toUndefined(ls, ''),
      lumisection_id: toUndefined(lsId, ''),
      title: toUndefined(title, ''),
      max_ls_number: toUndefined(maxLs, ''),
      max_run_number: toUndefined(maxRun, ''),
      min_ls_number: toUndefined(minLs, ''),
      min_run_number: toUndefined(minRun, ''),
      min_entries: toUndefined(minEntries, ''),
      title_contains: toUndefined(titleContains, '')
    }
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
  const response = await axiosApiInstance.get(endpoint, {
    params: {
      page,
      status: toUndefined(status, ''),
      task_name: toUndefined(taskName, ''),
      worker: toUndefined(worker, ''),
      min_date_created: toUndefined(minDateCreated, ''),
      max_date_created: toUndefined(maxDateCreated, ''),
      min_date_done: toUndefined(minDateDone, ''),
      max_date_done: toUndefined(maxDateDone, '')
    }
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
