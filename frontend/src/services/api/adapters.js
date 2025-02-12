import axios from 'axios'

import keycloak from '../keycloak'

const axiosApiInstance = axios.create()

axiosApiInstance.interceptors.request.use(
  async (config) => {
    const serviceToken = keycloak.getServiceToken('dials')

    // Parse the current URL to get the workspace query parameter
    const urlParams = new URLSearchParams(window.location.search)
    const workspaceFromUrl = urlParams.get('ws')

    config.headers = {
      Authorization: `${serviceToken.tokenType} ${serviceToken.accessToken}`,
      Accept: 'application/json',
      Workspace: config?.headers?.Workspace || workspaceFromUrl,
    }
    return config
  },
  (error) => {
    Promise.reject(error)
  }
)

export default axiosApiInstance
