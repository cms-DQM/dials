export const ENV = import.meta.env.VITE_APP_ENV ?? 'development'

const OPTIONS = {
  qa: {
    DIALS_API_URL: 'http://localhost:8000/api/v1',
    DIALS_API_AUDIENCE: 'cms-dials-qa-confidential-app',
    KEYCLOAK_URL: 'https://keycloak-qa.cern.ch/auth',
    KEYCLOAK_REALM: 'cern',
    KEYCLOAK_CLIENT_ID: 'cms-dials-qa-public-app',
    ROLE_DQM_HARDCORE: 'cms-dqm-hardcore',
  },
  development: {
    DIALS_API_URL: 'http://localhost:8000/api/v1',
    DIALS_API_AUDIENCE: 'cms-dials-dev-confidential-app',
    KEYCLOAK_URL: 'https://auth.cern.ch/auth',
    KEYCLOAK_REALM: 'cern',
    KEYCLOAK_CLIENT_ID: 'cms-dials-dev-public-app',
    ROLE_DQM_HARDCORE: 'cms-dqm-hardcore',
  },
  production: {
    DIALS_API_URL: 'https://cmsdials-api.web.cern.ch/api/v1',
    DIALS_API_AUDIENCE: 'cms-dials-prod-confidential-app',
    KEYCLOAK_URL: 'https://auth.cern.ch/auth',
    KEYCLOAK_REALM: 'cern',
    KEYCLOAK_CLIENT_ID: 'cms-dials-prod-public-app',
    ROLE_DQM_HARDCORE: 'cms-dqm-hardcore',
  },
}

export const DIALS_API_URL = OPTIONS[[ENV]].DIALS_API_URL
export const DIALS_API_AUDIENCE = OPTIONS[[ENV]].DIALS_API_AUDIENCE
export const KEYCLOAK_URL = OPTIONS[[ENV]].KEYCLOAK_URL
export const KEYCLOAK_REALM = OPTIONS[[ENV]].KEYCLOAK_REALM
export const KEYCLOAK_CLIENT_ID = OPTIONS[[ENV]].KEYCLOAK_CLIENT_ID
export const ROLE_DQM_HARDCORE = OPTIONS[[ENV]].ROLE_DQM_HARDCORE
export const API_SERVICES = [{ label: 'dials', aud: DIALS_API_AUDIENCE }]
