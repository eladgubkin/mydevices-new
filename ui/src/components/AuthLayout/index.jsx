import React from "react";
import DevicesView from "./DevicesView";
import Logout from "./Logout";

const AuthLayout = () => {
  return (
    <>
      <h1>Auth Layout</h1>
      <DevicesView />
      <Logout />
    </>
  );
};

export default AuthLayout;
