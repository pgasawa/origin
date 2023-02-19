import logo from './logo.svg';
import './App.css';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid'
import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text } from 'react-native'
import Cluster from './components/card';


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
      <div className='Time'>{currentTime.toLocaleTimeString()}</div>
      <div className='HelloMessage'></div>
      <div className="Workspaces">
        <Grid container spacing={2}>
          <Grid item xs={4}>
          <Cluster color={'red'} className="BasicCard" title="CS 189"></Cluster>
          </Grid>
          <Grid item xs={4}>
          <Cluster className="BasicCard" title="CS 170"></Cluster>
          </Grid>
          <Grid item xs={4}>
          <Cluster className="BasicCard" title="CS 61A"></Cluster>
          </Grid>
        </Grid>
        </div>
    </div>
  );
}

export default App;
