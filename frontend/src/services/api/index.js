import axios from 'axios'

import sleep from '../../utils/sleep'
import toUndefined from '../../utils/sanitizer'
import Mock from '../mocks'
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

const getLumisectionH1D = async ({ page, lumisectionId, minEntries, titleContains }) => {
  const endpoint = `${API_URL}/lumisection-h1d/`
  const response = await axios.get(endpoint, {
    params: {
      page,
      lumisection_id: toUndefined(lumisectionId, ''),
      min_entries: toUndefined(minEntries, ''),
      title_contains: toUndefined(titleContains, '')
    },
    headers: {
      Accept: 'application/json'
    }
  })
  return response.data
}

const getLumisectionH2D = async ({ page, lumisectionId, minEntries, titleContains }) => {
  const endpoint = `${API_URL}/lumisection-h2d/`
  const response = await axios.get(endpoint, {
    params: {
      page,
      lumisection_id: toUndefined(lumisectionId, ''),
      min_entries: toUndefined(minEntries, ''),
      title_contains: toUndefined(titleContains, '')
    },
    headers: {
      Accept: 'application/json'
    }
  })
  return response.data
}

const getLumisectionH1DSubsystemCount = async () => {
  const endpoint = `${API_URL}/lumisection-h1d/count-by-subsystem/`
  const response = await axios.get(endpoint, {
    headers: {
      Accept: 'application/json'
    }
  })
  return response.data
}

const getLumisectionH2DSubsystemCount = async () => {
  const endpoint = `${API_URL}/lumisection-h2d/count-by-subsystem/`
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

export const getLatestTasks = async () => {
  await sleep(1)
  return Mock.tasksResults
}

export const getPendingTasks = async () => {
  await sleep(1)
  return Mock.tasksPending
}

export const getFileIndexByPage = async (page) => {
  await sleep(1)
  const mockedResponse = {
    1: Mock.fileIndexPage1,
    2: Mock.fileIndexPage2,
    3: Mock.fileIndexPage3
  }
  return mockedResponse[[page]]
}

export const getHistograms1DByPage = async (page) => {
  await sleep(1)
  const mockedResponse = {
    1: Mock.histograms1DPage1,
    2: Mock.histograms1DPage2,
    3: Mock.histograms1DPage3
  }
  return mockedResponse[[page]]
}

export const getHistograms2DByPage = async (page) => {
  await sleep(1)
  const mockedResponse = {
    1: Mock.histograms2DPage1,
    2: Mock.histograms2DPage2,
    3: Mock.histograms2DPage3
  }
  return mockedResponse[[page]]
}

export const getRunsByPage = async (page) => {
  await sleep(1)
  const mockedResponse = {
    1: Mock.runsPage1,
    2: Mock.runsPage2
  }
  return mockedResponse[[page]]
}

export const getLumisectionsByPage = async (page) => {
  await sleep(1)
  const mockedResponse = {
    1: Mock.lumisectionsPage1,
    2: Mock.lumisectionsPage2,
    3: Mock.lumisectionsPage3
  }
  return mockedResponse[[page]]
}

const API = {
  fileIndex: {
    statusList: FILE_INDEX_STATUSES,
    get: getFileIndex
  },
  lumisection: {
    get: getLumisection,
    getH1D: getLumisectionH1D,
    getH2D: getLumisectionH2D,
    getH1DSSCount: getLumisectionH1DSubsystemCount,
    getH2DSSCount: getLumisectionH2DSubsystemCount
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
