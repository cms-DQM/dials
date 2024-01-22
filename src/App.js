import { Routes, Route } from 'react-router-dom';
import { NavLink } from 'react-router-dom';
import { Navbar, Nav, NavDropdown } from 'react-bootstrap';

import logo from './assets/img/logo.svg';
import Home from './components/Home';

function App() {
  return (
    <>
      <Navbar expand="lg" className="bg-dark" variant="dark" sticky="top">
        <Navbar.Brand as={NavLink} to='/'>
          <img
            src={logo}
            height="40vmin"
            className="d-inline-block align-top"
            alt="Home"
          />
        </Navbar.Brand>
        <Navbar.Toggle aria-controls="basic-navbar-nav" />
        <Navbar.Collapse id="basic-navbar-nav">
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
        </Navbar.Collapse>
      </Navbar>
      <Routes>
        <Route path="/" element={<Home />} />
      </Routes>
    </>
  );
}

export default App;
