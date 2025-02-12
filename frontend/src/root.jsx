import React, { useState, useEffect, useRef } from 'react'

import { useSearchParams } from 'react-router-dom'
import { ToastContainer, toast } from 'react-toastify'

import keycloak from './services/keycloak'
import API from './services/api'
import AppRoutes from './views/routes'
import AppNavbar from './views/components/navbar'

const Root = () => {
  const [selectedWorkspace, setSelectedWorkspace] = useState(null)
  const [allWorkspaces, setAllWorkspaces] = useState([])
  const [searchParams, setSearchParams] = useSearchParams()
  const workspaceFromUrl = useRef(searchParams.get('ws'))

  useEffect(() => {
    const fetchWorkspaces = async () => {
      API.workspaces
        .list()
        .then((response) => {
          setAllWorkspaces(response.workspaces)
        })
        .catch((error) => {
          console.error(error)
          toast.error('Failure to communicate with the API!')
        })
    }

    const fetchDefaultWorkspace = async () => {
      return API.workspaces
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
      if (workspaceFromUrl.current) {
        setSelectedWorkspace(workspaceFromUrl.current)
      } else {
        fetchDefaultWorkspace().then(setSelectedWorkspace)
      }

      fetchWorkspaces()
    }
  }, [])

  useEffect(() => {
    if (selectedWorkspace) {
      searchParams.set('ws', selectedWorkspace)
      setSearchParams(searchParams)
    }
  }, [selectedWorkspace, searchParams, setSearchParams])

  return (
    <>
      <AppNavbar
        allWorkspaces={allWorkspaces}
        selectedWorkspace={selectedWorkspace}
        onWorkspaceChange={setSelectedWorkspace}
      />
      {
        // The key parameter is not explicitly used in the AppRoutes component,
        // however, it is needed to re-render this component whenever this state
        // changes.
      }
      <AppRoutes key={selectedWorkspace}/>
      <ToastContainer position='bottom-right' />
    </>
  )
}

export default Root
