import React, { useRef, useState } from 'react';
import { Buffer } from 'buffer';

// MUI imports
import Button from '@mui/material/Button';
import CssBaseline from '@mui/material/CssBaseline';
import TextField from '@mui/material/TextField';
import Link from '@mui/material/Link';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Slide from '@mui/material/Slide';
import Alert from '@mui/material/Alert';
import { createTheme, ThemeProvider } from '@mui/material/styles';

// Networking
import axios from "axios";

function Copyright(props) {
  return (
    <Typography variant="body2" color="text.secondary" align="center" {...props}>
      {'Copyright © '}
      <Link color="inherit" href="https://mui.com/">
        Testicle Testing, Ltd
      </Link>{' '}
      {new Date().getFullYear()}
      {'.'}
    </Typography>
  );
}

const theme = createTheme();

export default function SignIn() {
  const userRef = useRef('')
  const passRef = useRef('')
  const [loginError, setLoginError] = useState(false)

  const handleSubmit = (event) => {
    event.preventDefault();

    const basicAuthAsToken = Buffer.from(`${userRef.current.value}:${passRef.current.value}`).toString('base64');

    const authorization = `Basic ${basicAuthAsToken}`

    axios.post("http://127.0.0.1:5000/login", {crossDomain: true }, { headers: { "Authorization": authorization, crossDomain: true } })
      .then((response) => {
        if (response.status === 200) {
          console.log(response.data)
          setLoginError(false);
        }
        else {
          setLoginError(true);
        }
      })
      .catch((err) => {
        console.log("Err")
      })
  };

  return (
    <ThemeProvider theme={theme}>
      <Container component="main" maxWidth="xs">
        <CssBaseline />
        <Box
          sx={{
            marginTop: 8,
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <Typography component="h1" variant="h5">
            Sign in
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
        <Copyright sx={{ mt: 8, mb: 4 }} />
      </Container>
    </ThemeProvider>
  );
}
