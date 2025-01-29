import React, { useState, useEffect } from 'react'

const KeycloakWrapper = ({
  keycloak,
  keycloakParams,
  onLogin,
  onRefresh,
  children,
}) => {
  const [authenticated, setAuthenticated] = useState(false)
  const [loginFailed, setLoginFailed] = useState(false)
  const [refreshFailed, setRefreshFailed] = useState(false)

  useEffect(() => {
    const initKeycloak = async () => {
      keycloak
        .init(keycloakParams)
        .then((auth) => {
          if (auth) {
            onLogin()
              .then(() => setAuthenticated(true))
              .catch(() => setLoginFailed(true))
          } else {
            setLoginFailed(true)
          }
        })
        .catch((error) => {
          console.error('Failed to authenticate:', error)
          setLoginFailed(true)
        })
    }

    if (!keycloak.didInitialize) {
      initKeycloak()
    }
  }, [keycloak, keycloakParams, onLogin])

  useEffect(() => {
    let refreshInterval

    const scheduleTokenRefresh = () => {
      refreshInterval = setInterval(async () => {
        keycloak
          .updateToken(60)
          .then((refreshed) => {
            if (refreshed) {
              onRefresh()
                .then(() => setRefreshFailed(false))
                .catch(() => setRefreshFailed(true))
            }
          })
          .catch((error) => {
            console.error('Failed to refresh token:', error)
            setRefreshFailed(true)
            clearInterval(refreshInterval)
          })
      }, 30000)
    }

    if (authenticated) {
      scheduleTokenRefresh()
    }

    return () => clearInterval(refreshInterval)
  }, [authenticated, keycloak, onRefresh])

  if (refreshFailed) {
    return (
      <div>
        Authentication refresh failed. Please, try refreshing your page.
      </div>
    )
  }

  if (loginFailed) {
    return <div>Authentication failed. Please, try refreshing your page.</div>
  }

  if (!authenticated) {
    return <div>Authenticating...</div>
  }

  return <>{children}</>
}

export default KeycloakWrapper
