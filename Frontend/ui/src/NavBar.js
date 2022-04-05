import * as React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import Container from '@mui/material/Container';
import Button from '@mui/material/Button';
import { useNavigate } from "react-router-dom";

const ResponsiveAppBar = () => {
  const navigate = useNavigate();

  const navigateToPage = (p) => {
      navigate(`/${p}`)
  }
  
  // TODO: Add drop down menu for login profile etc.
  return (
    <AppBar position="static">
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          <Typography variant="h6" noWrap component="div" sx={{ mr: 2, display: { xs: 'none', md: 'flex' } }}>
            Testrr
          </Typography>
          <Box sx={{ flexGrow: 1, display: { xs: 'none', md: 'flex' } }}>
              <Button onClick={() => navigateToPage('Tests')} sx={{ my: 2, color: 'white', display: 'block' }}>Tests</Button>
              <Button onClick={() => navigateToPage('Schedule')} sx={{ my: 2, color: 'white', display: 'block' }}>Schedule Test</Button>
              <Button onClick={() => navigateToPage('Availability')} sx={{ my: 2, color: 'white', display: 'block' }}>Athelete Availability</Button>
              <Button onClick={() => navigateToPage('Accounts')} sx={{ my: 2, color: 'white', display: 'block' }}>Accounts</Button>
          </Box>
        </Toolbar>
      </Container>
    </AppBar>
  );
};
export default ResponsiveAppBar;