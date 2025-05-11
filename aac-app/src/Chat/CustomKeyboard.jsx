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
  // const names = [
  //   "Banana",
  //   "For",
  //   "You",
  //   "Me",
  //   "Us",
  //   "Them",
  //   "They",
  //   "We",
  //   "I",
  //   "You and Me",
  //   "You and I",
  //   "Yes",
  //   "No",
  //   "Maybe",
  //   "Definitely",
  //   "Beautiful",
  // ];

  // const names = [
  //   "school",
  //   "new",
  //   "friends",
  //   "hockey",
  //   "softball",
  //   "goalie",
  //   "gym",
  //   "cafeteria",
  //   "classrooms",
  //   "board",
  //   "frustrated",
  //   "patient",
  //   "understand",
  //   "communicate",
  //   "excited",
  //   "nervous",
  //   "practice",
  //   "calm",
  //   "opportunity",
  //   "advice",
  //   "fun",
  //   "awesome",
  //   "play",
  //   "block",
  //   "save",
  //   "stop",
  //   "snowstorm",
  //   "snow",
  //   "water",
  //   "melting",
  //   "storm",
  //   "work",
  //   "together",
  //   "memory",
  //   "happy",
  //   "meet",
  //   "adjusting",
  //   "communication",
  //   "barrier",
  //   "aggravated",
  //   "convey",
  //   "thoughts",
  //   "encouraging",
  //   "adapting",
  //   "wheelchair",
  //   "crawl",
  //   "net",
  //   "position",
  //   "playground",
  //   "student",
  //   "teachers",
  //   "talk",
  //   "conversation",
  //   "listen",
  //   "smile",
  //   "freedom",
  //   "end",
  //   "year",
  //   "patient",
  //   "learn",
  //   "time",
  //   "experience",
  //   "handle",
  //   "deal",
  //   "understood",
  //   "remind",
  //   "scared",
  //   "adjust",
  //   "environment",
  //   "feeling",
  //   "overwhelming",
  //   "big",
  //   "kids",
  //   "confident",
  //   "advice",
  //   "cope",
  //   "getting",
  //   "used",
  //   "talking",
  //   "teaching",
  //   "teammates",
  //   "softballs",
  //   "game",
  //   "match",
  //   "opponent",
  //   "score",
  //   "goal",
  //   "challenge",
  //   "encouragement",
  //   "practice",
  //   "learning",
  //   "skills",
  //   "help",
  //   "support",
  //   "confide",
  //   "overcome",
  //   "connect",
  //   "empathy",
  //   "patience",
  //   "trust",
  //   "confidence",
  //   "bravery",
  // ];

  const names = [
    "school",
    "friends",
    "hockey",
    "softball",
    "goalie",
    "gym",
    "board",
    "frustrated",
    "patient",
    "communicate",
    "nervous",
    "practice",
    "calm",
    "memory",
    "snowstorm",
    "adjusting",
    "conversation",
    "smile",
    "freedom",
  ];
  return (
    <div style={{ padding: "20px" }}>
      <Grid container spacing={2}>
        {names.map((name, index) => {
          return (
            <Grid item xs={6} lg={6} md={6} key={index}>
              <Button
                color={"secondary"}
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
            color={"secondary"}
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
