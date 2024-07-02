import React, { useState, useEffect } from 'react'

import Spinner from 'react-bootstrap/Spinner'
import { toast } from 'react-toastify'

import API from '../../services/api'
import { pathsToJson } from '../../utils/sanitizer'

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
        const mesDir = pathsToJson(data.map((item) => item.me))
        setIngestedMEs(mesDir)
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
        <p>{JSON.stringify(ingestedMEs)}</p>
      )}
    </>
  )
}

export default DQMGui
