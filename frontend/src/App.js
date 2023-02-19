import logo from './logo.svg';
import './App.css';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid'
import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text } from 'react-native'
import Cluster from './components/card';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';

function App() {

  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  return (
    
    <div className="App">
      <Box 
      sx={{margin: 2}}>
      <Box sx={{margin: 20}}></Box>
      <div className='Time' style = {{display: 'flex', justifyContent: 'center', alignItems: 'center'}}>{currentTime.toLocaleTimeString()}</div>
      <div className='HelloMessage' style = {{display: 'flex', justifyContent: 'center', alignItems: 'center'}}> Good morning, Ayushi.</div>
      <Box 
      sx={{m: 10}}></Box>
      <div className="Workspaces">
      <Stack direction="row" spacing={4} justifyContent="center">
      <Cluster title="CS 189"></Cluster>
      <Cluster title="CS 170"></Cluster>
      <Cluster title="UGBA 105"></Cluster>
    </Stack>
        </div>
        </Box>
    </div>
   
  );
}

export default App;
