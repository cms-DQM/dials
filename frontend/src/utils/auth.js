import { OIDC_CONFIDENTIAL_TOKEN_NS, EXCHANGED_TOKEN_EVT } from '../config/env'
import API from '../services/api'

const onSigninComplete = async ({ dispatchEvent }) => {
  // Now that we are authenticated within the public app
  // exchange the token with the confidential app
  const apiToken = await API.auth.exchange()
  localStorage.setItem(OIDC_CONFIDENTIAL_TOKEN_NS, JSON.stringify(apiToken))

  if (dispatchEvent) {
    // Dispatch event browser event to notify that token was successfully exchanged
    // This event will be captured in the home page root page to check
    // if user finished the complete authentication flow (public -> exchange -> localStorage)
    window.dispatchEvent(new Event(EXCHANGED_TOKEN_EVT))
  }
}

export default onSigninComplete
