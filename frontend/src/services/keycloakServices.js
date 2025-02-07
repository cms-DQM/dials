import { API_SERVICES } from '../config/env'
import keycloak from './keycloak'
import KeycloakExchange from './keycloakExchange'

const handleExchange = async (service) => {
  const keycloakExchange = new KeycloakExchange({
    url: keycloak.authServerUrl,
    realm: keycloak.realm,
    clientId: keycloak.clientId,
    subjectToken: keycloak.token,
    targetAudience: service.aud,
  })

  await keycloakExchange
    .exchangeToken()
    .then((response) => {
      keycloakExchange.setToken(response.access_token)
    })
    .catch((err) => {
      console.error('Keycloak token exchange failed:', err)
    })
    .finally(() => {
      keycloak.serviceTokens[service.label] = keycloakExchange
    })
}

const onLogin = async () => {
  // Callback function to be executed after keycloak.init()
  // in case the authentication was successfull
  await Promise.all(API_SERVICES.map(async (srv) => handleExchange(srv)))
}

const onRefresh = async () => {
  // Callback function to be executed after keycloak.refresh()
  // in case the token was refreshed.
  //
  // We do not need a separate onRefresh function, since it is
  // identical to the onLogin function.
  // However, let's keep it here in case we want to do any fancy
  // operations specifically when token refreshes in the future.
  await Promise.all(API_SERVICES.map(async (srv) => handleExchange(srv)))
}

export { onLogin, onRefresh }
