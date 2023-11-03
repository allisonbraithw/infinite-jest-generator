import React from "react";
import ReactDOM from "react-dom/client";
import {
  createBrowserRouter,
  RouterProvider
} from "react-router-dom"

import { ApolloProvider } from "@apollo/client";
import { ChakraProvider } from "@chakra-ui/react";
import { client } from "./gqlClient";

import App from "./App.tsx";
import Benchmark from "./Benchmark.tsx";
import ImageGenerator from "./ImageGenerator.tsx";
// import "./index.css";
import "./styles.css";

const router = createBrowserRouter([
  {
    path: "/",
    element: <App />,
    children: [
      {
        path: "/benchmarks",
        element: <Benchmark />
      },
      {
        path: "/",
        element: <ImageGenerator />
      },
    ],
  },
]);

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ChakraProvider>
      <ApolloProvider client={client}>
        <RouterProvider router={router} />
      </ApolloProvider>
    </ChakraProvider>
  </React.StrictMode>
);
