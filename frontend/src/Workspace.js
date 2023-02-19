import './App.css';
import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import Cookies from 'js-cookie';
import { Link, Box, Stack, Button, Paper } from '@mui/material';
import backButton from './components/backButton';
import { styled } from '@mui/material/styles';

const Workspace = (props) => {
  const [urls, setUrls] = useState([]);
  const [summary, setSummary] = useState(null);
  const [userInput, setUserInput] = useState('');
  const [botResponse, setBotResponse] = useState('');
  const [workspaceID, setWorkspaceID] = useState(Cookies.get('curent_workspace_id'));
  const [chatHistory, setChatHistory] = useState('[]');
  const [disableChatButton, setDisableChatButton] = useState(false);

  useEffect(() => {
    setWorkspaceID(Cookies.get('curent_workspace_id'))
  }, [])

  useEffect(() => {
    // Fetch the list of URLs from the API
    console.log(`http://127.0.0.1:5000/top-n-urls?username=arvind6902@gmail.com&cluster_id=${workspaceID}`)
    axios.get(`http://127.0.0.1:5000/top-n-urls?username=arvind6902@gmail.com&cluster_id=${workspaceID}`)
      .then(response => {
        console.log("WINNER: ", response)
        setUrls(response.data.urls);
      })
      .catch(error => {
        console.log("SOMETHING WENT WRONG")
        console.error(error);
      });

    // Fetch the paragraph from the API
    axios.get(`http://127.0.0.1:5000/summarize-cluster?cluster_id=${workspaceID}`)
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
    // console.log(response)
    setBotResponse(response.data.answer);
    setChatHistory(response.data.history)
  }

  const getUrlsComponent = useCallback(() => {
    if (urls) {
      const component_urls = []
      for (var i = 0; i < urls.length; i++) {
        const url = urls[i];
        const url_component = (<Item>
          <p style={{ color: 'black', padding: 0, margin: 0 }}>{url.title}</p>
          <div style={{whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis', width: '100%'}}>
            <Link href={url.url} target="_blank" color="inherit">{url.url}</Link>
          </div>
        </Item>)
        component_urls.push(url_component)
      }
      return component_urls
    } else {
      return "Loading URLs"
    }
  }, [urls])

  const getChatHistory = useCallback(() => {
    if (chatHistory) {
      const component_chats = []
      for (var i = 0; i < chatHistory.length; i++) {
        const userchat = chatHistory[i][0];
        const botchat = chatHistory[i][1];
        var user_component = <div style={{borderRadius: '5%', fill: 'black', color: 'white'}}> </div>
        var bot_component = <div style={{borderRadius: '5%', fill: 'white', color: 'black'}}> </div>
        component_chats.push(user_component)
        component_chats.push(bot_component)
      }
      return component_chats
    } else {
      return "Loading URLs"
    }
  }, [urls])

  function getSummary() {
    if (summary) {
      return summary
    } else {
      return "Loading summary."
    }
  }

  const Item = styled(Paper)(({ theme }) => ({
    backgroundColor: theme.palette.mode === 'dark' ? '#1A2027' : '#fff',
    ...theme.typography.body2,
    padding: theme.spacing(1),
    textAlign: 'center',
    color: theme.palette.text.secondary,
  }));

  return (
    <div>
      <Box sx={{ margin: 2 }}>
        <div style={{ float: 'right' }}>
          {backButton(props.setUpdate)}
        </div>
        <Box sx={{ margin: 2 }}></Box>
        <div className='Headings' style={{ display: 'flex', justifyContent: 'center', alignItems: 'center' }}>
          {props.workspaceName}
        </div>
        <Stack direction='row'>
          <Box className='LeftColumn' sx={{ width: '30%', marginRight: 2 }}>
            <Box >
              <div className='Subheadings'>Last Visited</div>
              <Stack spacing={2}>
                {/* {urls.map((url, index) => (
              <li key={index}>{url.url}</li>
              ))} */}
                {getUrlsComponent()}
              </Stack>

            </Box>
            <Box sx={{ margin: 4 }}></Box>
            {/* <hr ></hr> */}
            <Box >
              <div className='Subheadings'>Related Views</div>
              <p style={{ fontStyle: 'italic' }}>People in your organization also viewed</p>
              <Stack spacing={2}>
                {/* {urls.map((url, index) => (
              <li key={index}>{url.url}</li>
              ))} */}
                {getUrlsComponent()}
              </Stack>
            </Box>
          </Box>
          <Box className='LeftColumn' sx={{ width: '40%', marginRight: 2 }}>
            <Box >
              <div className='Subheadings'>Summary</div>
              {getSummary()}

            </Box>
            <Box sx={{ margin: 4 }}></Box>
            {/* <hr ></hr> */}
            <Box >
              <div className='Subheadings'>Semantic Search</div>
              <Stack spacing={2}>
                {getUrlsComponent()}
              </Stack>
            </Box>
          </Box>
          <div className='LeftColumn' style={{ width: '30%' }}>
            <Box >
              <div className='Subheadings'>AI Assistant</div>
              <p>Hi! I'm Origin, and I'm here to assist you! I'm fine-tuned on {props.workspaceName}. Feel free to ask me specific questions you might have!</p>

              <input type="text" value={userInput} onChange={handleUserInput} />
              <Button
                style={{ color: 'black' }}
                disabled={disableChatButton}
                onClick={() => {
                  // Make a call to the chatbot API with the user's input
                  setDisableChatButton(true);
                  axios.get(`http://127.0.0.1:5000/cluster-chat-bot?cluster_id=${workspaceID}&title=${props.workspaceName}&question=${userInput}&history=${chatHistory}`)
                    .then(response => {
                      handleBotResponse(response);
                      setDisableChatButton(false);
                    })
                    .catch(error => {
                      console.error(error);
                      setDisableChatButton(false);
                    });
                }}>Send</Button>
              {getChatHistory}
            </Box>
          </div>
        </Stack>
      </Box>
    </div>
    //     {/* <div>
    //     <h2>Summary</h2>
    //     <p>{getSummary()}</p>

    //     </div>
    //     <div>
    //     <h2>Chatbot</h2>
    //     <input type="text" value={userInput} onChange={handleUserInput} />
    //     <button 
    //         disabled={disableChatButton}
    //         onClick={() => {
    //         // Make a call to the chatbot API with the user's input
    //         setDisableChatButton(true);
    //         axios.get(`http://127.0.0.1:5000/cluster-chat-bot?cluster_id=${workspaceID}&title=${props.workspaceName}&question=${userInput}&history=${chatHistory}`)
    //         .then(response => {
    //             handleBotResponse(response);
    //             setDisableChatButton(false);
    //         })
    //         .catch(error => {
    //             console.error(error);
    //             setDisableChatButton(false);
    //         });
    //     }}>Send</button>
    //     <p>{botResponse}</p>
    //     </div>
    // </div> */}
  );
}

export default Workspace;