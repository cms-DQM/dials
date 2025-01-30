import { sanitizedURLSearchParams } from '../../utils'
import { DIALS_API_URL } from '../../config/env'
import axiosApiInstance from './adapters'

const getDataset = async ({ datasetId, workspace }) => {
  const endpoint = `${DIALS_API_URL}/dataset-index/${datasetId}/`
  const headers = { Workspace: workspace }
  const response = await axiosApiInstance.get(endpoint, {
    headers,
  })
  return response.data
}

const listDatasets = async ({
  pageSize,
  nextToken,
  fields,
  dataset,
  datasetRegex,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/dataset-index/`
  const headers = { Workspace: workspace }
  const params = sanitizedURLSearchParams(
    {
      page_size: pageSize,
      next_token: nextToken,
      fields,
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

const datasetIndexApi = {
  dataset: {
    get: getDataset,
    list: listDatasets,
  },
}

export default datasetIndexApi
