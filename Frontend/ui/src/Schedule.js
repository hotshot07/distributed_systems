import React, { useRef, useState, useContext } from 'react';
import { TokenContext } from './Store';
import axios from "axios";

import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import Stack from '@mui/material/Stack';
import Grid from '@mui/material/Grid';
import Divider from '@mui/material/Divider';
import Typography from '@mui/material/Typography';
import CssBaseline from '@mui/material/CssBaseline';
import { Box } from '@mui/system';

// Date-time stuff
import {
  DatePicker,
  MuiPickersUtilsProvider,
} from '@material-ui/pickers';

// pick a date util library
import DateFnsUtils from '@date-io/date-fns';
const ENDPOINT = 'testerr.ie';
const PORT = '5000';
// "athlete_id": "12342",
// "date": "2022-03-16",
// "orchestrator_id": "2",
// "tester_id": "Tester2"

// "test_datetime": "2022-03-16 12:00:00",
// "test_result": "postive",
// "tester_id": "Tester2"

export default function Schedule() {
  const [globalAuthData, setGlobalAuthData] = useContext(TokenContext)
  const [tableData, setTableData] = useState([]);

  const athleteIdCreateTestRef = useRef('');
  const [dateTestCreate, setDateTestCreate] = useState(new Date());
  const orchestratorIdRef = useRef('');
  const testerIdRef = useRef('');

  const [testDateToUpdate, setTestDateToUpdate] = useState(new Date());
  const testTimeToUploadRef = useRef('');
  const testerIdUploadRef = useRef('');
  const testResultToUploadRef = useRef('');

  async function handleUploadTestResult() {
    const auth_and_cors_headers = {
      'crossDomain': 'true',
      "X-Access-Token": `${globalAuthData.token}`
    }
    const utcTestUpload = testDateToUpdate.toISOString().split("T")[0] + " " + testTimeToUploadRef.current.value + ":00:00";
    console.log(utcTestUpload, testerIdUploadRef.current.value, testResultToUploadRef.current.value);

    await axios.post(`http://${ENDPOINT}:${PORT}/upload-test-result`,
      {
        test_datetime: utcTestUpload,
        test_result: testResultToUploadRef.current.value,
        tester_id: testerIdUploadRef.current.value
      },
      { headers: auth_and_cors_headers }).then((response) => {
        console.log(response);
      });
  }

  async function handleCreateTest() {
    const auth_and_cors_headers = {
      'crossDomain': 'true',
      "X-Access-Token": `${globalAuthData.token}`
    }
    const createTestDate = dateTestCreate.toISOString().split("T")[0];

    await axios.post(`http://${ENDPOINT}:${PORT}/assign-athlete-test`,
      {
        athlete_id: athleteIdCreateTestRef.current.value,
        datetimeUTC: createTestDate,
        orchestrator_id: orchestratorIdRef.current.value,
        tester_id: testerIdRef.current.value
      }, { headers: auth_and_cors_headers }).then((response) => {
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
          <Box>
            <Stack direction="column" spacing={2} justifyContent="center" alignItems="center">
              <Box sx={{ alignItems: 'center', }}>
                <Typography component="h1" variant="h5">Upload Test Result</Typography>
              </Box>
              <TextField id="standard-basic" label="Test Result" variant="standard" inputRef={testResultToUploadRef} />
              <TextField id="standard-basic" label="Tester ID" variant="standard" inputRef={testerIdUploadRef} />
              <Box sx={{ alignItems: 'center', m: 2 }}>
                <TextField id="standard-basic" label="Hour (24hr)" variant="standard" inputRef={testTimeToUploadRef} type="number" defaultValue={12} />
              </Box>

              <Box sx={{ alignItems: 'center', m: 2 }}>
                <MuiPickersUtilsProvider utils={DateFnsUtils}>
                  <DatePicker value={dateTestCreate} onChange={(newDate) => { setTestDateToUpdate(newDate) }} />
                </MuiPickersUtilsProvider>
              </Box>
              <Button onClick={handleUploadTestResult} type="submit" fullWidth variant="contained" sx={{ mt: 3, mb: 2 }}> Uplaod Test </Button>
            </Stack>
          </Box>
        </Stack>
      </Grid>
    </div>
  )
}
