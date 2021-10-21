import React, {useState, useEffect } from 'react'
import { BrowserRouter as Router, Switch, Route } from "./index";
import logo from './logo.svg';
import './App.css';
import "./index.css";
// import SearchIQS from './components/SearchIQS';
import SearchPage from './pages/SeachPage';




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
      {/* <header className="App-header">

      </header> */}
      {/* <h1> testing - {testObject}</h1> */}
      <SearchPage></SearchPage>
    </div>
  );
}

export default App;
