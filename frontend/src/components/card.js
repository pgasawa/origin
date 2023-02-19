import * as React from "react";
import Box from "@mui/material/Box";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import Typography from "@mui/material/Typography";

export default function Cluster() {
  return (
    <Card sx={{ maxWidth: 300 }}>
      <CardContent>
        <Typography variant="h5" component="div">
          CS 189
        </Typography>
        <hr />
        <Button size="medium">LAUNCH WORKSPACE</Button>
      </CardContent>
    </Card>
  );
}
