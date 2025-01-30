import { sanitizedURLSearchParams } from '../../utils'
import { DIALS_API_URL } from '../../config/env'
import axiosApiInstance from './adapters'

const listMLBadLumisections = async ({
  pageSize,
  nextToken,
  fields,
  modelId,
  modelIdIn,
  datasetId,
  datasetIdIn,
  dataset,
  datasetRegex,
  meId,
  me,
  meRegex,
  runNumber,
  runNumberIn,
  lsNumber,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/ml-bad-lumisection/`
  const headers = { Workspace: workspace }
  const params = sanitizedURLSearchParams(
    {
      page_size: pageSize,
      next_token: nextToken,
      fields,
      model_id: modelId,
      model_id__in: modelIdIn,
      dataset_id: datasetId,
      dataset_id__in: datasetIdIn,
      dataset,
      dataset__regex: datasetRegex,
      me_id: meId,
      me,
      me__regex: meRegex,
      run_number: runNumber,
      run_number__in: runNumberIn,
      ls_number: lsNumber,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
    headers,
  })
  return response.data
}

const getMLCertificationJson = async ({
  modelIdIn,
  datasetIdIn,
  runNumberIn,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/ml-bad-lumisection/cert-json/`
  const headers = { Workspace: workspace }
  const params = sanitizedURLSearchParams(
    {
      model_id__in: modelIdIn,
      dataset_id__in: datasetIdIn,
      run_number__in: runNumberIn,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
    headers,
  })
  return response.data
}

const getMLGoldenJson = async ({
  modelIdIn,
  datasetIdIn,
  runNumberIn,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/ml-bad-lumisection/golden-json/`
  const headers = { Workspace: workspace }
  const params = sanitizedURLSearchParams(
    {
      model_id__in: modelIdIn,
      dataset_id__in: datasetIdIn,
      run_number__in: runNumberIn,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
    headers,
  })
  return response.data
}

const mlBadLumisectionApi = {
  mlBadLumis: {
    list: listMLBadLumisections,
    certJson: getMLCertificationJson,
    goldenJson: getMLGoldenJson,
  },
}

export default mlBadLumisectionApi
