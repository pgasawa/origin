import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import RocketLaunchIcon from "@mui/icons-material/RocketLaunch";
import './card.css'
import React, { useState, useEffect } from 'react';
import { Text, TextInput, View } from 'react-native';
import axios from 'axios'
import Cookies from 'js-cookie';
// import { useNavigate } from "react-router-dom";

export default function Cluster(props) {
  const [text, setText] = useState(props.title);
  const [input, setInput] = useState('edit me');
  // const navigator = useNavigate();

  const getClusters = async (input) => {
    return axios.get(`http://127.0.0.1:5000/change-cluster-name?cluster_id=${props.id}&new_cluster_name=${input}`)
      .catch(function (res) {
          if (res.response) {
              console.log(res.response.data.reason + " Please wait a few seconds and try reloading the page.");
          } else {
              console.log("Something went wrong. Please wait a few seconds and try reloading the page.")
          }
      });
  }

  function onEnter() {
    props.setUpdate(1)
    getClusters(input)
    setText(input)
  }

  function enterWorkspace() {
    Cookies.set('curent_workspace_id', props.id, { sameSite: 'none' , secure: true });
  }

  return (
      <Stack direction="column">
          

          <Button
              id="ClusterButton"
              className="ClusterButton"
              variant="contained"
              endIcon={<RocketLaunchIcon />}
              style={{
                  backgroundColor: 'black',
                  fontSize: 'medium'
              }}
              onClick={() => enterWorkspace()}
          >
              {text}
          </Button>
          <TextInput
              style={{
                  color: 'black',
                  padding: 0,
                  paddingLeft: 1,
                  justifyContent: 'left',
                  backgroundColor: 'white',
                  // textTransform: 'uppercase'
              }}
              onSubmitEditing={onEnter}
              onChange={(evt) => setInput(evt.target.value)}
              value={input}
          />
      </Stack>
  );
}