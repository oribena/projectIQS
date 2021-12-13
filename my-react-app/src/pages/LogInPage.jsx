import React, { Component } from 'react';
// import '../components/searchIQS.css'
import '../components/form.css'
import Login from "../components/Login";

class LogIn extends React.Component {
    render() { 

        return <div className='body-container' style={{color:"#996633"}}>
                <Login ></Login>

                {/* <h1>Log In</h1>
                <form>
                <br></br>
                <center>
                <div className="form-group">
                    <label>User Name</label>
                    <input type="text" className="form-control" placeholder="Enter user name" style={{width:"30%"}} />
                </div>
                <br></br>
                <div className="form-group">
                    <label>Password</label>
                    <input type="password" className="form-control" placeholder="Enter password" style={{width:"30%"}}/>
                </div>
                <br></br>
                <button class="button" type="submit" >Sign in</button>
                <br></br>
                <p className="forgot-password text-right">
                you are not registered yet? Go to <a href="/Register">Register</a>
                </p>
                </center>
            </form> */}

                </div>;
    }
}
 
export default LogIn;