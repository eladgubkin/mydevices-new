import React from "react";
import ApolloClient from "apollo-boost";
import { gql } from "apollo-boost";
import { GoogleLogin, GoogleLogout } from "react-google-login";

const App = () => {
  const responseGoogle = (response) => {
    const id_token = response.tokenObj.id_token;
    console.log(id_token);
    const client = new ApolloClient({
      uri: "http://localhost:8080/v1/graphql",
      headers: {
        "content-type": "application/json",
        Authorization:
          "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJodHRwczovL2hhc3VyYS5pby9qd3QvY2xhaW1zIjp7IngtaGFzdXJhLWFsbG93ZWQtcm9sZXMiOlsiYW5vbnltb3VzIl0sIngtaGFzdXJhLWRlZmF1bHQtcm9sZSI6ImFub255bW91cyJ9fQ.MC-ofrg48ykY8nGdr5ZHQcUhFoGB01dirjDGXfz5KiY",
      },
    });

    client
      .mutate({
        mutation: gql`
          mutation LoginWithGoogle($googleToken: String!) {
            loginWithGoogle(googleToken: $googleToken) {
              jwtToken
            }
          }
        `,
        variables: {
          googleToken: id_token,
        },
      })
      .then((result) => {
        localStorage.setItem("jwtToken", result.data.loginWithGoogle.jwtToken);
        const loggedInClient = new ApolloClient({
          uri: "http://localhost:8080/v1/graphql",
          headers: {
            "content-type": "application/json",
            Authorization: "Bearer " + result.data.loginWithGoogle.jwtToken,
          },
        });

        loggedInClient
          .query({
            query: gql`
              {
                users {
                  id
                  email
                  first_name
                  last_name
                  google_userid
                  devices {
                    id
                    name
                    description
                  }
                }
              }
            `,
          })
          .then((result) => console.log(result));
      });
  };

  return (
    <div id="app">
      <h3>Lol</h3>
      <GoogleLogin
        clientId="5512257356-q78clnbfa8ep4kl3nutlomv83gglnk1k.apps.googleusercontent.com"
        onSuccess={responseGoogle}
        onFailure={responseGoogle}
        cookiePolicy={"single_host_origin"}
      />
      <GoogleLogout
        clientId="5512257356-q78clnbfa8ep4kl3nutlomv83gglnk1k.apps.googleusercontent.com"
        buttonText="Logout"
        onLogoutSuccess={() => console.log("logout")}
      />
    </div>
  );
};

export default App;
