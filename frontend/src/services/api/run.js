import { sanitizedURLSearchParams } from '../../utils'
import { DIALS_API_URL } from '../../config/env'
import axiosApiInstance from './adapters'

const getRun = async ({ datasetId, runNumber, workspace }) => {
  const endpoint = `${DIALS_API_URL}/run/${datasetId}/${runNumber}/`
  const headers = { Workspace: workspace }
  const response = await axiosApiInstance.get(endpoint, {
    headers,
  })
  return response.data
}

const listRuns = async ({
  pageSize,
  nextToken,
  fields,
  datasetId,
  datasetIdIn,
  runNumber,
  runNumberLte,
  runNumberGte,
  dataset,
  datasetRegex,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/run/`
  const headers = { Workspace: workspace }
  const params = sanitizedURLSearchParams(
    {
      page_size: pageSize,
      next_token: nextToken,
      fields,
      dataset_id: datasetId,
      dataset_id__in: datasetIdIn,
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
    headers,
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
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/run/count/`
  const headers = { Workspace: workspace }
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
    headers,
  })
  return response.data
}

const runApi = {
  run: {
    get: getRun,
    list: listRuns,
    count: countRuns,
  },
}

export default runApi
