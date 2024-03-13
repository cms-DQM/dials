import React, { useState, useEffect } from 'react'

import { ToastContainer } from 'react-toastify'
import { useAuth } from 'react-oidc-context'

import { OIDC_CONFIDENTIAL_TOKEN_NS, EXCHANGED_TOKEN_EVT } from './config/env'
import { AppNavbar, AppRoutes } from './components'
import onSigninComplete from './utils/auth'

const Root = () => {
  const auth = useAuth()
  const [tokenExchanged, setTokenExchanged] = useState(false)

  window.addEventListener(EXCHANGED_TOKEN_EVT, () => {
    setTokenExchanged(true)
  })

  useEffect(() => {
    return auth.events.addAccessTokenExpiring(() => {
      auth
        .signinSilent()
        .then(async (_user) => {
          await onSigninComplete({
            subjectToken: _user.access_token,
            dispatchEvent: false,
          })
        })
        .catch((err) => {
          console.error(err)
        })
    })
  }, [auth, auth.events, auth.signinSilent])

  useEffect(() => {
    return auth.events.addAccessTokenExpired(() => {
      auth.removeUser()
      localStorage.removeItem(OIDC_CONFIDENTIAL_TOKEN_NS)
      window.location.href = '/'
    })
  }, [auth, auth.events, auth.signinSilent])

  // Will render authenticating div if auth provider is still loading
  // or user is authenticated (auth not loading anymore) but
  // token hasn't been exchanged yet
  if (auth.isLoading || (auth.isAuthenticated && !tokenExchanged)) {
    return <div>Authenticating...</div>
  }

  if (auth.error) {
    return <div>Oops... {auth.error.message}</div>
  }

  return (
    <>
      <AppNavbar />
      <AppRoutes />
      <ToastContainer position='bottom-right' />
    </>
  )
}

export default Root
