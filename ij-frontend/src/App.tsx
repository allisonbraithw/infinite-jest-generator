import React from "react";

import { Link, Outlet } from "react-router-dom";
import { Breadcrumb, BreadcrumbItem, BreadcrumbLink } from "@chakra-ui/react";

import "./App.css";

function App() {
  return (
    <>
      <Breadcrumb>
        <BreadcrumbItem>
          <BreadcrumbLink as={Link} to="/">Home</BreadcrumbLink>
        </BreadcrumbItem>
        <BreadcrumbItem>
          <BreadcrumbLink as={Link} to="/benchmarks">Benchmarks</BreadcrumbLink>
        </BreadcrumbItem>
      </Breadcrumb>
      <Outlet />
    </>
  )
}

export default App;
