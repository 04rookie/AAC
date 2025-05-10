import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import {
  Outlet,
  RouterProvider,
  createRootRoute,
  createRoute,
  createRouter,
} from "@tanstack/react-router";
import { TanStackRouterDevtools } from "@tanstack/react-router-devtools";
import { DataProvider } from "./Context";
import { createTheme, ThemeProvider } from "@mui/material/styles";

import "./styles.css";
import reportWebVitals from "./reportWebVitals.js";

import App from "./App.jsx";
import ChatMain from "./Chat/ChatMain.jsx";
import ChatUser from "./Chat/ChatUser.jsx";

const rootRoute = createRootRoute({
  component: () => (
    <>
      <Outlet />
      <TanStackRouterDevtools />
    </>
  ),
});

const indexRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/",
  component: App,
});

// Example of adding additional routes/pages
const userRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/user",
  component: () => <ChatUser />,
});

const aacRoute = createRoute({
  getParentRoute: () => rootRoute,
  path: "/aac",
  component: () => <ChatMain />,
});

// Add the new routes to the route tree
const routeTree = rootRoute.addChildren([indexRoute, userRoute, aacRoute]);

const router = createRouter({
  routeTree,
  context: {},
  defaultPreload: "intent",
  scrollRestoration: true,
  defaultStructuralSharing: true,
  defaultPreloadStaleTime: 0,
});

const rootElement = document.getElementById("app");
if (rootElement && !rootElement.innerHTML) {
  const root = ReactDOM.createRoot(rootElement);
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
  root.render(
    // <StrictMode>
      <ThemeProvider theme={theme}>
        <DataProvider>
          <RouterProvider router={router} />
        </DataProvider>
      </ThemeProvider>
    // {/* </StrictMode> */}
  );
}
// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
