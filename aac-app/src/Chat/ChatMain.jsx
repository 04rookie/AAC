import ChatWindow from "./ChatWindow";
import {
  Button,
  Card,
  CardContent,
  Checkbox,
  Grid,
  Typography,
} from "@mui/material";
import { useContext } from "react";
import { DataContext } from "../Context";
import Options from "./Options";
import CustomKeyboard from "./CustomKeyboard";
export default function ChatMain() {
  const { options, setOptions, toggle, setToggle } = useContext(DataContext);
  const receiveOptionChannel = new BroadcastChannel("options");
  receiveOptionChannel.onmessage = (event) => {
    // console.log(event.data);
    setOptions(event.data);
  };
  console.log(toggle);
  return (
    <Grid
      container
      spacing={0}
      style={{
        height: "100vh",
        width: "100vw",
        backgroundColor: "#2F2F2F",
        // backgroundColor: theme.palette.background.black,
      }}
    >
      <Grid size={{ xs: 12, md: 6 }}>
        <div
          style={{
            height: "100vh",
            minHeight: "-webkit-fill-available",
            width: "100%",
            overflowY: "scroll",
            overflowX: "hidden",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          {toggle == false ? (
            // <Button onClick={()=>setToggle(true)}>Toggle</Button>
            <CustomKeyboard />
          ) : (
            // <></>
            <Options />
          )}
        </div>
      </Grid>
      <Grid size={{ xs: 12, md: 6, height: "100%", width: "100%" }}>
        <div
          style={{
            // height: "100vh",
            height: "100%",
            // overflowY: "clip",
            width: "100%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
          }}
        >
          <ChatWindow type={"you"} />
        </div>
      </Grid>
    </Grid>
  );
}
