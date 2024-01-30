import React from 'react'
import { NavLink } from 'react-router-dom'
import BootstrapNavbar from 'react-bootstrap/Navbar'
import Nav from 'react-bootstrap/Nav'
import NavDropdown from 'react-bootstrap/NavDropdown'
import Image from 'react-bootstrap/Image'

import logo from '../assets/img/logo.svg'

const Navbar = () => {
  return (
    <BootstrapNavbar expand='lg' bg='dark' variant='dark' sticky='top'>
      <BootstrapNavbar.Brand as={NavLink} to='/'>
        <Image src={logo} height='40vmin' className='d-inline-block align-top' alt='Home'/>
      </BootstrapNavbar.Brand>
      <BootstrapNavbar.Toggle aria-controls='basic-navbar-nav' />
      <BootstrapNavbar.Collapse id='basic-navbar-nav'>
        <Nav className='me-auto'>
          <Nav.Link as={NavLink} to='/ingest'>Data Ingestion</Nav.Link>
          <NavDropdown title='Data Explorer'>
            <NavDropdown.Item as={NavLink} to='/file-index'>Indexed files</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item as={NavLink} to='/histograms-1d'>Histograms 1D</NavDropdown.Item>
            <NavDropdown.Item as={NavLink} to='/histograms-2d'>Histograms 2D</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item as={NavLink} to='/runs'>Runs</NavDropdown.Item>
            <NavDropdown.Item as={NavLink} to='/lumisections'>Lumisections</NavDropdown.Item>
          </NavDropdown>
          <NavDropdown title='Machine Learning'>
            <NavDropdown.Item as={NavLink} to='/create'>Create</NavDropdown.Item>
            <NavDropdown.Item as={NavLink} to='/train'>Train</NavDropdown.Item>
            <NavDropdown.Item as={NavLink} to='/predict'>Predict</NavDropdown.Item>
          </NavDropdown>
        </Nav>
      </BootstrapNavbar.Collapse>
    </BootstrapNavbar>
  )
}

export default Navbar
