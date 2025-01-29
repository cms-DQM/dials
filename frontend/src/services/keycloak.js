import Keycloak from 'keycloak-js'

import { KEYCLOAK_URL, KEYCLOAK_REALM, KEYCLOAK_CLIENT_ID } from '../config/env'

const keycloak = new Keycloak({
  url: KEYCLOAK_URL,
  realm: KEYCLOAK_REALM,
  clientId: KEYCLOAK_CLIENT_ID,
})

keycloak.serviceTokens = {}

keycloak.getServiceToken = (serviceName) => {
  const service = keycloak.serviceTokens[serviceName]
  return {
    tokenType: service.tokenParsed.typ,
    accessToken: service.token,
    roles: service.tokenParsed.cern_roles,
  }
}

export default keycloak
