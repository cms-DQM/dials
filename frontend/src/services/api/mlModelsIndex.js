import { sanitizedURLSearchParams } from '../../utils'
import { DIALS_API_URL } from '../../config/env'
import axiosApiInstance from './adapters'

const listMLModelsIndex = async ({
  pageSize,
  nextToken,
  fields,
  modelId,
  modelIdIn,
  filename,
  filenameRegex,
  targetMe,
  targetMeRegex,
  active,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/ml-models-index/`
  const headers = { Workspace: workspace }
  const params = sanitizedURLSearchParams(
    {
      page_size: pageSize,
      next_token: nextToken,
      fields,
      model_id: modelId,
      model_id__in: modelIdIn,
      filename,
      filename__regex: filenameRegex,
      targetMe,
      target_me__regex: targetMeRegex,
      active,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
    headers,
  })
  return response.data
}

const mlModelsIndexApi = {
  mlModelsIndex: {
    list: listMLModelsIndex,
  },
}

export default mlModelsIndexApi
