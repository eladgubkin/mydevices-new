import React from "react";
import ApolloClient from "apollo-boost";
import { gql } from "apollo-boost";
import { GoogleLogin } from "react-google-login";

const App = () => {
  const responseGoogle = (response) => {
    const id_token = response.tokenObj.id_token;
    console.log(id_token);
    const client = new ApolloClient({
      uri: "http://localhost:8080/v1/graphql",
      headers: {
        "content-type": "application/json",
        "X-ID-Token": id_token,
      },
    });

    client
      .query({
        query: gql`
          {
            users {
              id
            }
          }
        `,
      })
      .then((result) => console.log(result));
  };

  return (
    <div id="app">
      <h3>Lol</h3>
      <GoogleLogin
        clientId="5512257356-q78clnbfa8ep4kl3nutlomv83gglnk1k.apps.googleusercontent.com"
        buttonText="Login"
        onSuccess={responseGoogle}
        onFailure={responseGoogle}
        cookiePolicy={"single_host_origin"}
      />
    </div>
  );
};

export default App;
