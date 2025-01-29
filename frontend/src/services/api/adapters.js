import axios from 'axios'

import keycloak from '../keycloak'
import { SELECTED_WORKSPACE_KEY } from '../../config/env'

const axiosApiInstance = axios.create()

axiosApiInstance.interceptors.request.use(
  async (config) => {
    const serviceToken = keycloak.getServiceToken('dials')
    config.headers = {
      Authorization: `${serviceToken.tokenType} ${serviceToken.accessToken}`,
      Accept: 'application/json',
      Workspace:
        config?.headers?.Workspace ||
        localStorage.getItem(SELECTED_WORKSPACE_KEY),
    }
    return config
  },
  (error) => {
    Promise.reject(error)
  }
)

export default axiosApiInstance
