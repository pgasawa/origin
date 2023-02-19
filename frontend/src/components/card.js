import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import RocketLaunchIcon from "@mui/icons-material/RocketLaunch";
import './card.css'
import React, { useState, useEffect } from 'react';
import { Text, TextInput, View } from 'react-native';



export default function Cluster(props) {
  const [text, setText] = useState(props.title);
  function onEnter(newText) {
    setText(newText); 
    document.getElementById("ClusterButton").innerHTML = newText;
    }
  return (
    <Stack direction="column">
      <TextInput
        style={{
          color: "black",
          padding: 0,
          paddingLeft: 1,
          justifyContent: "left",
          backgroundColor: 'white',
          textTransform: "lowercase"
        }}
        placeholder="edit me"
        onSubmitEditing={(newText) => onEnter(newText)}
      />

      <Button
        id="ClusterButton"
        className="ClusterButton"
        variant="contained"
        endIcon={<RocketLaunchIcon />}
        style={{
          backgroundColor: 'black',
          fontSize: 'medium'
        }}
      > {text}
      </Button>
    </Stack>

  );
}
