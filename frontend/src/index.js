import 'bootstrap/dist/css/bootstrap.min.css'
import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css'
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css'
import 'react-toastify/dist/ReactToastify.css'

import React from 'react'

import ReactDOM from 'react-dom/client'
import { AuthProvider } from 'react-oidc-context'
import { BrowserRouter } from 'react-router-dom'

import oidcConfig from './config/oidc'
import Root from './root'

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <AuthProvider {...oidcConfig}>
      <BrowserRouter>
        <Root />
      </BrowserRouter>
    </AuthProvider>
  </React.StrictMode>
)
