import { sanitizedURLSearchParams } from '../../utils'
import { DIALS_API_URL } from '../../config/env'
import axiosApiInstance from './adapters'

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

const thirdPartyProxiesApi = {
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

export default thirdPartyProxiesApi
