import { sanitizedURLSearchParams } from '../../utils/sanitizer'
import { DIALS_API_URL } from '../../config/env'
import axiosApiInstance from './adapters'

const listHistograms = async ({
  pageSize,
  nextToken,
  fields,
  dim,
  datasetId,
  fileId,
  runNumber,
  runNumberLte,
  runNumberGte,
  lsNumber,
  lsNumberLte,
  lsNumberGte,
  meId,
  entriesGte,
  dataset,
  datasetRegex,
  logicalFileName,
  logicalFileNameRegex,
  me,
  meRegex,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/th${dim}/`
  const headers = { Workspace: workspace }
  const params = sanitizedURLSearchParams(
    {
      page_size: pageSize,
      next_token: nextToken,
      fields,
      dataset_id: datasetId,
      file_id: fileId,
      run_number: runNumber,
      run_number__lte: runNumberLte,
      run_number__gte: runNumberGte,
      ls_number: lsNumber,
      ls_number__lte: lsNumberLte,
      ls_number__gte: lsNumberGte,
      me_id: meId,
      entries__gte: entriesGte,
      dataset,
      dataset__regex: datasetRegex,
      logical_file_name: logicalFileName,
      logical_file_name__regex: logicalFileNameRegex,
      me,
      me__regex: meRegex,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
    headers,
  })
  return response.data
}

const getHistogram = async ({
  dim,
  datasetId,
  runNumber,
  lsNumber,
  meId,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/th${dim}/${datasetId}/${runNumber}/${lsNumber}/${meId}/`
  const headers = { Workspace: workspace }
  const response = await axiosApiInstance.get(endpoint, {
    headers,
  })
  return response.data
}

const histogramApi = {
  histogram: {
    get: getHistogram,
    list: listHistograms,
  },
}

export default histogramApi
