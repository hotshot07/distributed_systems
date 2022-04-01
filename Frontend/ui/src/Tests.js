import * as React from 'react';
import Button from '@mui/material/Button';
import Stack from '@mui/material/Stack';
import Grid from '@mui/material/Grid'
// Search components
import TextField from '@mui/material/TextField';

// Table Stuff
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';
import { CssBaseline } from '@mui/material';

function createData(name, calories, fat, carbs, protein) {
  return { name, calories, fat, carbs, protein };
}

const rows = [
  createData('Frozen yoghurt', 123, "Yokes", "false", "Canada"),
  createData('Ice cream sandwich', 420, "Loads", "false", "United Kingdom"),
  createData('Eclair', 262, "None", "true", "China"),
  createData('Cupcake', 305, "Guinness", "true", "Ireland"),
  createData('Gingerbread', 356, "None", "true", "Spain"),
];


class Tests extends React.Component{
  constructor(props) {
    super(props);
  
    // Initializing the state 
    this.state = { color: 'lightgreen' };
  }

  render() {
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
        <Grid item xs={3}>
            <Stack direction="row" spacing={2}>
                <Button variant="contained">Get Results</Button>
                <TextField id="outlined-basic" label="Athlete ID" variant="outlined"/>
            </Stack>
            <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="simple table">
                <TableHead>
                <TableRow>
                    <TableCell>Athlete Name</TableCell>
                    <TableCell align="right">ID</TableCell>
                    <TableCell align="right">Drugs</TableCell>
                    <TableCell align="right">Passed</TableCell>
                    <TableCell align="right">ADO</TableCell>
                </TableRow>
                </TableHead>
                <TableBody>
                {rows.map((row) => (
                    <TableRow
                    key={row.name}
                    sx={{ '&:last-child td, &:last-child th': { border: 0 } }}
                    >
                    <TableCell component="th" scope="row">
                        {row.name}
                    </TableCell>
                    <TableCell align="right">{row.calories}</TableCell>
                    <TableCell align="right">{row.fat}</TableCell>
                    <TableCell align="right">{row.carbs}</TableCell>
                    <TableCell align="right">{row.protein}</TableCell>
                    </TableRow>
                ))}
                </TableBody>
            </Table>
            </TableContainer>
        </Grid>   
      </Grid> 
        );  
      }

  componentDidMount(){
    console.log("Component did mount.")
  
  }
};
export default Tests;