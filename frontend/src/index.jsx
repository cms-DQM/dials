import 'bootstrap/dist/css/bootstrap.min.css'
import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css'
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css'
import 'react-toastify/dist/ReactToastify.css'

import React from 'react'
import ReactDOM from 'react-dom/client'

import keycloak from './services/keycloak'
import { onLogin, onRefresh } from './services/keycloakServices'
import KeycloakWrapper from './keycloakWrapper'
import Root from './root'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <KeycloakWrapper
      keycloak={keycloak}
      keycloakParams={{ onLoad: 'login-required' }}
      onLogin={onLogin}
      onRefresh={onRefresh}
    >
      <Root />
    </KeycloakWrapper>
  </React.StrictMode>
)
