import './App.css';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid'
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Workspace() {
    const [urls, setUrls] = useState([]);
    const [summary, setSummary] = useState('');
    const [userInput, setUserInput] = useState('');
    const [botResponse, setBotResponse] = useState('');

    useEffect(() => {
        // Fetch the list of URLs from the API
        axios.get('http://127.0.0.1:5000.com/top-n-urls')
          .then(response => {
            setUrls(response.data.urls);
          })
          .catch(error => {
            console.error(error);
          });
    
        // Fetch the paragraph from the API
        axios.get('http://127.0.0.1:5000/summarize-cluster')
          .then(response => {
            setSummary(response.data);
          })
          .catch(error => {
            console.error(error);
          });
      }, []);

    function handleUserInput(event) {
    setUserInput(event.target.value);
    }

    function handleBotResponse(response) {
    setBotResponse(response);
    }

    return (
    <div style={{ display: 'flex', justifyContent: 'space-between' }}>
        <div>
        <h2>URLs</h2>
        <ul>
            {urls.map((url, index) => (
            <li key={index}>{url}</li>
            ))}
        </ul>
        </div>
        <div>
        <h2>Summary</h2>
        <p>{summary}</p>
        </div>
        <div>
        <h2>Chatbot</h2>
        <input type="text" value={userInput} onChange={handleUserInput} />
        <button onClick={() => {
            // Make a call to the chatbot API with the user's input
            axios.post('http://127.0.0.1:5000/cluster_chat', { input: userInput })
            .then(response => {
                handleBotResponse(response.data);
            })
            .catch(error => {
                console.error(error);
            });
        }}>Send</button>
        <p>{botResponse}</p>
        </div>
    </div>
    );
}