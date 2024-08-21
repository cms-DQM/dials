import axios from 'axios'

import { getConfidentialToken } from '../../utils/userTokens'
import { OIDC_USER_WORKSPACE } from '../../config/env'

const axiosApiInstance = axios.create()
axiosApiInstance.interceptors.request.use(
  async (config) => {
    const oidc = getConfidentialToken()
    config.headers = {
      Authorization: `${oidc.tokenType} ${oidc.accessToken}`,
      Accept: 'application/json',
      Workspace:
        config?.headers?.Workspace || localStorage.getItem(OIDC_USER_WORKSPACE),
    }
    return config
  },
  (error) => {
    Promise.reject(error)
  }
)

export { axiosApiInstance }
