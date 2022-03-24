import './SignIn.js';
import React from 'react'
import SignIn from './SignIn.js';
import ResponsiveAppBar from './NavBar.js'

function App() {
  return (
    <div className="App">
      <ResponsiveAppBar />
      <SignIn />
    </div>
  );
}

export default App;
