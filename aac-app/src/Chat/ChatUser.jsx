import ChatWindow from "./ChatWindow";
import {
  Button,
  Card,
  CardContent,
  Checkbox,
  Grid,
  Typography,
} from "@mui/material";

export default function ChatUser() {
  return (
    <div
      style={{
        height: "100vh",
        width: "100vw",
        backgroundColor: "#2F2F2F",
        // backgroundColor: theme.palette.background.black,
      }}
    >
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
        <ChatWindow type={"them"}/>
      </div>
    </div>
  );
}
