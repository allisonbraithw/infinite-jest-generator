import React, { useState } from "react";

import { graphql } from "../src/gql";
import { Input, Button, Flex, Spacer, Container, Image } from "@chakra-ui/react";

import "./App.css";
import { useLazyQuery } from "@apollo/client";

// Sample Query-- the codegen does not create code that compiles if there are
// no queries registered via the 'graphql' function
const getCharacterQueryDocument = graphql(`
  query GetCharacter($fullName: String!) {
    character(fullName: $fullName) {
      fullName
      description
      portraitLink
    }
  }
`);

function App() {
  const [character, setCharacter] = useState("")
  const [loadCharacter, { called, loading, data }] = useLazyQuery(getCharacterQueryDocument)

  const handleButtonClick = () => {
    loadCharacter({ variables: { fullName: character } });
  };

  return (
    <>
      <Flex p={4}>
        <Input placeholder="Hal Incandenza" value={character} onChange={(e) => setCharacter(e.target.value)} />
        <Spacer p={4} />
        <Button onClick={handleButtonClick}>Submit</Button>
      </Flex>
      <Flex p={4}>
        {called && loading && <Container borderRadius="xl" border="2px solid">Loading...</Container>}
        {data && data.character && <Container borderRadius="xl" border="2px solid">{data?.character?.description}</Container>}
      </Flex>
      {data && data.character &&
        <Flex p={4}>
          <Container>
            <Image src={data.character.portraitLink!} alt={data?.character?.fullName} />
          </Container>
        </Flex>}
    </>
  )
}

export default App;
