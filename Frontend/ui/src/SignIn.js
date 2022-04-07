import React, { useRef, useState, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Buffer } from 'buffer';
import { TokenContext } from './Store';
import logo from './assets/Testerr-logos_transparent.png'

// MUI imports
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Box from '@mui/material/Box';
import Grid from '@mui/material/Grid';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Slide from '@mui/material/Slide';
import Alert from '@mui/material/Alert';
import { createTheme, ThemeProvider } from '@mui/material/styles';

// Networking
import axios from "axios";

const ENDPOINT = '20.224.88.180';
const PORT = '3000';

const theme = createTheme();

export default function SignIn() {
  const [globalAuthData, setGlobalAuthData] = useContext(TokenContext)
  const userRef = useRef('')
  const passRef = useRef('')
  const [loginError, setLoginError] = useState(false)
  const navigate = useNavigate();

  const handleSubmit = (event) => {
    event.preventDefault();

    const basicAuthAsToken = Buffer.from(`${userRef.current.value}:${passRef.current.value}`).toString('base64');
    const authorization = `Basic ${basicAuthAsToken}`
    
    axios.post(`http://${ENDPOINT}:${PORT}/login`, { crossDomain: true }, { headers: { "Authorization": authorization, crossDomain: true } })
      .then((response) => {
        setLoginError(false);
        setGlobalAuthData({
          token: response.data,
          loggedIn: true
        })
        if (globalAuthData['loggedIn'] === true && globalAuthData['token']) {
          navigate('/Tests')
        }

      })
      .catch((err) => {
        console.log(globalAuthData);
        setLoginError(true)
      })
  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Grid container sx={{ alignItems: 'center', }} justifyContent="center">
          <Box component="div" src={logo}>
            <img style={{ width: 300, height: 300 }} src={logo} alt="logo"/>
          </Box>
        </Grid>
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Typography component="h1" variant="h5">
            Sign in to Testrr
          </Typography>
          <Slide direction="up" in={loginError} mountOnEnter unmountOnExit>
            <Alert severity="error">Username or password not recognised.</Alert>
          </Slide>
          <Box noValidate sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="email"
              label="Email Address"
              name="email"
              autoComplete="email"
              inputRef={userRef}
              autoFocus
            />
            <TextField
              margin="normal"
              required
              fullWidth
              name="password"
              label="Password"
              type="password"
              id="password"
              inputRef={passRef}
              autoComplete="current-password"
            />
            <Button
              type="submit"
              fullWidth
              variant="contained"
              onClick={handleSubmit}
              sx={{ mt: 3, mb: 2 }}
            >
              Sign In
            </Button>
          </Box>
        </Box>

      </Container>
    </ThemeProvider>
  );
}
