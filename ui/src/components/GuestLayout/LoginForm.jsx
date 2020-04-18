import React from "react";
import { GoogleLogin } from "react-google-login";
import { useMutation } from "@apollo/react-hooks";
import gql from "graphql-tag";
import { writeStorage } from "@rehooks/local-storage";

const LOGIN_WITH_GOOGLE = gql`
  mutation LoginWithGoogle($googleToken: String!) {
    loginWithGoogle(googleToken: $googleToken) {
      jwtToken
    }
  }
`;

const LOGIN_WITH_CREDENTIALS = gql`
  mutation LoginWithCredentials($email: String!, $password: String!) {
    loginWithCredentials(email: $email, password: $password) {
      jwtToken
    }
  }
`;

const REGISTER_WITH_CREDENTIALS = gql`
  mutation RegisterWithCredentials(
    $email: String!
    $password: String!
    $firstName: String!
    $lastName: String!
  ) {
    registerWithCredentials(
      email: $email
      password: $password
      firstName: $firstName
      lastName: $lastName
    ) {
      ok
    }
  }
`;

const LoginForm = () => {
  const [loginWithGoogle] = useMutation(LOGIN_WITH_GOOGLE);
  const [loginWithCredentials] = useMutation(LOGIN_WITH_CREDENTIALS);
  const [registerWithCredentials] = useMutation(REGISTER_WITH_CREDENTIALS);

  return (
    <div>
      <GoogleLogin
        clientId="5512257356-q78clnbfa8ep4kl3nutlomv83gglnk1k.apps.googleusercontent.com"
        cookiePolicy={"single_host_origin"}
        onSuccess={(res) => {
          loginWithGoogle({
            variables: { googleToken: res.tokenObj.id_token },
          }).then((result) => {
            writeStorage("jwtToken", result.data.loginWithGoogle.jwtToken);
          });
        }}
      />
      <button
        type="button"
        onClick={() => {
          loginWithCredentials({
            variables: {
              email: "eladoxyt@gmail.com",
              password: "12345",
            },
          }).then((result) => {
            writeStorage("jwtToken", result.data.loginWithCredentials.jwtToken);
          });
        }}
      >
        Sign in with credentials
      </button>
      <button
        type="button"
        onClick={() => {
          const email = "eladoxyt@gmail.com";
          const password = "12345";
          const firstName = "elad";
          const lastName = "gubkin";
          registerWithCredentials({
            variables: {
              email,
              password,
              firstName,
              lastName,
            },
          }).then((result) => {
            if (result.data.registerWithCredentials.ok) {
              loginWithCredentials({
                variables: {
                  email,
                  password,
                },
              }).then((res) => {
                writeStorage(
                  "jwtToken",
                  res.data.loginWithCredentials.jwtToken
                );
              });
            }
          });
        }}
      >
        Register with credentials
      </button>
    </div>
  );
};

export default LoginForm;
