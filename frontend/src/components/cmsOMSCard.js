import React from 'react'

import Card from 'react-bootstrap/Card'
import Spinner from 'react-bootstrap/Spinner'

const CMSOMSCard = (props) => {
  const { isLoading, runNumber } = props

  return (
    <Card>
      <Card.Header>More from OMS</Card.Header>
      <Card.Body>
      {
        isLoading
          ? (
            <Spinner
            animation='border'
            role='status'
          />
            )
          : (
            <>
            <Card.Text>
              <a
                href={`https://cmsoms.cern.ch/cms/runs/report?cms_run=${runNumber}`}
                target='_blank'
                rel='noopener noreferrer'
              >
                {`Run ${runNumber}`}
              </a>
            </Card.Text>
            <Card.Text>
              <a
                href={`https://cmsoms.cern.ch/cms/triggers/l1_rates?cms_run=${runNumber}`}
                target='_blank'
                rel='noopener noreferrer'
              >
                {`L1 rates from run ${runNumber}`}
              </a>
            </Card.Text>
            <Card.Text>
              <a
                href={`https://cmsoms.cern.ch/cms/triggers/hlt_trigger_rates?cms_run=${runNumber}`}
                target='_blank'
                rel='noopener noreferrer'
              >
                {`HLT rates from run ${runNumber}`}
              </a>
            </Card.Text>
            </>
            )
      }
      </Card.Body>
    </Card>
  )
}

export default CMSOMSCard
