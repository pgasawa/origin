import logo from './logo.svg';
import './App.css';
import axios from 'axios'
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid'
import React, { useState, useEffect } from 'react';
import { StyleSheet, View, Text } from 'react-native'
import Cluster from './components/card';
import Box from '@mui/material/Box';
import Stack from '@mui/material/Stack';

function App() {
  const [currentTime, setCurrentTime] = useState(new Date());
  const [clusterData, setClusterData] = useState(null);

  const getClusters = async () => {
    return axios.get('http://127.0.0.1:5000/get-clusters?username=arvind6902@gmail.com')
        .then(function (res) {
            if (res.data.clusters !== null){
                console.log(res)
                return (res.data.clusters)
            }
        })
        .catch(function (res) {
            if (res.response) {
                console.log(res.response.data.reason + " Please wait a few seconds and try reloading the page.");
            } else {
                console.log("Something went wrong. Please wait a few seconds and try reloading the page.")
            }
        });
  }

  useEffect( () => {
      if (clusterData === null) {
          getClusters().then( (res) => {
              setClusterData(res)
          })
      }
  }, [clusterData])

  useEffect(() => {
    const interval = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  function getClustersComponent() {
    const clusters = []
    for (var i = 0; i < clusterData.length; i++) { 
      const cluster = clusterData[i];
      const preview = <Cluster title={cluster.name}></Cluster>
      clusters.push(preview)
   }
   return clusters
  }

  if (clusterData) {
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
        {getClustersComponent()}
      </Stack>
          </div>
          </Box>
      </div>
    
    );
  } else {
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
        <div className='HelloMessage' style = {{display: 'flex', justifyContent: 'center', alignItems: 'center'}}> Loading workspaces.</div>
      </Stack>
          </div>
          </Box>
      </div>
    );
  }
}

export default App;
