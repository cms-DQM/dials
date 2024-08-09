import React from 'react'

import { useAuth } from 'react-oidc-context'
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button'

const PrivateRoute = ({ roles, component: Component, ...props }) => {
  // Methods hasRealmRole and hasResourceRole inspired from keycloak-js
  // Src code: https://github.com/keycloak/keycloak/blob/main/js/libs/keycloak-js/src/keycloak.js

  const auth = useAuth()
  const kc = auth.user?.profile
  const clientId = auth.settings.client_id

  const hasRealmRole = (role) => {
    const access = kc.cern_roles
    return !!access && access.indexOf(role) >= 0
  }

  const hasResourceRole = ({ role, resource }) => {
    if (!kc.resource_access) {
      return false
    }
    const access = kc.resource_access[resource || clientId]
    return !!access && access.roles.indexOf(role) >= 0
  }

  const validateRoles = (roles) => {
    return roles.some((r) => {
      const realm = hasRealmRole(r)
      const resource = hasResourceRole(r)
      return realm || resource
    })
  }

  const isAuthorized = (roles) => {
    return auth.isAuthenticated && (roles === undefined || validateRoles(roles))
  }

  return isAuthorized(roles) ? (
    <Component {...props} />
  ) : (
    <Modal show={true}>
      <Modal.Header>
        <Modal.Title>Permission denied</Modal.Title>
      </Modal.Header>
      <Modal.Body>
        {auth.isAuthenticated
          ? 'It seems you don\'t have the required role to access this resource, please ask your administrator.'
          : 'You are not authenticated.'}
      </Modal.Body>
      <Modal.Footer>
        <Button
          type='submit'
          onClick={() => {
            window.location.href = '/'
          }}
        >
          Go back to Home
        </Button>
      </Modal.Footer>
    </Modal>
  )
}

export default PrivateRoute
