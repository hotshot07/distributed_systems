import React, { useContext, useRef } from 'react'
import { TokenContext } from './Store'
import axios from "axios";

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


const ENDPOINT = 'localhost';
const PORT = '5000';


function Accounts() {
    const [globalAuthData, setGlobalAuthData] = useContext(TokenContext)
    console.log("GOLBAL AUTH DATA")
    console.log(globalAuthData)

    // *Account creation refs.
    const acIdRef = useRef('');
    const acNameOfAdoRef = useRef('');
    const acNumAccountsRef = useRef('');
    const [accountType, setAccountType] = React.useState('');

    // *Account update refs.
    const updateIdRef = useRef('');
    const updateFirstNameRef = useRef('');
    const updateLastNameRef = useRef('');
    const updateNameOfAdoRef = useRef('');
    const updateCountryRef = useRef('');
    const updateEmailRef = useRef('');
    const updatePhoneNumberRef = useRef('');
    const [accountTypeUpdate, setAccountTypeUpdate] = React.useState('');

    async function handleCreateTest() {
        const auth_and_cors_headers = {
            'crossDomain': 'true',
            "X-Access-Token": `${globalAuthData.token}`
        }

        await axios.post(`http://${ENDPOINT}:${PORT}/create-n-accounts`,
            {
                Id: acIdRef.currrent.value,
                Organization: acNameOfAdoRef.current.value,
                NumberOfAccounts: acNumAccountsRef.current.value,
                AccountType: accountType
            }, { headers: auth_and_cors_headers }).then((response) => {
                console.log(response);
            }).catch((err) => {
                console.log(err);
            });
    }

    async function handleUpdateAccount() {
        const auth_and_cors_headers = {
            'crossDomain': 'true',
            "X-Access-Token": `${globalAuthData.token}`
        }

        await axios.post(`http://${ENDPOINT}:${PORT}/update-${accountTypeUpdate.toLocaleLowerCase()}-account`,
            {
                Id: updateIdRef.current.value,
                Organization: updateNameOfAdoRef.current.value,
                FirstName: updateFirstNameRef.current.value,
                LastName: updateLastNameRef.current.value,
                Email: updateEmailRef.current.value,
                Country: updateCountryRef.current.value,
                PhoneNumber: updatePhoneNumberRef.current.value
            }, { headers: auth_and_cors_headers }).then((response) => {
                console.log(response);
            }).catch((err) => {
                console.log(err);
            });
    }

    return (
        <div>
            <Grid container sx={{ alignItems: 'center', }} justifyContent="center">
                <Typography component="h1" variant="h2" sx={{ m: 5 }}>Account Manager</Typography>
            </Grid>
            <Grid container direction="column" alignItems="center" justifyContent="center"
            >
                <CssBaseline />

                <Stack direction="row" divider={<Divider orientation="vertical" flexItem />} spacing={10} sx={{ mt: 2 }}>
                    {CreateNAccountsCard()}
                    {UpdateAccountCard()}
                </Stack>
            </Grid>
        </div >
    )

    function UpdateAccountCard() {
        return <Card>
            <Stack direction="column" divider={<Divider orientation="vertical" flexItem />} spacing={2} sx={{ m: 2 }}>
                {updateFormHeader()}
                {updateForm()}
                {DropDownUpdateAccountType()}
                <Button type="submit" onClick={handleUpdateAccount} fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}>Do Something Else</Button>
            </Stack>
        </Card>;
    }

    function updateFormHeader() {
        return <Box sx={{ alignItems: 'center', }}>
            <Typography component="h1" variant="h5">Update Account</Typography>
        </Box>;
    }

    function updateForm() {
        return <>
            <TextField id="outlined-basic" label="ID" variant="outlined" inputRef={updateIdRef} />
            <TextField id="outlined-basic" label="Email" variant="outlined" inputRef={updateEmailRef} />
            <TextField id="outlined-basic" label="Organization Name" variant="outlined" inputRef={updateNameOfAdoRef} />
            <TextField id="outlined-basic" label="First Name" variant="outlined" inputRef={updateFirstNameRef} />
            <TextField id="outlined-basic" label="Last Name" variant="outlined" inputRef={updateLastNameRef} />
            <TextField id="outlined-basic" label="Country" variant="outlined" inputRef={updateCountryRef} />
            <TextField id="outlined-basic" label="Phone Number" variant="outlined" inputRef={updatePhoneNumberRef} />
        </>;
    }

    function CreateNAccountsCard() {
        return <Card>
            <Stack direction="column" divider={<Divider orientation="vertical" flexItem />} spacing={2} sx={{ m: 2 }}>
                {CreateAccountTitle()}
                {CreateAccountTopForm()}
                {DropDownAccountType()}
                <Button type="submit" fullWidth onClick={handleCreateTest} variant="contained" sx={{ mt: 3, mb: 2 }}> Create Account</Button>
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
                    <MenuItem value={"Admin"}>Tester</MenuItem>
                </Select>
            </FormControl>
        </Box>;
    }

    function DropDownUpdateAccountType() {
        return <Box sx={{ minWidth: 120 }}>
            <FormControl fullWidth>
                <InputLabel id="demo-simple-select-label">Account Type</InputLabel>
                <Select
                    labelId="demo-simple-select-label"
                    id="demo-simple-select"
                    value={accountTypeUpdate}
                    label="Account Type"
                    onChange={(event) => { setAccountTypeUpdate(event.target.value); }}
                >
                    <MenuItem value={"Athlete"}>Athlete</MenuItem>
                    <MenuItem value={"Orchestrator"}>Orchestrator</MenuItem>
                    <MenuItem value={"Admin"}>Admin</MenuItem>
                    <MenuItem value={"Admin"}>Tester</MenuItem>
                </Select>
            </FormControl>
        </Box>;
    }
}

export default Accounts