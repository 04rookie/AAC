import PropTypes from "prop-types";
import Card from "@mui/material/Card";
import {
  Button,
  CardContent,
  DialogActions,
  DialogContent,
  DialogContentText,
  Typography,
} from "@mui/material";
import { v4 as uuidv4 } from "uuid";
import { useContext, useEffect, useRef, useState } from "react";
// import { DateTime } from "luxon";
import DialogTitle from "@mui/material/DialogTitle";
import Dialog from "@mui/material/Dialog";
import { DataContext } from "../Context";
function Display({ message, type }) {
  const currentIndex = useRef(0);
  const { chat } = useContext(DataContext);
  const listRef = useRef(null);
  useEffect(() => {
    listRef.current.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [message]);

  useEffect(() => {
    console.log("chat", chat);
  }, [chat]);
  // console.log(chat);
  return (
    // <div style={{ height: "50vh", overflowY: "scroll" }}>
    <div
      // ref={listRef}
      style={{
        // border: "1px solid",
        height: "100%",
        // position: "relative",
        // height: "100%",
        overflowY: "scroll",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        // minHeight: "-webkit-fill-available",
      }}
    >
      {message.map((msg, index) => {
        return (
          <div
            style={{
              padding: "10px",
            }}
            key={uuidv4()}
          >
            <Card>
              <CardContent>
                <div
                  style={{
                    marginBottom: "10px",
                    display: "flex",
                    flexDirection: "row",
                    justifyContent: "space-between",
                  }}
                >
                  <div>
                    <Typography variant="h6">
                      {(msg.sender == "you" && type == "you") || (msg.sender == "them" && type == "them")? "You" : "Them"}
                    </Typography>
                  </div>
                  <div>
                    <Typography variant="caption">
                      {msg.time.toFormat("HH:mm:ss")}
                    </Typography>
                  </div>
                </div>
                <div>
                  <Typography variant="body1">{msg.message}</Typography>
                </div>
              </CardContent>
            </Card>
          </div>
        );
      })}
      <div ref={listRef} />
    </div>
    // </div>
  );
}

Display.propTypes = {
  message: PropTypes.array.isRequired,
};

export default Display;
