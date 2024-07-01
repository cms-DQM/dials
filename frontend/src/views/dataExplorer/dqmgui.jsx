import React, { useState, useEffect } from 'react'

import Spinner from 'react-bootstrap/Spinner'
import { toast } from 'react-toastify'

import API from '../../services/api'

const DQMGui = () => {
  const datasetName = '/ZeroBias/Run2023C-PromptReco-v1/DQMIO'
  const runNumber = 367112

  const [ingestedMEs, setIngestedMEs] = useState()
  const [isLoadingMEs, setIsLoadingMEs] = useState(true)

  const fetchMEs = () => {
    setIsLoadingMEs(true)
    API.mes
      .list({})
      .then((data) => {
        setIngestedMEs(data)
        setIsLoadingMEs(false)
      })
      .catch((err) => {
        console.error(err)
        toast.error('Failure to communicate with the API!')
      })
  }

  useEffect(() => {
    fetchMEs()
  }, [])

  return (
    <>
      <h1>{datasetName}</h1>
      <h1>{runNumber}</h1>
      <h1>Monitoring Elements:</h1>
      {isLoadingMEs ? (
        <Spinner animation='border' role='status' />
      ) : (
        ingestedMEs.map((item) => {
          return <p key={item.me_id}>{item.me}</p>
        })
      )}
    </>
  )
}

export default DQMGui
