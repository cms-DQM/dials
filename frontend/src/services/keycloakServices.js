import { DIALS_API_AUDIENCE } from '../config/env'
import keycloak from './keycloak'
import KeycloakExchange from './keycloakExchange'

const onLogin = async () => {
  const serviceLogin = new KeycloakExchange({
    url: keycloak.authServerUrl,
    realm: keycloak.realm,
    clientId: keycloak.clientId,
    subjectToken: keycloak.token,
    targetAudience: DIALS_API_AUDIENCE,
  })

  await serviceLogin
    .exchangeToken()
    .then((response) => {
      serviceLogin.setToken(response.access_token)
    })
    .catch((err) => {
      console.error('Keycloak token exchange failed:', err)
    })
    .finally(() => {
      keycloak.serviceTokens.dials = serviceLogin
    })
}

const onRefresh = async () => {
  const serviceRefresh = new KeycloakExchange({
    url: keycloak.authServerUrl,
    realm: keycloak.realm,
    clientId: keycloak.clientId,
    subjectToken: keycloak.token,
    targetAudience: DIALS_API_AUDIENCE,
  })

  await serviceRefresh
    .exchangeToken()
    .then((response) => {
      serviceRefresh.setToken(response.access_token)
    })
    .catch((err) => {
      console.error('Keycloak token exchange failed:', err)
    })
    .finally(() => {
      keycloak.serviceTokens.dials = serviceRefresh
    })
}

export { onLogin, onRefresh }
