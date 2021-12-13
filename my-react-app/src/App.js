import React, {useState, useEffect } from 'react'
import { BrowserRouter } from "./index";
import { Routes ,Route } from 'react-router-dom';
import logo from './logo.svg';
// import { BrowserRouter } from 'react-router-dom';
import Register from './pages/RegisterPage'
import './App.css';
import "./index.css";
// import SearchIQS from './components/SearchIQS';
import SearchPage from './pages/SearchPage';
import HomePage from './pages/HomePage';
import LogInPage from './pages/LogInPage';


import {Navbar, Nav, Container, NavDropdown} from 'react-bootstrap/'




function App()  {
  const [testObject, setTestObject] = useState(0);
  // happens when the page renders
  useEffect(()=> {
    fetch('/test').then(res => res.json()).then(data => {
      setTestObject(data.test)
    })
  },[]);

  return (
    <div className="App">

   

      <div class="nav"style={{position: "sticky", top:0, fontSize: 22, backgroundColor:"#ffcc99"}}>
  <Navbar style={{position: "sticky", top:0}} class="navbar navbar-custom" expand="lg" >
    <Container fluid>
      <Navbar.Brand href="/Home" style={{fontSize: 23, color:"#996633"}}>IQS Search<br></br></Navbar.Brand>
      <Navbar.Toggle aria-controls="navbarScroll" />
      <Navbar.Collapse id="navbarScroll">
        <Nav
          // className="me-auto my-2 my-lg-0"
          
          navbarScroll
        >
          <Nav.Link style={{paddingLeft:"30px"}} href="/Search">Search</Nav.Link>
          {/* <Nav.Link style={{paddingLeft:"30px"}} href="/Login">Log in</Nav.Link> */}
          <NavDropdown style={{paddingLeft:"30px"}} title="Search Algorithms" id="navbarScrollingDropdown">
            <NavDropdown.Item href="#action3">Best IQS</NavDropdown.Item>
            <NavDropdown.Item href="#action4">Lame ALMIK</NavDropdown.Item>
            <NavDropdown.Divider />
            <NavDropdown.Item href="#action5">
              Something else here
            </NavDropdown.Item>
          </NavDropdown>
          <NavDropdown style={{paddingLeft:"1000px"}} title="User" id="navbarScrollingDropdown">
            <NavDropdown.Item href="/LogIn">Login</NavDropdown.Item>
            <NavDropdown.Item href="/Register">Register</NavDropdown.Item>
            <NavDropdown.Item href="#action4">History</NavDropdown.Item>
          </NavDropdown>
        </Nav>
      </Navbar.Collapse>
    </Container>
  </Navbar>
  </div>
  <Routes>
        <Route path='/' element={<HomePage/>} />
        <Route path='/Home' element={<HomePage/>} />
        <Route path='/Search' element={<SearchPage/>} />
        <Route exact path="/Register" element={<Register/>} />
        <Route path='/LogIn' element={<LogInPage/>} />

      </Routes>

        <br></br>
        {/* <HomePage></HomePage> */}
      </div>
    
  );
}

export default App;
