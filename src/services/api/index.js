import sleep from '../../utils/sleep';
import dateFormat from '../../utils/date';

import tasksResults from '../mocks/tasksResults.json'
import tasksPending from '../mocks/tasksPending.json'
import fileIndexPage1 from '../mocks/fileIndex-page1.json'
import fileIndexPage2 from '../mocks/fileIndex-page2.json'
import fileIndexPage3 from '../mocks/fileIndex-page3.json'

const FILE_INDEX_STATUSES = [
  "INDEXED",
  "PENDING",
  "RUNNING",
  "OK",
  "FAILED"
]

const getLatestTasks = async () => {
  await sleep(1);
  const tasks = tasksResults.results.slice(0, 5).map(item => {
    return { ...item, date_created: dateFormat(item.date_created, 'dd.MM.yyyy HH:mm:ss') }
  })
  return tasks
}

const getPendingTasks = async () => {
  await sleep(1);
  return tasksPending
}

const getFileIndexByPage = async (page) => {
  await sleep(1);
  const mockedResponse = {
    1: fileIndexPage1,
    2: fileIndexPage2,
    3: fileIndexPage3
  }
  return mockedResponse[[page]]
}

export {
  FILE_INDEX_STATUSES,
  getLatestTasks,
  getPendingTasks,
  getFileIndexByPage
}