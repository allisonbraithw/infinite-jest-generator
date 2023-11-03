import React from "react";

import {
    Button,
    Flex,
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
import { set } from "lodash";

const CHARACTERS = ["Hal Incandenza", "Orin Incandenza", "Don Gately", "Joelle Van Dyne"]

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
    const [characterIndex, setCharacterIndex] = React.useState(0)
    const [loadCharacterEval, { loading }] = useLazyQuery(getCharacterEvaluationDocument, {
        onCompleted: (data) => {
            setCharacterEvals(characterEvals => [...characterEvals, data.character])
        }
    })

    const handleSubmit = () => {
        if (characterIndex >= CHARACTERS.length) {
            return;
        }
        loadCharacterEval({ variables: { fullName: CHARACTERS[characterIndex] } });
        setCharacterIndex(characterIndex + 1)
    };

    return (
        <>
            <Flex p={4} justify="right">
                <Button isLoading={loading} onClick={handleSubmit} isDisabled={characterIndex >= CHARACTERS.length}>Generate {CHARACTERS[characterIndex]}</Button>
            </Flex>
            <TableContainer p={4}>
                <Table variant='simple' layout='fixed'>
                    <TableCaption>Relevancy Assessments of Main Characters</TableCaption>
                    <Thead>
                        <Tr>
                            <Th>Character</Th>
                            <Th width="35%">Description</Th>
                            <Th isNumeric>Relevancy</Th>
                            <Th width="35%">Explanation</Th>
                        </Tr>
                    </Thead>
                    <Tbody>
                        {characterEvals.map((characterEval) =>
                            <Tr key={characterEval.fullName}>
                                <Td>{characterEval.fullName}</Td>
                                <Td whiteSpace="normal" wordBreak="break-word">{characterEval.description}</Td>
                                <Td isNumeric>{characterEval.evaluation.relevancy}</Td>
                                <Td whiteSpace="normal" wordBreak="break-word">{characterEval.evaluation.explanation}</Td>
                            </Tr>
                        )}
                    </Tbody>
                </Table>
            </TableContainer>
        </>
    )
}

export default Benchmark;