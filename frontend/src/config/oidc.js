import { WebStorageStateStore } from 'oidc-client-ts'

import {
  OIDC_AUTHORITY,
  OIDC_PUBLIC_CLIENT_ID,
  OIDC_SCOPE,
} from '../config/env'
import onSigninComplete from '../utils/auth'

// We need to always match the reidrect uri registered at CERN's application portal
const redirectUri = window.location.origin + '/'

// We are going to store public token in the localStorage
const userStore = new WebStorageStateStore({ store: window.localStorage })

// This function will execute after we receive the signin callback from CERN's auth page
const onSigninCallback = async (_user) => {
  window.history.replaceState({}, document.title, window.location.pathname)
  await onSigninComplete({
    subjectToken: _user.access_token,
    dispatchEvent: true,
  })
}

// OIDC configuration
const oidcConfig = {
  authority: OIDC_AUTHORITY,
  client_id: OIDC_PUBLIC_CLIENT_ID,
  scope: OIDC_SCOPE,
  redirect_uri: redirectUri,
  onSigninCallback,
  userStore,
}

export default oidcConfig
