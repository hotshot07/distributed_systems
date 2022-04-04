import React, { useContext } from 'react'
import { TokenContext } from './Store'

// mui imports
import Divider from '@mui/material/Divider';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import Paper from '@mui/material/Paper';
import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField';
import Grid from '@mui/material/Grid';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import { CssBaseline } from '@mui/material';


function Accounts() {
    const [globalAuthData, setGlobalAuthData] = useContext(TokenContext)
    console.log("GOLBAL AUTH DATA")
    console.log(globalAuthData)
    return (
        <div>
            <Grid container sx={{ alignItems: 'center', }} justifyContent="center">
                <Typography component="h1" variant="h2">Account Manager</Typography>
            </Grid>
            <Grid
                container
                direction="column"
                alignItems="center"
                justifyContent="center"
            >
                <CssBaseline />

                <Stack direction="row" divider={<Divider orientation="vertical" flexItem />} spacing={10} sx={{ mt: 2 }}>
                    <Card sx={{ m: 2, marginTop: 5 }}>
                        <Stack direction="column" divider={<Divider orientation="vertical" flexItem />} spacing={2} sx={{ m: 2 }}>
                            <Box sx={{ alignItems: 'center', }}>
                                <Typography component="h1" variant="h5">Create Account</Typography>
                            </Box>

                            <TextField id="outlined-basic" label="Something" variant="outlined" />
                            <TextField id="outlined-basic" label="Something 2" variant="outlined" />
                            <TextField id="outlined-basic" label="Something 3" variant="outlined" />
                            <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}> Create Account</Button>
                        </Stack>
                    </Card>
                    <Card sx={{ m: 2, marginTop: 5 }}>
                        <Stack direction="column" divider={<Divider orientation="vertical" flexItem />} spacing={2} sx={{ m: 2 }} >
                            <Box sx={{ alignItems: 'center', }}>
                                <Typography component="h1" variant="h5">Other Account</Typography>
                            </Box>

                            <TextField id="outlined-basic" label="Other" variant="outlined" />
                            <TextField id="outlined-basic" label="Other 2" variant="outlined" />
                            <TextField id="outlined-basic" label="Other 3" variant="outlined" />
                            <Button type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>Do Something Else</Button>
                        </Stack>
                    </Card>
                </Stack>
            </Grid>
        </div >
    )
}

export default Accounts