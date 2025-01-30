import { sanitizedURLSearchParams } from '../../utils/sanitizer'
import { DIALS_API_URL } from '../../config/env'
import axiosApiInstance from './adapters'

const getLumisection = async ({
  datasetId,
  runNumber,
  lsNumber,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/lumisection/${datasetId}/${runNumber}/${lsNumber}/`
  const headers = { Workspace: workspace }
  const response = await axiosApiInstance.get(endpoint, {
    headers,
  })
  return response.data
}

const listLumisections = async ({
  pageSize,
  nextToken,
  fields,
  datasetId,
  runNumber,
  runNumberLte,
  runNumberGte,
  lsNumber,
  lsNumberLte,
  lsNumberGte,
  dataset,
  datasetRegex,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/lumisection/`
  const headers = { Workspace: workspace }
  const params = sanitizedURLSearchParams(
    {
      page_size: pageSize,
      next_token: nextToken,
      fields,
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
    headers,
  })
  return response.data
}

const countLumisections = async ({
  datasetId,
  runNumber,
  runNumberLte,
  runNumberGte,
  lsNumber,
  lsNumberLte,
  lsNumberGte,
  dataset,
  datasetRegex,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/lumisection/count/`
  const headers = { Workspace: workspace }
  const params = sanitizedURLSearchParams(
    {
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
    headers,
  })
  return response.data
}

const lumisectionApi = {
  lumisection: {
    get: getLumisection,
    list: listLumisections,
    count: countLumisections,
  },
}

export default lumisectionApi
