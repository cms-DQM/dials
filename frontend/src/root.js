import React, { useState, useEffect } from 'react'

import { Routes, Route } from 'react-router-dom'
import { ToastContainer } from 'react-toastify'
import { useAuth } from 'react-oidc-context'

import { OIDC_CONFIDENTIAL_TOKEN_NS } from './config/env'
import { Navbar, PrivateRoute } from './components'
import Views from './views'
import API from './services/api'

// Note on `PrivateRoute`
//
// From the component src code you can see that you can
// restrict user access based on applications-portal roles
// just add the parameter "roles={['role-name']}" to a private route
// and users without that role will see a permission denied modal and be redirected to home
//
// Example (based on applications-portal-qa), only users in viz-role will load that component:
// <PrivateRoute roles={['viz-role']} component={Views.DataExplorer.Histograms2D} />

const Root = () => {
  const auth = useAuth()
  const [tokenExchanged, setTokenExchanged] = useState(false)

  window.addEventListener('confidential-token-stored', () => {
    setTokenExchanged(true)
  })

  useEffect(() => {
    return auth.events.addAccessTokenExpiring(() => {
      auth.signinSilent()
        .then(async (_user) => {
          const apiToken = await API.auth.exchange({ subjectToken: _user.access_token })
          localStorage.setItem(OIDC_CONFIDENTIAL_TOKEN_NS, JSON.stringify(apiToken))
        })
        .catch(err => {
          console.error(err)
        })
    })
  }, [auth.events, auth.signinSilent])

  useEffect(() => {
    return auth.events.addAccessTokenExpired(() => {
      auth.removeUser()
      localStorage.removeItem(OIDC_CONFIDENTIAL_TOKEN_NS)
      window.location.href = '/'
    })
  }, [auth.events, auth.signinSilent])

  return (
    <>
      {
        !auth.isLoading || tokenExchanged
          ? (
            <>
              <Navbar />
              <Routes>
                <Route path='/' element={<Views.Home.Index />} />
                <Route path='/ingest' element={<PrivateRoute component={Views.DataIngestion.Index} />} />
                <Route path='/file-index' element={<PrivateRoute component={Views.DataExplorer.FileIndex} />} />
                <Route path='/runs'>
                  <Route index element={<PrivateRoute component={Views.DataExplorer.Runs} />} />
                  <Route path=':runNumber' element={<PrivateRoute component={Views.DataExplorer.Run} />} />
                </Route>
                <Route path='/lumisections'>
                  <Route index element={<PrivateRoute component={Views.DataExplorer.Lumisections} />} />
                  <Route path=':id' element={<PrivateRoute component={Views.DataExplorer.Lumisection} />} />
                </Route>
                <Route path='/histograms-1d'>
                  <Route index element={<PrivateRoute component={Views.DataExplorer.Histograms1D} />} />
                  <Route path=':id' element={<PrivateRoute component={Views.DataExplorer.Histogram} dim={1} />} />
                </Route>
                <Route path='/histograms-2d'>
                  <Route index element={<PrivateRoute component={Views.DataExplorer.Histograms2D} />} />
                  <Route path=':id' element={<PrivateRoute component={Views.DataExplorer.Histogram} dim={2} />} />
                </Route>
                <Route path='/create' element={<PrivateRoute component={Views.MachineLearning.CreatePipelines} />} />
                <Route path='/train' element={<PrivateRoute component={Views.MachineLearning.RunPipelines} />} />
                <Route path='/predict' element={<PrivateRoute component={Views.MachineLearning.ModelPredict} />} />
              </Routes>
              <ToastContainer
                position='bottom-right'
              />
            </>
            )
          : (
            <div>Authenticating...</div>
            )
      }
    </>
  )
}

export default Root
