import React, { useContext } from "react";
import { DataContext } from "../Context";
import { Button, Typography } from "@mui/material";
import { v4 as uuidv4 } from "uuid";
import { DateTime } from "luxon";
export default function Options() {
  const { options, setOptions, setChat, postResponse, toggle, setToggle } =
    useContext(DataContext);
  const sendChannel = new BroadcastChannel("you");
  return (
    <div>
      {options.map((option, index) => {
        return (
          <div
            onClick={() => {
              let uuid = uuidv4();
              sendChannel.postMessage({
                uuid: uuid,
                message: option,
                sender: "you",
                time: DateTime.now(),
                urls: [],
                topics: [],
              });
              setChat((prev) => [
                ...prev,
                {
                  message: option,
                  sender: "you",
                  time: DateTime.now(),
                  urls: [],
                  topics: [],
                },
              ]);
              postResponse({
                index: index,
              });
              setOptions([]);
            }}
          >
            <Typography
              key={index}
              variant="subtitle2"
              style={{
                color: "white",
                margin: "10px",
                padding: "10px",
                //   backgroundColor: "#3F3F3F",
                borderRadius: "5px",
              }}
            >
              {index + 1}
              {": "}
              {option}
            </Typography>
          </div>
        );
      })}
      <Button onClick={()=>setToggle(false)} variant="contained">
        Custom Keyboard
      </Button>
    </div>
  );
}
