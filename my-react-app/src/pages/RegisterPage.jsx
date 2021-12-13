import React, { Component } from 'react';
// import '../components/searchIQS.css'
import '../components/form.css'
import {Card} from 'react-bootstrap'
import register from "../components/register";

class Register extends React.Component {
    render() { 

        return <div className='body-container' style={{color:"#996633"}}>
                {/* <register></register> */}

                <center>
                <Card style={{ width: '30rem' }}>
                <Card.Body>
            <h1>Register</h1>
            <form>
                <br></br>
                <center>
                <div className="form-group">
                    <label>User Name</label>
                    <input type="text" className="form-control" placeholder="Enter user name" style={{width:"20rem"}} />
                </div>
                <br></br>
                <div className="form-group">
                    <label>Password</label>
                    <input type="password" className="form-control" placeholder="Enter password" style={{width:"20rem"}}/>
                </div>
                <br></br>
                <button class="button" type="submit" >Sign in</button>
                <br></br>
                <p className="forgot-password text-right">
                you are already registered yet? Go to <a href="/LogIn">Log In</a>
                </p>
                </center>
            </form>
            </Card.Body>
            </Card>
            </center>

        </div>;
    }
}
 
export default Register;