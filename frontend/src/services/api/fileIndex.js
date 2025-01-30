import { sanitizedURLSearchParams } from '../../utils'
import { DIALS_API_URL } from '../../config/env'
import axiosApiInstance from './adapters'

const FILE_INDEX_STATUSES = [
  'PENDING',
  'STARTED',
  'FILE_NOT_AVAILABLE',
  'COPY_ERROR',
  'ROOTFILE_ERROR',
  'PARSING_ERROR',
  'FINISHED',
]

const listFileIndex = async ({
  pageSize,
  nextToken,
  fields,
  logicalFileName,
  logicalFileNameRegex,
  status,
  minSize,
  dataset,
  datasetRegex,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/file-index/`
  const headers = { Workspace: workspace }
  const params = sanitizedURLSearchParams(
    {
      page_size: pageSize,
      next_token: nextToken,
      fields,
      logical_file_name: logicalFileName,
      logical_file_name__regex: logicalFileNameRegex,
      status,
      min_size: !isNaN(minSize) ? parseInt(minSize) * 1024 ** 2 : undefined, // Transforming from MB (user input) to B
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

const countFileIndex = async ({
  logicalFileName,
  logicalFileNameRegex,
  status,
  minSize,
  dataset,
  datasetRegex,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/file-index/count/`
  const headers = { Workspace: workspace }
  const params = sanitizedURLSearchParams(
    {
      logical_file_name: logicalFileName,
      logical_file_name__regex: logicalFileNameRegex,
      status,
      min_size: !isNaN(minSize) ? parseInt(minSize) * 1024 ** 2 : undefined, // Transforming from MB (user input) to B
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

const fileIndexApi = {
  fileIndex: {
    statusList: FILE_INDEX_STATUSES,
    list: listFileIndex,
    count: countFileIndex,
  },
}

export default fileIndexApi
