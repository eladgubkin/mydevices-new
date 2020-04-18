import React from "react";
import { createHttpLink } from "apollo-link-http";
import ApolloClient from "apollo-client";
import { InMemoryCache } from "apollo-cache-inmemory";
import { ApolloProvider } from "@apollo/react-hooks";
import { useLocalStorage } from "@rehooks/local-storage";
import AuthLayout from "./components/AuthLayout";
import GuestLayout from "./components/GuestLayout";

const customFetch = (uri, options) => {
  if (localStorage.getItem("jwtToken")) {
    options.headers.Authorization =
      "Bearer " + localStorage.getItem("jwtToken");
  } else {
    options.headers.Authorization =
      "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYW5vbnltb3VzIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6ImFub255bW91cyJ9fQ.cTmrTxKnKRFS6sb8VzIU85WPgu_qHW-kg7zXU3TIVM4";
  }
  return fetch(uri, options);
};

const client = new ApolloClient({
  link: createHttpLink({
    fetch: customFetch,
    uri: "http://localhost:8080/v1/graphql",
  }),
  cache: new InMemoryCache(),
});

const App = () => {
  const [jwtToken] = useLocalStorage("jwtToken");

  return (
    <ApolloProvider client={client}>
      {jwtToken ? <AuthLayout /> : <GuestLayout />}
    </ApolloProvider>
  );
};

export default App;
