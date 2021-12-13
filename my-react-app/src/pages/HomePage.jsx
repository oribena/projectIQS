import React, { Component } from 'react';
import 'my-react-app/node_modules/bootstrap/dist/css/bootstrap.min.css';
import Login from "../components/Login";
import logo2 from '../images/logo2.gif'
import '../components/home.css'

class Home extends React.Component {
    render() { 

        return <div className='body-container' style={{color:"#996633"}}>
                <h1>Iterative Query Selection</h1>
                <hr></hr>
                <div id="wrapper">
                <br></br>
                <div id="two"><img src={logo2} alt="loading..." /></div>
                <div id="one"><Login ></Login></div>
                </div>
                </div>;
    }
}
 
export default Home;