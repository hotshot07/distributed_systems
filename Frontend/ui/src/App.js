import './SignIn.js';
import React, { useState, useContext } from 'react'
import SignIn from './SignIn.js';
import NavBar from './NavBar.js'
import Tests from './Tests.js'
import Store from './Store.js'
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { createTheme, ThemeProvider } from '@mui/material/styles';
import Accounts from './Accounts.js';

const theme = createTheme();

const TokenContext = React.createContext('token')

function App() {
  const [globalAuthToken, setGlobalAuthToken] = useState([''])

  return (
    <div className="App">
      <Store>
        <ThemeProvider theme={theme}>
          <BrowserRouter>
            <NavBar />
            <Routes>
              <Route path="/" element={<SignIn />} />
              <Route path="/Tests" element={<Tests/>} />
              <Route path="/Accounts" element={<Accounts />} />
            </Routes>
          </BrowserRouter>
        </ThemeProvider>
      </Store>
    </div>
  );
}

export default App;
