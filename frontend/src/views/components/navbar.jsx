import React, { useState } from 'react'

import { NavLink } from 'react-router-dom'
import Navbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import NavDropdown from 'react-bootstrap/NavDropdown'
import Image from 'react-bootstrap/Image'
import Button from 'react-bootstrap/Button'
import Modal from 'react-bootstrap/Modal'

import keycloak from '../../services/keycloak'
import logo from '../../assets/img/logo.png'

const AppNavbar = ({
  allWorkspaces,
  selectedWorkspace,
  setSelectedWorkspace,
}) => {
  const [showLogoutModal, setShowLogoutModal] = useState(false)

  return (
    <Navbar expand='lg' bg='dark' variant='dark' sticky='top'>
      <Navbar.Brand as={NavLink} to='/'>
        <Image
          src={logo}
          height='30vmin'
          className='d-inline-block align-top ms-3'
          alt='Home'
        />{' '}
        <Navbar.Text>DIALS</Navbar.Text>
      </Navbar.Brand>
      <Navbar.Toggle aria-controls='basic-navbar-nav' />
      <Navbar.Collapse
        id='basic-navbar-nav'
        className='justify-content-end me-3'
      >
        <Nav className='me-auto'>
          <Nav.Link as={NavLink} to='/overview'>
            Overview
          </Nav.Link>
          <Nav.Link as={NavLink} to='/browser'>
            Browser
          </Nav.Link>
          <NavDropdown title='Data Explorer'>
            <NavDropdown.Item as={NavLink} to='/file-index'>
              Indexed files
            </NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item as={NavLink} to='/histograms-1d'>
              Histograms 1D
            </NavDropdown.Item>
            <NavDropdown.Item as={NavLink} to='/histograms-2d'>
              Histograms 2D
            </NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item as={NavLink} to='/runs'>
              Runs
            </NavDropdown.Item>
            <NavDropdown.Item as={NavLink} to='/lumisections'>
              Lumisections
            </NavDropdown.Item>
          </NavDropdown>
          <NavDropdown title='Machine Learning'>
            <NavDropdown.Item as={NavLink} to='/json-portal'>
              Json Portal
            </NavDropdown.Item>
            <NavDropdown.Item as={NavLink} to='/predictions'>
              Predictions
            </NavDropdown.Item>
          </NavDropdown>
        </Nav>
        <Nav>
          <NavDropdown title={`Using workspace: ${selectedWorkspace}`}>
            {allWorkspaces.map((workspace) => (
              <NavDropdown.Item
                key={`workspace-item-${workspace}`}
                onClick={() => setSelectedWorkspace(workspace)}
              >
                {workspace}
              </NavDropdown.Item>
            ))}
          </NavDropdown>
          <Nav.Link className='me-3'>Signed in as: {keycloak.subject}</Nav.Link>
          <Button type='submit' onClick={() => setShowLogoutModal(true)}>
            Logout
          </Button>
          <Modal show={showLogoutModal}>
            <Modal.Header>
              <Modal.Title>Logout</Modal.Title>
            </Modal.Header>
            <Modal.Body>Are you sure that you want to logout?</Modal.Body>
            <Modal.Footer>
              <Button
                variant='secondary'
                onClick={() => setShowLogoutModal(false)}
              >
                No
              </Button>
              <Button variant='primary' onClick={() => keycloak.logout()}>
                Yes
              </Button>
            </Modal.Footer>
          </Modal>
        </Nav>
      </Navbar.Collapse>
    </Navbar>
  )
}

export default AppNavbar
