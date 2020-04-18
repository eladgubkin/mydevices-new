import React from "react";
import { deleteFromStorage } from "@rehooks/local-storage";

const Logout = () => {
  return (
    <button
      type="button"
      onClick={() => {
        deleteFromStorage("jwtToken");
      }}
    >
      Logout?
    </button>
  );
};

export default Logout;
