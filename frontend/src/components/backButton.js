import Button from "@mui/material/Button";
import Stack from "@mui/material/Stack";
import RocketLaunchIcon from "@mui/icons-material/RocketLaunch";
import './card.css'
import React, { useState, useEffect } from 'react';
import { Text, TextInput, View } from 'react-native';
import axios from 'axios'
import Cookies from 'js-cookie';
// import { useNavigate } from "react-router-dom";

export default function backButton(setUpdate) {
  function exitWorkspace() {
    Cookies.remove('curent_workspace_id');
    setUpdate(1)
  }

  return (
          <Button
              className="ClusterButton"
              variant="contained"
              endIcon={<RocketLaunchIcon />}
              style={{
                  backgroundColor: 'black',
                  fontSize: 'medium'
              }}
              onClick={() => exitWorkspace()}
          >
              Exit Workspace
          </Button>
  );
}