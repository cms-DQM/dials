import sleep from '../../utils/sleep';
import dateFormat from '../../utils/date';

import tasksResults from '../../mocks/tasksResults.json'
import tasksPending from '../../mocks/tasksPending.json'

const getLatestTasks = async () => {
  await sleep(5);
  const tasks = tasksResults.results.slice(0, 5).map(item => {
    return { ...item, date_created: dateFormat(item.date_created, 'dd.MM.yyyy HH:mm:ss') }
  })
  return tasks
}

const getPendingTasks = async () => {
  await sleep(5);
  return tasksPending
}

export {
  getLatestTasks,
  getPendingTasks
}