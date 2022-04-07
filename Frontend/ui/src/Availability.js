import React, { useRef, useState, useContext } from 'react';
import { TokenContext } from './Store';
import axios from "axios";

import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';
import Grid from '@mui/material/Grid';
import Divider from '@mui/material/Divider';
// import Slide from '@mui/material/Slide';
// import Alert from '@mui/material/Alert';
import Typography from '@mui/material/Typography';
import CssBaseline from '@mui/material/CssBaseline';
import { DataGrid } from '@mui/x-data-grid';
import { Box } from '@mui/system';


// Date-time stuff
import {
    DatePicker,
    MuiPickersUtilsProvider,
} from '@material-ui/pickers';

// pick a date util library
import DateFnsUtils from '@date-io/date-fns';

const ENDPOINT = "20.224.88.180";
const PORT = 4000

const columns = [
    { field: 'athlete_id', headerName: 'Athlete ID' },
    { field: 'available_time', headerName: 'Time' },
    { field: 'date', headerName: 'Date' },
    { field: 'athlete_id', headerName: 'Athlete ID' }
]

export default function Availability() {
    const [globalAuthData, setGlobalAuthData] = useContext(TokenContext)
    const [tableData, setTableData] = useState([]);

    // Refs for getting athlete availability
    const athleteIdRef = useRef('');

    // Refs and State for updating availability
    const timeToUpdateRef = useRef('');
    const athleteIdUpdateRef = useRef('');
    const countryUpdateRef = useRef('');
    const locationUpdateRef = useRef('')
    const [dateToUpdate, setDateToUpdate] = useState(new Date());

    async function handleAvailabilityClick() {
        let idCounter = 0;
        const auth_and_cors_headers = {
            'crossDomain': 'true',
            "X-Access-Token": `${globalAuthData.token}`
        }
        await axios.get(`http://${ENDPOINT}:${PORT}/view-athlete-availability/`.concat(athleteIdRef.current.value),
            { headers: auth_and_cors_headers })
            .then((response) => {
                response.data.forEach((x, i) => { x['_id'] = idCounter++ });
                console.log(response);
                setTableData(response.data);
            })
            .catch(() => {
                console.log("Uh oh");
            });
    }

    async function handleAvailabilityUpdate() {
        const utcTimeToUpdate = dateToUpdate.toISOString().split("T")[0] + " " + timeToUpdateRef.current.value + ":00:00"
        const auth_and_cors_headers = {
            'crossDomain': 'true',
            "X-Access-Token": `${globalAuthData.token}`
        }
        await axios.post(`http://${ENDPOINT}:${PORT}/update-athlete-availability`,
            [{
                athlete_id: athleteIdUpdateRef.current.value,
                datetimeUTC: utcTimeToUpdate,
                location: locationUpdateRef.current.value,
                location_country: countryUpdateRef.current.value
            }], { headers: auth_and_cors_headers }).then((response) => {
                console.log(response);
            }).catch((err) => {
                console.log(err);
            });
    }

    function keyPress() {
        return "Hello"
    }

    return (
        <div>
            <Grid container spacing={0} direction="column" alignItems="center" justifyContent="center" style={{ minHeight: '40vh' }} >
                <CssBaseline />
                <Stack direction="row" spacing={20} justifyContent="center" alignItems="center" divider={<Divider orientation="vertical" flexItem />}>
                    <Box sx={{ alignItems: 'center' }}>
                        <Stack direction="column" spacing={2} sx={{ m: 2 }} justifyContent="center" alignItems="center">
                            <TextField id="standard-basic" label="Athelete ID" variant="standard" sx={{ m: 2 }} onKeyDown={keyPress} inputRef={athleteIdRef} />
                            <Button variant="outlined" sx={{ m: 2 }} onClick={handleAvailabilityClick}>Get Availability</Button>
                        </Stack>
                        <Box container sx={{ m: 2, width: 500, height: 300, }} >
                            <DataGrid
                                rows={tableData}
                                getRowId={(row) => row._id}
                                columns={columns}
                                pageSize={15} />
                        </Box>
                    </Box>
                    <Box>
                        <Stack direction="column" spacing={2} justifyContent="center" alignItems="center">
                            <Box sx={{ alignItems: 'center', }}>
                                <Typography component="h1" variant="h5">Add Availability</Typography>
                            </Box>

                            <TextField id="standard-basic" label="Athlete ID" variant="standard" inputRef={athleteIdUpdateRef} />
                            <TextField id="standard-basic" label="Location" variant="standard" inputRef={locationUpdateRef} />
                            <TextField id="standard-basic" label="Country" variant="standard" inputRef={countryUpdateRef} />

                            <Box sx={{ alignItems: 'center', m: 2 }}>
                                <MuiPickersUtilsProvider utils={DateFnsUtils}>
                                    <DatePicker value={dateToUpdate} onChange={(newDate) => { setDateToUpdate(newDate) }} />
                                </MuiPickersUtilsProvider>
                            </Box>
                            <Box sx={{ alignItems: 'center', m: 2 }}>
                                <TextField id="standard-basic" label="Hour (24hr)" variant="standard" inputRef={timeToUpdateRef} type="number" defaultValue={12} />
                            </Box>
                            <Button onClick={handleAvailabilityUpdate} type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}> Add Availability </Button>
                        </Stack>
                    </Box>
                </Stack>
            </Grid>

        </div>
    )
}