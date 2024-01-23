import { NavLink } from 'react-router-dom';
import { default as BootstrapNavbar } from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import NavDropdown from 'react-bootstrap/NavDropdown';
import Image from 'react-bootstrap/Image';

import logo from '../assets/img/logo.svg';

const Navbar = () => {
  return (
    <BootstrapNavbar expand="lg" bg="dark" variant="dark" sticky="top">
      <BootstrapNavbar.Brand as={NavLink} to='/'>
        <Image src={logo} height="40vmin" className="d-inline-block align-top" alt="Home"/>
      </BootstrapNavbar.Brand>
      <BootstrapNavbar.Toggle aria-controls="basic-navbar-nav" />
      <BootstrapNavbar.Collapse id="basic-navbar-nav">
        <Nav className="me-auto">
          <Nav.Link as={NavLink} to="/ingest">Data Ingestion</Nav.Link>
          <NavDropdown title="Data Explorer">
            <NavDropdown.Item as={NavLink} to="/indexedFiles">Indexed files</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item as={NavLink} to="/histograms1d">Histograms 1D</NavDropdown.Item>
            <NavDropdown.Item as={NavLink} to="/histograms2d">Histograms 2D</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item as={NavLink} to="/runs">Runs</NavDropdown.Item>
            <NavDropdown.Item as={NavLink} to="/lumisections">Lumisections</NavDropdown.Item>
          </NavDropdown>
          <NavDropdown title="Machine Learning">
            <NavDropdown.Item as={NavLink} to="/train">Train</NavDropdown.Item>
            <NavDropdown.Item as={NavLink} to="/predict">Predict</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item as={NavLink} to="/history">History</NavDropdown.Item>
          </NavDropdown>
        </Nav>
      </BootstrapNavbar.Collapse>
    </BootstrapNavbar>
  )
};

export default Navbar;