// createContext.js
import { createContext, useEffect, useRef, useState } from "react";
import PropTypes from "prop-types";
const DataContext = createContext();
import axios from "axios";
import { DateTime } from "luxon";

const DataProvider = ({ children }) => {
  const instance = axios.create({
    // baseURL: "http://127.0.0.1:9999",
    // baseURL: "http://127.0.0.1:9999",
    // baseURL: "http://35.184.42.87:9999",
    baseURL: "http://127.0.0.1:5000",
    // httpsAgent: new https.Agent({
    //   rejectUnauthorized: false,
    // }),
  });
  // const [chatID, setChatID] = useState(null);
  const [showLoading, setShowLoading] = useState(false);
  const [chat, setChat] = useState([]);
  const [options, setOptions] = useState([]);
  const optionsChannel = new BroadcastChannel("options");
  const [toggle, setToggle] = useState(true);
  const [currentMessage, setCurrentMessage] = useState("");
  // const [filter, setFilter] = useState({
  //   Health: false,
  //   Environment: false,
  //   Technology: false,
  //   Economy: false,
  //   Entertainment: false,
  //   Sports: false,
  //   Politics: false,
  //   Education: false,
  //   Travel: false,
  //   Food: false,
  // });
  // const [topicFrequency, setTopicFrequency] = useState({
  //   Health: 0,
  //   Environment: 0,
  //   Technology: 0,
  //   Economy: 0,
  //   Entertainment: 0,
  //   Sports: 0,
  //   Politics: 0,
  //   Education: 0,
  //   Travel: 0,
  //   Food: 0,
  //   General: 0,
  // });
  // const topicUpdated = useRef(false);
  // const stop = useRef(false);
  // useEffect(() => {
  //   if (stop.current == false) {
  //     setShowLoading(true);
  //     instance
  //       .post(
  //         "/init",

  //         {
  //           topics: [],
  //         },
  //         { timeout: 20000 }
  //       )
  //       .then((res) => {
  //         // console.log(res?.data);
  //         // setChatID(res?.data?.chatID);
  //         // setChat(() => [
  //         //   {
  //         //     message: res?.data?.content,
  //         //     sender: "bot",
  //         //     time: DateTime.now(),
  //         //     urls: [],
  //         //     topics: [],
  //         //   },
  //         // ]);
  //         // stop.current = true;
  //         setShowLoading(false);
  //       })
  //       .catch((err) => {
  //         if(err?.response?.data?.content == "Queue Overflow") {
  //           stop.current = true;
  //           setChat((prev) => [
  //             ...prev,
  //             {
  //               message:
  //                 "Server is under heavy load. Please try again later. (GCP is expensive!) :( ",
  //               sender: "bot",
  //               time: DateTime.now(),
  //               urls: [],
  //               topics: [],
  //             },
  //           ]);
  //           return;
  //         }
  //         console.log("Error, failed to call init");
  //         stop.current = true;
  //         // code to handle timeout
  //         setChat((prev) => [
  //           ...prev,
  //           {
  //             message:
  //               "Failed to connect to the server. Please try again later. :( ",
  //             sender: "bot",
  //             time: DateTime.now(),
  //             urls: [],
  //             topics: [],
  //           },
  //         ]);
  //         setShowLoading(false);
  //       });
  //   }
  // }, []);

  async function postResponse(data){
    try {
      setShowLoading(true);
      const res = await instance.post(
        "/respond",
        {
          index: data.index,
        },
        { timeout: 40000 }
      );
      setShowLoading(false);
    } catch (err) {
      console.log(err);
      setChat((prev) => [
        ...prev,
        {
          message:
            "Failed to connect to the server. Please try again later. :( ",
          sender: "bot",
          time: DateTime.now(),
          urls: [],
          topics: [],
        },
      ]);
      setShowLoading(false);
    }
    return;
  }
  async function postMessage(data) {
    try {
      setShowLoading(true);
      const res = await instance.post(
        "/chat",
        {
          // chatID: chatID,
          prompt: data.message?.replace(/[^a-zA-Z0-9\s]/g, ""),
          type: data?.type,
          toggle: data?.toggle,
          // updTopic: topicUpdated.current,
          // topics: selectedTopics,
        },
        { timeout: 40000 }
      );
      // console.log(res?.data);
      optionsChannel.postMessage(res?.data?.options);
      // topicUpdated.current = false;
      // setChat((prev) => {
      //   return [
      //     ...prev,
      //     {
      //       message: res?.data?.content?.message,
      //       sender: "bot",
      //       time: DateTime.now(),
      //       urls: res?.data?.content?.meta?.urls ?? [],
      //       topics: res?.data?.content?.meta?.topics ?? [],
      //     },
      //   ];
      // });
      if (
        res?.data?.content?.message ==
        "Bye Bye!! Please refresh the page to start chatting again"
      ) {
        // stop.current = true;
        setShowLoading(true);
        return;
      }
      setShowLoading(false);
    } catch (err) {
      console.log(err);
      setChat((prev) => [
        ...prev,
        {
          message:
            "Failed to connect to the server. Please try again later. :( ",
          sender: "bot",
          time: DateTime.now(),
          urls: [],
          topics: [],
        },
      ]);
      // stop.current = false;
      setShowLoading(false);
    }
    return;
  }
  // console.log(topicFrequency);

  // useEffect(() => {
  //   const handleBeforeUnload = (event) => {
  //     // Prevent default action and show confirmation dialog
  //     event.preventDefault();
  //     event.returnValue = "Are you sure you want to close?"; // This is required for some browsers
  //     instance.post("/end", { chatID: chatID });
  //   };

  //   // Add event listener
  //   window.addEventListener("beforeunload", handleBeforeUnload);

  //   // Cleanup function to remove event listener
  //   return () => {
  //     window.removeEventListener("beforeunload", handleBeforeUnload);
  //   };
  // }, []);
  // console.log(chat);
  return (
    <DataContext.Provider
      value={{
        chat,
        setChat,
        // filter,
        // setFilter,
        showLoading,
        setShowLoading,
        // chatID,
        postMessage,
        // topicUpdated,
        // topicFrequency,
        options,
        setOptions,
        postResponse,
        toggle, 
        setToggle,
        setCurrentMessage,
        currentMessage,
      }}
    >
      {children}
    </DataContext.Provider>
  );
};

DataProvider.propTypes = {
  children: PropTypes.node.isRequired,
};

export { DataProvider, DataContext };
