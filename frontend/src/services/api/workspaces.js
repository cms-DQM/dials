import { DIALS_API_URL } from '../../config/env'
import axiosApiInstance from './adapters'

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

const workspacesApi = {
  workspaces: {
    list: getWorkspaces,
    getUserDefaultWorkspace,
  },
}

export default workspacesApi
