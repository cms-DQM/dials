import { sanitizedURLSearchParams } from '../../utils/sanitizer'
import { DIALS_API_URL } from '../../config/env'
import axiosApiInstance from './adapters'

const listMEs = async ({ fields, me, meRegex, dim, workspace }) => {
  const endpoint = `${DIALS_API_URL}/mes/`
  const headers = { Workspace: workspace }
  const params = sanitizedURLSearchParams(
    {
      fields,
      me,
      me__regex: meRegex,
      dim,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
    headers,
  })
  return response.data
}

const listMEsByRun = async ({ datasetId, runNumber, workspace }) => {
  const endpoint = `${DIALS_API_URL}/mes/${datasetId}/${runNumber}/`
  const headers = { Workspace: workspace }
  const response = await axiosApiInstance.get(endpoint, {
    headers,
  })
  return response.data
}

const mesApi = {
  mes: {
    list: listMEs,
    listByRun: listMEsByRun,
  },
}

export default mesApi
