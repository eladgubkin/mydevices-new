import React from "react";
import { useQuery } from "@apollo/react-hooks";
import gql from "graphql-tag";

const DevicesView = () => {
  const { loading, error, data } = useQuery(gql`
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
  `);

  if (loading) return <h2>Loading...</h2>;
  if (error) console.log(`Error! ${error.message}`);

  return (
    <div>
      {data.users.map((user, i) => (
        <div key={i}>
          <h3>{user.email}</h3>
          <h4>
            {user.first_name} {user.last_name}
          </h4>
        </div>
      ))}
    </div>
  );
};

export default DevicesView;
