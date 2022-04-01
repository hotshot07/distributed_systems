import './SignIn.js';
import React from 'react'
import SignIn from './SignIn.js';
import NavBar from './NavBar.js'
import Tests from './Tests.js'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { createTheme, ThemeProvider } from '@mui/material/styles';

const theme = createTheme();

function App() {
  return (
    <div className="App">
      <ThemeProvider theme={theme}>
      <BrowserRouter>
      <NavBar />
      <Routes>
        <Route path="/" element={<SignIn />} />
        <Route path="/Tests" element={<Tests/>} />
      </Routes>
    </BrowserRouter>
    </ThemeProvider>
    </div>
  );
}

export default App;
