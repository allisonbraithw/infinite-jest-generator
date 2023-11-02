import React from "react";

import {
    Button,
    Table,
    Thead,
    Tbody,
    Tr,
    Th,
    Td,
    TableCaption,
    TableContainer,
} from '@chakra-ui/react'
import { graphql } from "../src/gql";
import { Character } from "../src/graphql.ts"
import { useLazyQuery } from "@apollo/client";



const getCharacterEvaluationDocument = graphql(`
  query GetCharacterEvaluation($fullName: String!) {
    character(fullName: $fullName) {
      fullName
      description
      evaluation {
        relevancy
        explanation
      }
    }
  }
`);

function Benchmark() {
    const [characterEvals, setCharacterEvals] = React.useState<Character[]>([])
    const [loadCharacterEval, { loading }] = useLazyQuery(getCharacterEvaluationDocument, {
        onCompleted: (data) => {
            setCharacterEvals(characterEvals => [...characterEvals, data.character])
        }
    })

    const handleSubmit = () => {
        loadCharacterEval({ variables: { fullName: "Hal Incandenza" } });
    };

    return (
        <>
            <Button isLoading={loading} onClick={handleSubmit}>Generate</Button>
            <TableContainer p={4}>
                <Table variant='simple'>
                    <TableCaption>Relevancy Assessments of Main Characters</TableCaption>
                    <Thead>
                        <Tr>
                            <Th>Character</Th>
                            <Th>Description</Th>
                            <Th isNumeric>Relevancy</Th>
                            <Th>Explanation</Th>
                        </Tr>
                    </Thead>
                    <Tbody>
                        {characterEvals.map((characterEval) =>
                            <Tr>
                                <Td>{characterEval.fullName}</Td>
                                <Td>{characterEval.description}</Td>
                                <Td isNumeric>{characterEval.evaluation.relevancy}</Td>
                                <Td>{characterEval.evaluation.explanation}</Td>
                            </Tr>
                        )}
                    </Tbody>
                </Table>
            </TableContainer>
        </>
    )
}

export default Benchmark;