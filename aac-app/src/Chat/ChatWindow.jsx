import { Button } from "@mui/material";
import OutlinedInput from "@mui/material/OutlinedInput";
import Display from "./Display";
import SendIcon from "@mui/icons-material/Send";
import { use, useContext, useEffect, useState } from "react";
import { DataContext } from "../Context";
import { v4 as uuidv4 } from "uuid";
import { DateTime } from "luxon";

// import { moment } from "moment";
function ChatWindow({ type }) {
  const { chat, setChat, currentMessage, setCurrentMessage, toggle, setToggle, setOptions } =
    useContext(DataContext);
  const { postMessage } = useContext(DataContext);
  const { showLoading } = useContext(DataContext);
  const sendChannel = new BroadcastChannel(type);
  useEffect(() => {
    const receiveChannel = new BroadcastChannel(type == "you" ? "them" : "you");
    receiveChannel.onmessage = (event) => {
      // console.log(event.data);
      let isUnique = true;
      chat.forEach((element) => {
        if (element.uuid == event.data.uuid) {
          isUnique = false;
        }
      });
      if (!isUnique) {
        return;
      }
      setChat((prev) => [
        ...prev,
        {
          message: event.data.message,
          sender: event.data.sender,
          time: DateTime.now(),
          urls: [],
          topics: [],
        },
      ]);
    };
  }, []);
  return (
    <div
      style={{
        height: "100%",
        width: "100%",
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        // overflowY: "auto",
      }}
    >
      <div
        style={{
          height: "59vh",
          marginTop: "5%",
          marginRight: "10%",
          marginLeft: "10%",
          marginBottom: "10%",
          border: "1px solid",
          borderColor: "white",
          borderRadius: "5px",
          display: "flex",
          flexDirection: "column",
        }}
      >
        <Display message={chat} type={type} />
        <div style={{ width: "100%", display: "flex", flexDirection: "row" }}>
          <div style={{ width: "100%", padding: "10px" }}>
            <OutlinedInput
              onKeyDown={(e) => {
                if (showLoading == false && e.key === "Enter") {
                  postMessage({
                    message: currentMessage,
                    type: type,
                    toggle: toggle,
                  });
                  let uuid = uuidv4();
                  if (type == "you" && toggle == false) {
                    // sendChannel.postMessage({
                    //   uuid: uuid,
                    //   message: currentMessage,
                    //   sender: type,
                    //   time: DateTime.now(),
                    //   urls: [],
                    //   topics: [],
                    // });
                    // setChat((prev) => [
                    //   ...prev,
                    //   {
                    //     uuid: uuid,
                    //     message: currentMessage,
                    //     sender: type,
                    //     time: DateTime.now(),
                    //     urls: [],
                    //     topics: [],
                    //   },
                    // ]);
                  }
                  if (type == "them") {
                    sendChannel.postMessage({
                      uuid: uuid,
                      message: currentMessage,
                      sender: type,
                      time: DateTime.now(),
                      urls: [],
                      topics: [],
                    });
                    setChat((prev) => [
                      ...prev,
                      {
                        uuid: uuid,
                        message: currentMessage,
                        sender: type,
                        time: DateTime.now(),
                        urls: [],
                        topics: [],
                      },
                    ]);
                  }
                  setOptions([]);
                  setToggle(true);
                  setCurrentMessage("");
                }
              }}
              fullWidth={true}
              value={currentMessage}
              onChange={(e) => {
                // if (!e.target.value.match(/^[0-9a-zA-Z?,. ]+$/) && e.target.value !== "") {
                //   return;
                // }
                setCurrentMessage(e.target.value);
              }}
            />
          </div>
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              padding: "10px",
            }}
          >
            <Button
              disabled={showLoading}
              onClick={() => {
                if (currentMessage.trim() == "") return;
                let uuid = uuidv4();
                postMessage({
                  message: currentMessage,
                  toggle: toggle,
                  type: type,
                });
                if (type == "you" && toggle == false) {
                  // sendChannel.postMessage({
                  //   uuid: uuid,
                  //   message: currentMessage,
                  //   sender: type,
                  //   time: DateTime.now(),
                  //   urls: [],
                  //   topics: [],
                  // });
                  // setChat((prev) => [
                  //   ...prev,
                  //   {
                  //     uuid: uuid,
                  //     message: currentMessage,
                  //     sender: type,
                  //     time: DateTime.now(),
                  //     urls: [],
                  //     topics: [],
                  //   },
                  // ]);
                }
                if (type == "them") {
                  sendChannel.postMessage({
                    uuid: uuid,
                    message: currentMessage,
                    sender: type,
                    time: DateTime.now(),
                    urls: [],
                    topics: [],
                  });
                  setChat((prev) => [
                    ...prev,
                    {
                      uuid: uuid,
                      message: currentMessage,
                      sender: type,
                      time: DateTime.now(),
                      urls: [],
                      topics: [],
                    },
                  ]);
                }
                setOptions([]);
                setToggle(true);
                setCurrentMessage("");
              }}
              variant="contained"
              endIcon={<SendIcon />}
            >
              {showLoading ? "Loading..." : "Send"}
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChatWindow;
