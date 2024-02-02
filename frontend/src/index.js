import 'bootstrap/dist/css/bootstrap.min.css'
import 'react-bootstrap-range-slider/dist/react-bootstrap-range-slider.css'
import 'react-bootstrap-table-next/dist/react-bootstrap-table2.min.css'
import 'react-toastify/dist/ReactToastify.css'

import React from 'react'
import ReactDOM from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import Root from './root'

const root = ReactDOM.createRoot(document.getElementById('root'))
root.render(
  <React.StrictMode>
    <BrowserRouter>
      <Root />
    </BrowserRouter>
  </React.StrictMode>
)
