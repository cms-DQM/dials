export const ENV = import.meta.env.VITE_APP_ENV ?? 'development'

const OPTIONS = {
  qa: {
    API_URL: 'http://localhost:8000/api/v1',
    OIDC_AUTHORITY: 'https://keycloak-qa.cern.ch/auth/realms/cern/',
    OIDC_PUBLIC_CLIENT_ID: 'cms-dials-public-app',
    OIDC_SCOPE: 'openid profile email',
  },
  development: {
    API_URL: 'http://localhost:8000/api/v1',
    OIDC_AUTHORITY: 'https://auth.cern.ch/auth/realms/cern/',
    OIDC_PUBLIC_CLIENT_ID: 'cms-dials-dev-public-app',
    OIDC_SCOPE: 'openid profile email',
  },
  production: {
    API_URL: 'https://cmsdials-api.web.cern.ch/api/v1',
    OIDC_AUTHORITY: 'https://auth.cern.ch/auth/realms/cern/',
    OIDC_PUBLIC_CLIENT_ID: 'cms-dials-public-app',
    OIDC_SCOPE: 'openid profile email',
  },
}

export const API_URL = OPTIONS[[ENV]].API_URL
export const OIDC_AUTHORITY = OPTIONS[[ENV]].OIDC_AUTHORITY
export const OIDC_PUBLIC_CLIENT_ID = OPTIONS[[ENV]].OIDC_PUBLIC_CLIENT_ID
export const OIDC_SCOPE = OPTIONS[[ENV]].OIDC_SCOPE
export const OIDC_PUBLIC_TOKEN_NS = `oidc.user:${OIDC_AUTHORITY}:${OIDC_PUBLIC_CLIENT_ID}`
export const OIDC_CONFIDENTIAL_TOKEN_NS = `oidc.user.confidential:${OIDC_AUTHORITY}:${OIDC_PUBLIC_CLIENT_ID}`
export const EXCHANGED_TOKEN_EVT = 'confidential-token-stored'
export const OIDC_USER_WORKSPACE = 'oidc.user.workspace'
