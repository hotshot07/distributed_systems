import React, { useContext, useRef } from 'react'
import { TokenContext } from './Store'

// mui imports
import Divider from '@mui/material/Divider';
import Button from '@mui/material/Button';
import Card from '@mui/material/Card';
import InputLabel from '@mui/material/InputLabel';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';
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

    // *Account creation refs.
    const acIdRef = useRef('');
    const acNameOfAdoRef = useRef('');
    const acNumAccountsRef = useRef('');
    const [accountType, setAccountType] = React.useState('');


    return (
        <div>
            <Grid container sx={{ alignItems: 'center', }} justifyContent="center">
                <Typography component="h1" variant="h2" sx={{m:5}}>Account Manager</Typography>
            </Grid>
            <Grid container direction="column" alignItems="center" justifyContent="center"
            >
                <CssBaseline />

                <Stack direction="row" divider={<Divider orientation="vertical" flexItem />} spacing={10} sx={{ mt: 2 }}>
                    {CreateAccountCard()}
                    <Card>
                        <Stack direction="column" divider={<Divider orientation="vertical" flexItem />} spacing={2} sx={{ m: 2 }} >
                            <Box sx={{ alignItems: 'center', }}>
                                <Typography component="h1" variant="h5">Update Account</Typography>
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

    function CreateAccountCard() {
        return <Card>
            <Stack direction="column" divider={<Divider orientation="vertical" flexItem />} spacing={2} sx={{ m: 2 }}>
                {CreateAccountTitle()}
                {CreateAccountTopForm()}
                {DropDownAccountType()}
                <Button type="submit" fullWidth onClick={() => { console.log(accountType); } } variant="contained" sx={{ mt: 3, mb: 2 }}> Create Account</Button>
            </Stack>
        </Card>;
    }

    function CreateAccountTitle() {
        return <Box sx={{ alignItems: 'center', }}>
            <Typography component="h1" variant="h5">Create Account</Typography>
        </Box>;
    }

    function CreateAccountTopForm() {
        return <>
            <TextField id="outlined-basic" label="ID" variant="outlined" inputRef={acIdRef} />
            <TextField id="outlined-basic" label="Organization Name" variant="outlined" inputRef={acNameOfAdoRef} />
            <TextField id="outlined-basic" label="Number of Accounts" variant="outlined" inputRef={acNumAccountsRef} />
        </>;
    }

    function DropDownAccountType() {
        return <Box sx={{ minWidth: 120 }}>
            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">Account Type</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={accountType}
                    label="Account Type"
                    onChange={(event) => { setAccountType(event.target.value); }}
                >
                    <MenuItem value={"Athlete"}>Athlete</MenuItem>
                    <MenuItem value={"Orchestrator"}>Orchestrator</MenuItem>
                    <MenuItem value={"Admin"}>Admin</MenuItem>
                </Select>
            </FormControl>
        </Box>;
    }
}

export default Accounts