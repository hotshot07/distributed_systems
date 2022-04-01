import React, { useState, useEffect, useRef } from 'react';
// import React, { useMemo, useState, useEffect } from "react";
import axios from "axios";

// MUI basics
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Grid from '@mui/material/Grid';
import Slide from '@mui/material/Slide';
import Alert from '@mui/material/Alert';

// Search components
import TextField from '@mui/material/TextField';
import { DataGrid, useGridApiRef} from '@mui/x-data-grid';
import Paper from '@mui/material/Paper';
import { CssBaseline } from '@mui/material';

const columns = [
  { field: 'athlete_name', headerName: 'Name'},
  { field: 'athlete_id', headerName: 'ID'},
  { field: 'assigned_on', headerName: 'Assigned' },
  { field: 'location', headerName: 'Location'},
  { field: 'result', headerName: 'Result'},
  { field: 'ochestrator_id', headerName: 'Orchestrator'},
  { field: 'test_datetime', headerName: 'Test Date'},
  { field: 'tester_name', headerName: 'Tester'}
]

const Tests = () => {
  const [tableData, setTableData] = useState([]);
  const [tableError, setTableError] = useState(false);

  const countryTextFieldValueRef = useRef('')
  const tableInitialMount = useRef(true);
  let idCounter = 0;

  async function getData() {
    console.log(countryTextFieldValueRef.current.value)
    if (countryTextFieldValueRef) {
      await axios.get('http://127.0.0.1:3000/view-test-results/'.concat(countryTextFieldValueRef.current.value), { crossDomain: true })
      .then((response) => {
        response.data.Items.forEach((x, i) => {
          x['_id']            = idCounter++;
          x['ochestrator_id'] = x['orchestrator']['user_id'];
          x['athlete_name']   = x['athlete']['first_name'] + " " + x['athlete']['second_name'];
          x['athlete_id']     = x['athlete']['user_id']
          x['tester_name']    = x['tester']['first_name'] + " " + x['tester']['second_name']
        });
        
        setTableData(response.data.Items);
        });
    }
    else{
      console.log(countryTextFieldValueRef)
      console.log("Something went wrong")
    }
  }
  
  useEffect(() => {
    if (tableInitialMount.current){
      tableInitialMount.current = false;
    }
    else{
      console.log("Table data changed")
    }
  }, [tableData])

  return (
  <Grid
      container
      spacing={0}
      direction="column"
      alignItems="center"
      justifyContent="center"
      style={{ minHeight: '100vh' }}
    >
      <CssBaseline/>

        <Stack direction="row" spacing={2} justifyContent="center" alignItems="center">
            <TextField id="outlined-basic" label="Country" variant="outlined" sx={{ m: 2 }} inputRef={countryTextFieldValueRef}/>
            <Button variant="outlined" sx={{ m: 2 }} onClick={getData}>Get Results</Button>
        </Stack>
        <Slide direction="up" in={tableError} mountOnEnter unmountOnExit>
          <Alert severity="error">Results for {countryTextFieldValueRef} could not be loaded.</Alert>
        </Slide>
        <div style={{ height: 400, width: "50%" }}>
          <DataGrid
          getRowId={(row) => row._id} 
          columns={columns} 
          rows={tableData} 
          pageSize={15} />
        </div>
    </Grid> 
    );  
};
export default Tests;