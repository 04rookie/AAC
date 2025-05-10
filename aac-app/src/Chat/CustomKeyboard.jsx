import { useContext } from "react";
import { DataContext } from "../Context";
import { Button, Grid } from "@mui/material";

export default function CustomKeyboard() {
  const {
    options,
    setOptions,
    setChat,
    postResponse,
    toggle,
    setToggle,
    setCurrentMessage,
    currentMessage,
  } = useContext(DataContext);
  const names = [
    "Banana",
    "For",
    "You",
    "Me",
    "Us",
    "Them",
    "They",
    "We",
    "I",
    "You and Me",
    "You and I",
    "Yes",
    "No",
    "Maybe",
    "Definitely",
    "Beautiful",
  ];
  return (
    <div style={{ padding: "20px" }}>
      <Grid container spacing={2}>
        {names.map((name, index) => {
          return (
            <Grid item xs={6} lg={6} md={6} key={index}>
              <Button
                onClick={() => {
                  // setToggle(true);
                  setCurrentMessage((prev) => {
                    return prev + " " + name;
                  });
                }}
                style={{ borderWidth: "2px" }}
                variant="outlined"
              >
                {name}
              </Button>
            </Grid>
          );
        })}
        <Grid item xs={6} lg={6} md={6}>
          <Button
            onClick={() => {
              setToggle(true);
            }}
            style={{ borderWidth: "2px" }}
            variant="outlined"
          >
            Go back
          </Button>
        </Grid>
      </Grid>
    </div>
  );
}
