import logo from "./logo.svg";
import "./App.css";
import { DataProvider } from "./Context";
import { createTheme, ThemeProvider } from "@mui/material/styles";

function App() {
  const theme = createTheme({
    palette: {
      mode: "dark",
      primary: {
        main: "#7A288A", // purple
        light: "#9C4DC6", // lighter purple
        dark: "#4B0E6E", // darker purple
        contrastText: "#FFFFFF", // white
      },
      secondary: {
        main: "#FFC107", // orange-yellow
        light: "#FFD95B", // lighter orange-yellow
        dark: "#FFA000", // darker orange-yellow
        contrastText: "#000000", // black
      },
      background: {
        default: "#2F2F2F", // dark gray
        black: "#000000", // dark gray
        paper: "#333333", // darker gray
      },
      text: {
        primary: "#FFFFFF", // white
        secondary: "#AAAAAA", // light gray
        disabled: "#666666", // medium gray
      },
      error: {
        main: "#F44336", // red
        light: "#FFC4C4", // lighter red
        dark: "#B71C1C", // darker red
        contrastText: "#FFFFFF", // white
      },
      warning: {
        main: "#FF9800", // orange
        light: "#FFD95B", // lighter orange
        dark: "#FFA000", // darker orange
        contrastText: "#000000", // black
      },
      info: {
        main: "#2196F3", // blue
        light: "#64B5F6", // lighter blue
        dark: "#1565C0", // darker blue
        contrastText: "#FFFFFF", // white
      },
      success: {
        main: "#4CAF50", // green
        light: "#6BC46B", // lighter green
        dark: "#2E865F", // darker green
        contrastText: "#FFFFFF", // white
      },
    },
  });
  return (
    <ThemeProvider theme={theme}>
      <DataProvider>
        <div className="App">
          Hello!
        </div>
      </DataProvider>
    </ThemeProvider>
  );
}

export default App;
