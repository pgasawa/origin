import logo from './logo.svg';
import './App.css';
import Button from '@mui/material/Button';
import React, { Component }  from 'react';
import BasicCard from './components/card';


function App() {
  return (
    <div className="App">
      <header className="App-header">
        <Button variant="contained">Contained</Button>
        <BasicCard title="CS 189" description="Introduction to Machine Learning"></BasicCard>
      </header>
    </div>
  );
}

export default App;
