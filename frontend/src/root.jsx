import React, { useState, useEffect } from 'react'

import { ToastContainer, toast } from 'react-toastify'
import { useAuth } from 'react-oidc-context'

import {
  OIDC_CONFIDENTIAL_TOKEN_NS,
  OIDC_USER_WORKSPACE,
  EXCHANGED_TOKEN_EVT,
} from './config/env'
import { AppNavbar, AppRoutes } from './components'
import onSigninComplete from './utils/auth'
import { getUserWorkspace } from './utils/userTokens'
import API from './services/api'

const Root = () => {
  const auth = useAuth()
  const [silentSignin, setSilentSignin] = useState(false)
  const [tokenExchanged, setTokenExchanged] = useState(false)
  const [selectedWorkspace, setSelectedWorkspace] = useState(null)
  const [allWorkspaces, setAllWorkspaces] = useState([])

  // When user is redirected from SSO login, we capture this event
  // to finished authentication
  window.addEventListener(EXCHANGED_TOKEN_EVT, () => {
    setTokenExchanged(true)
  })

  // When user load the page in another tab but it was already authenticated from another session
  // `tokenExchanged` will not be set to true by the event, because the event ocurred in another window
  // then we check if the confidential token is present in the localStorage to set the value to true
  useEffect(() => {
    if (localStorage.getItem(OIDC_CONFIDENTIAL_TOKEN_NS) !== null) {
      setTokenExchanged(true)
    }
  }, [])

  useEffect(() => {
    return auth.events.addAccessTokenExpiring(() => {
      setSilentSignin(true)
      auth
        .signinSilent()
        .then(async (_user) => {
          await onSigninComplete({
            dispatchEvent: false,
          })
        })
        .catch((err) => {
          console.error(err)
        })
        .finally(() => {
          setSilentSignin(false)
        })
    })
  }, [silentSignin, auth, auth.events, auth.signinSilent])

  useEffect(() => {
    return auth.events.addAccessTokenExpired(() => {
      auth.removeUser()
      localStorage.removeItem(OIDC_CONFIDENTIAL_TOKEN_NS)
      window.location.href = '/'
    })
  }, [auth, auth.events, auth.signinSilent])

  useEffect(() => {
    const fetchWorkspaces = async () => {
      API.config
        .getWorkspaces()
        .then((response) => {
          setAllWorkspaces(response.workspaces)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
    }
    if (auth.isAuthenticated && tokenExchanged) {
      // if the workspace is already set in localStorage
      // we want to preserve that, since the user might have selected another workspace
      const currentWorkspace = localStorage.getItem(OIDC_USER_WORKSPACE)
      setSelectedWorkspace(currentWorkspace !== null ? currentWorkspace : getUserWorkspace())
      fetchWorkspaces()
    }
  }, [auth.isAuthenticated, tokenExchanged])

  useEffect(() => {
    if (selectedWorkspace) {
      localStorage.setItem(OIDC_USER_WORKSPACE, selectedWorkspace)
    }
  }, [selectedWorkspace])

  // Will render authenticating div if auth provider is still loading
  // or user is authenticated (auth not loading anymore) but
  // token hasn't been exchanged yet
  if (
    !silentSignin &&
    (auth.isLoading || (auth.isAuthenticated && !tokenExchanged))
  ) {
    return <div>Authenticating...</div>
  }

  if (auth.error) {
    return <div>Oops... {auth.error.message}</div>
  }

  return (
    <>
      <AppNavbar
        allWorkspaces={allWorkspaces}
        selectedWorkspace={selectedWorkspace}
        setSelectedWorkspace={setSelectedWorkspace}
      />
      <AppRoutes key={selectedWorkspace} />
      <ToastContainer position='bottom-right' />
    </>
  )
}

export default Root
