import sleep from '../../utils/sleep';
import dateFormat from '../../utils/date';

import Mock from '../mocks'

const FILE_INDEX_STATUSES = [
  "INDEXED",
  "PENDING",
  "RUNNING",
  "PROCESSED",
  "FAILED"
]

const getLatestTasks = async () => {
  await sleep(1);
  const tasks = Mock.tasksResults.results.slice(0, 5).map(item => {
    return { ...item, date_created: dateFormat(item.date_created, 'dd.MM.yyyy HH:mm:ss') }
  })
  return tasks
}

const getPendingTasks = async () => {
  await sleep(1);
  return Mock.tasksPending
}

const getFileIndexByPage = async (page) => {
  await sleep(1);
  const mockedResponse = {
    1: Mock.fileIndexPage1,
    2: Mock.fileIndexPage2,
    3: Mock.fileIndexPage3
  }
  return mockedResponse[[page]]
}

const getHistograms1DByPage = async (page) => {
  await sleep(1);
  const mockedResponse = {
    1: Mock.histograms1DPage1,
    2: Mock.histograms1DPage2,
    3: Mock.histograms1DPage3
  }
  return mockedResponse[[page]]
}

const getHistograms2DByPage = async (page) => {
  await sleep(1);
  const mockedResponse = {
    1: Mock.histograms2DPage1,
    2: Mock.histograms2DPage2,
    3: Mock.histograms2DPage3
  }
  return mockedResponse[[page]]
}

const getRunsByPage = async (page) => {
  await sleep(1);
  const mockedResponse = {
    1: Mock.runsPage1,
    2: Mock.runsPage2
  }
  return mockedResponse[[page]]
}

const getLumisectionsByPage = async (page) => {
  await sleep(1);
  const mockedResponse = {
    1: Mock.lumisectionsPage1,
    2: Mock.lumisectionsPage2,
    3: Mock.lumisectionsPage3
  }
  return mockedResponse[[page]]
}

export {
  FILE_INDEX_STATUSES,
  getLatestTasks,
  getPendingTasks,
  getFileIndexByPage,
  getHistograms1DByPage,
  getHistograms2DByPage,
  getRunsByPage,
  getLumisectionsByPage
}