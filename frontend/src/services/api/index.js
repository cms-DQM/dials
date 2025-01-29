import { sanitizedURLSearchParams, getNextToken } from '../../utils/sanitizer'
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

const getWorkspaces = async () => {
  const endpoint = `${DIALS_API_URL}/auth/workspaces/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

const getUserDefaultWorkspace = async () => {
  const endpoint = `${DIALS_API_URL}/auth/user-default-workspace/`
  const response = await axiosApiInstance.get(endpoint)
  return response.data
}

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

const getLumisection = async ({
  datasetId,
  runNumber,
  lsNumber,
  workspace,
}) => {
  const endpoint = `${DIALS_API_URL}/run/${datasetId}/${runNumber}/${lsNumber}/`
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

const getCAFJson = async ({ className, kind }) => {
  const endpoint = `${DIALS_API_URL}/caf/`
  const params = sanitizedURLSearchParams(
    {
      class_name: className,
      kind,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const listRREditableDatasets = async ({
  className,
  datasetName,
  globalState,
}) => {
  const endpoint = `${DIALS_API_URL}/runregistry/editable-datasets/`
  const params = sanitizedURLSearchParams(
    {
      class_name: className,
      dataset_name: datasetName,
      global_state: globalState,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const getBrilcalcLumi = async ({
  brilwsVersion,
  connect,
  fillNum,
  runNumber,
  beamStatus,
  unit,
  aModeTag,
  normTag,
  begin,
  end,
  byLs,
  scope,
}) => {
  const endpoint = `${DIALS_API_URL}/brilws/brilcalc-lumi/`
  const params = sanitizedURLSearchParams(
    {
      brilws_version: brilwsVersion,
      connect,
      fillnum: fillNum,
      runnumber: runNumber,
      beamstatus: beamStatus,
      unit,
      amodetag: aModeTag,
      normtag: normTag,
      begin,
      end,
      byls: byLs,
      scope,
    },
    { repeatMode: false }
  )
  const response = await axiosApiInstance.get(endpoint, {
    params,
  })
  return response.data
}

const genericFetchAllPages = async ({ apiMethod, params = {} }) => {
  const allData = []
  let nextPageExists = true
  let nextToken = null
  let errorCount = 0
  let totalPages = 0
  while (nextPageExists) {
    totalPages++
    try {
      const { results, next } = await apiMethod({
        nextToken,
        ...params,
      })
      results.forEach((e) => allData.unshift(e))
      nextPageExists = !(next === null)
      nextToken = getNextToken({ next }, 'next')
    } catch (err) {
      errorCount++
    }
  }

  return {
    results: allData,
    count: allData.length,
    error: errorCount,
    totalPages,
  }
}

const API = {
  utils: {
    genericFetchAllPages,
  },
  config: {
    getWorkspaces,
    getUserDefaultWorkspace,
  },
  dataset: {
    get: getDataset,
    list: listDatasets,
  },
  fileIndex: {
    statusList: FILE_INDEX_STATUSES,
    list: listFileIndex,
    count: countFileIndex,
  },
  run: {
    get: getRun,
    list: listRuns,
    count: countRuns,
  },
  lumisection: {
    get: getLumisection,
    list: listLumisections,
    count: countLumisections,
  },
  mes: {
    list: listMEs,
    listByRun: listMEsByRun,
  },
  histogram: {
    get: getHistogram,
    list: listHistograms,
  },
  mlModelsIndex: {
    list: listMLModelsIndex,
  },
  mlBadLumis: {
    list: listMLBadLumisections,
    certJson: getMLCertificationJson,
    goldenJson: getMLGoldenJson,
  },
  caf: {
    get: getCAFJson,
  },
  runregistry: {
    editableDatasets: {
      list: listRREditableDatasets,
    },
  },
  brilws: {
    brilcalc: {
      lumi: getBrilcalcLumi,
    },
  },
}

export default API
