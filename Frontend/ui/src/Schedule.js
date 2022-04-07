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

// "athlete_id": "12342",
// "date": "2022-03-16",
// "orchestrator_id": "2",
// "tester_id": "Tester2"

export default function Schedule() {
  const [globalAuthData, setGlobalAuthData] = useContext(TokenContext)
  const [tableData, setTableData] = useState([]);

  const athleteIdCreateTestRef = useRef('');
  const [dateTestCreate, setDateTestCreate] = useState(new Date());
  const orchestratorIdRef = useRef('');
  const testerIdRef = useRef('');

  async function handleCreateTest() {
    const createTestDate = dateTestCreate.toISOString().split("T")[0];
    await axios.post('http://localhost:5000/assign-athlete-test',
      {
        athlete_id: athleteIdCreateTestRef.current.value,
        datetimeUTC: createTestDate,
        orchestrator_id: orchestratorIdRef.current.value,
        tester_id: testerIdRef.current.value
      }, { crossDomain: true }).then((response) => {
        console.log(response);
      }).catch((err) => {
        console.log(err);
      });
  }

  return (
    <div>
      <Grid container spacing={0} direction="column" alignItems="center" justifyContent="center" style={{ minHeight: '40vh' }} >
        <CssBaseline />
        <Stack direction="row" spacing={20} justifyContent="center" alignItems="center" divider={<Divider orientation="vertical" flexItem />}>
          <Box>
            <Stack direction="column" spacing={2} justifyContent="center" alignItems="center">
              <Box sx={{ alignItems: 'center', }}>
                <Typography component="h1" variant="h5">Create Test</Typography>
              </Box>

              <TextField id="standard-basic" label="Athlete ID" variant="standard" inputRef={athleteIdCreateTestRef} />
              <TextField id="standard-basic" label="Orchestrator ID" variant="standard" inputRef={orchestratorIdRef} />
              <TextField id="standard-basic" label="Tester ID" variant="standard" inputRef={testerIdRef} />

              <Box sx={{ alignItems: 'center', m: 2 }}>
                <MuiPickersUtilsProvider utils={DateFnsUtils}>
                  <DatePicker value={dateTestCreate} onChange={(newDate) => { setDateTestCreate(newDate) }} />
                </MuiPickersUtilsProvider>
              </Box>
              <Button onClick={handleCreateTest} type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}> Create Test </Button>
            </Stack>
          </Box>
        </Stack>
      </Grid>
    </div>
  )
}
