import axios from 'axios'

import toUndefined from '../../utils/sanitizer'
import { API_URL } from '../../config/env'

const FILE_INDEX_STATUSES = [
  'INDEXED',
  'PENDING',
  'RUNNING',
  'PROCESSED',
  'FAILED'
]

const getFileIndex = async ({ page, era, minSize, pathContains, status }) => {
  const endpoint = `${API_URL}/file-index/`
  const response = await axios.get(endpoint, {
    params: {
      page,
      era: toUndefined(era, ''),
      status: toUndefined(status, ''),
      min_size: !isNaN(minSize) ? parseInt(minSize) * (1024 ** 2) : undefined, // Transforming from MB (user input) to B
      path_contains: toUndefined(pathContains, '')
    },
    headers: {
      Accept: 'application/json'
    }
  })
  return response.data
}

const getRun = async ({ page, maxRun, minRun }) => {
  const endpoint = `${API_URL}/run/`
  const response = await axios.get(endpoint, {
    params: {
      page,
      max_run_number: toUndefined(maxRun, ''),
      min_run_number: toUndefined(minRun, '')
    },
    headers: {
      Accept: 'application/json'
    }
  })
  return response.data
}

const getLumisection = async ({ page, maxLs, minLs, maxRun, minRun }) => {
  const endpoint = `${API_URL}/lumisection/`
  const response = await axios.get(endpoint, {
    params: {
      page,
      max_ls_number: toUndefined(maxLs, ''),
      max_run_number: toUndefined(maxRun, ''),
      min_ls_number: toUndefined(minLs, ''),
      min_run_number: toUndefined(minRun, '')
    },
    headers: {
      Accept: 'application/json'
    }
  })
  return response.data
}

const getLumisectionHist = async (dim, { page, run, ls, maxLs, minLs, maxRun, minRun, minEntries, titleContains }) => {
  const endpoint = `${API_URL}/lumisection-h${dim}d/`
  const response = await axios.get(endpoint, {
    params: {
      page,
      run_number: toUndefined(run, ''),
      ls_number: toUndefined(ls, ''),
      max_ls_number: toUndefined(maxLs, ''),
      max_run_number: toUndefined(maxRun, ''),
      min_ls_number: toUndefined(minLs, ''),
      min_run_number: toUndefined(minRun, ''),
      min_entries: toUndefined(minEntries, ''),
      title_contains: toUndefined(titleContains, '')
    },
    headers: {
      Accept: 'application/json'
    }
  })
  return response.data
}

const getLumisectionHistSubsystemCount = async (dim) => {
  const endpoint = `${API_URL}/lumisection-h${dim}d/count-by-subsystem/`
  const response = await axios.get(endpoint, {
    headers: {
      Accept: 'application/json'
    }
  })
  return response.data
}

const getTrackedTasks = async ({ page }) => {
  const endpoint = `${API_URL}/celery-tasks/`
  const response = await axios.get(endpoint, {
    params: {
      page
    },
    headers: {
      Accept: 'application/json'
    }
  })
  return response.data
}

const getEnqueuedTasks = async () => {
  const endpoint = `${API_URL}/celery-tasks/queued/`
  const response = await axios.get(endpoint, {
    headers: {
      Accept: 'application/json'
    }
  })
  return response.data
}

const API = {
  fileIndex: {
    statusList: FILE_INDEX_STATUSES,
    get: getFileIndex
  },
  lumisection: {
    get: getLumisection,
    getHist: getLumisectionHist,
    getSubsystemCount: getLumisectionHistSubsystemCount
  },
  run: {
    get: getRun
  },
  jobQueue: {
    tracked: getTrackedTasks,
    enqueued: getEnqueuedTasks
  }
}

export default API
