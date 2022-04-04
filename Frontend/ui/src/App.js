import './SignIn.js';
import React, { useState, useContext } from 'react'
import SignIn from './SignIn.js';
import NavBar from './NavBar.js'
import Tests from './Tests.js'
import Store from './Store.js'
import Accounts from './Accounts.js';
import Availability from './Availability.js';
import Schedule from './Schedule.js';
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { createTheme, ThemeProvider } from '@mui/material/styles';


const theme = createTheme();

const TokenContext = React.createContext('token')

function App() {
  const [globalAuthData, setGlobalAuthData] = useState([''])

  console.log("On the app page!")
  console.log(globalAuthData)
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
              <Route path='/Availability' element={<Availability />} />
              <Route path='/Schedule' element={<Schedule />}/>
            </Routes>
          </BrowserRouter>
        </ThemeProvider>
      </Store>
    </div>
  );
}

export default App;
