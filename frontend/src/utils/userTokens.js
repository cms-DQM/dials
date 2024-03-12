import { User } from 'oidc-client-ts'

import { OIDC_PUBLIC_TOKEN_NS, OIDC_CONFIDENTIAL_TOKEN_NS } from '../config/env'

export const getPublicToken = () => {
  const oidcStorage = localStorage.getItem(OIDC_PUBLIC_TOKEN_NS)
  if (!oidcStorage) {
    throw new Error('User is not authenticated!')
  }
  const user = User.fromStorageString(oidcStorage)
  return {
    tokenType: user.token_type,
    accessToken: user.access_token,
  }
}

export const getConfidentialToken = () => {
  const oidcStorage = localStorage.getItem(OIDC_CONFIDENTIAL_TOKEN_NS)
  if (!oidcStorage) {
    throw new Error('User is not authenticated!')
  }
  const user = JSON.parse(oidcStorage)
  return {
    tokenType: user.token_type,
    accessToken: user.access_token,
    expiresIn: user.expires_in,
  }
}
