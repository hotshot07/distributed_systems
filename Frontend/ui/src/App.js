import './SignIn.js';
import React from 'react'
import SignIn from './SignIn.js';
import NavBar from './NavBar.js'
import HowTo from './HowTo.js'
import { BrowserRouter, Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className="App">
      <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/" element={<SignIn />} />
        <Route path="/howto" element={<HowTo />} />
      </Routes>
    </BrowserRouter>
    </div>
  );
}

export default App;
