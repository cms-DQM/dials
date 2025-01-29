import React, { useState, useEffect } from 'react'

import { BrowserRouter } from 'react-router-dom'
import { ToastContainer, toast } from 'react-toastify'

import keycloak from './services/keycloak'
import { SELECTED_WORKSPACE_KEY } from './config/env'
import API from './services/api'
import AppRoutes from './views/routes'
import AppNavbar from './views/components/navbar'

const Root = () => {
  const [selectedWorkspace, setSelectedWorkspace] = useState(null)
  const [allWorkspaces, setAllWorkspaces] = useState([])

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

    const fetchDefaultWorkspace = async () => {
      return API.config
        .getUserDefaultWorkspace()
        .then((response) => {
          return response.workspace
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
          return undefined
        })
    }

    if (keycloak.authenticated) {
      // if the workspace is already set in localStorage (from another tab, maybe)
      // we want to preserve that, since the user might have selected another workspace
      const currentWorkspace = localStorage.getItem(SELECTED_WORKSPACE_KEY)

      if (currentWorkspace) {
        setSelectedWorkspace(currentWorkspace)
      } else {
        fetchDefaultWorkspace().then(setSelectedWorkspace)
      }

      fetchWorkspaces()
    }
  }, [])

  useEffect(() => {
    if (selectedWorkspace) {
      localStorage.setItem(SELECTED_WORKSPACE_KEY, selectedWorkspace)
    }
  }, [selectedWorkspace])

  return (
    <BrowserRouter>
      <AppNavbar
        allWorkspaces={allWorkspaces}
        selectedWorkspace={selectedWorkspace}
        setSelectedWorkspace={setSelectedWorkspace}
      />
      <AppRoutes key={selectedWorkspace} />
      <ToastContainer position='bottom-right' />
    </BrowserRouter>
  )
}

export default Root
