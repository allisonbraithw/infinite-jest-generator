/* eslint-disable */
import { TypedDocumentNode as DocumentNode } from '@graphql-typed-document-node/core';
export type Maybe<T> = T | null;
export type InputMaybe<T> = Maybe<T>;
export type Exact<T extends { [key: string]: unknown }> = { [K in keyof T]: T[K] };
export type MakeOptional<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]?: Maybe<T[SubKey]> };
export type MakeMaybe<T, K extends keyof T> = Omit<T, K> & { [SubKey in K]: Maybe<T[SubKey]> };
export type MakeEmpty<T extends { [key: string]: unknown }, K extends keyof T> = { [_ in K]?: never };
export type Incremental<T> = T | { [P in keyof T]?: P extends ' $fragmentName' | '__typename' ? T[P] : never };
/** All built-in and custom scalars, mapped to their actual values */
export type Scalars = {
  ID: { input: string; output: string; }
  String: { input: string; output: string; }
  Boolean: { input: boolean; output: boolean; }
  Int: { input: number; output: number; }
  Float: { input: number; output: number; }
};

export type Character = {
  __typename?: 'Character';
  alternativeNames?: Maybe<Array<Maybe<Scalars['String']['output']>>>;
  description: Scalars['String']['output'];
  evaluation?: Maybe<DescriptionEval>;
  fullName: Scalars['String']['output'];
  portraitLink?: Maybe<Scalars['String']['output']>;
  sources: Array<Maybe<Scalars['String']['output']>>;
};

export type DescriptionEval = {
  __typename?: 'DescriptionEval';
  explanation?: Maybe<Scalars['String']['output']>;
  relevancy?: Maybe<Scalars['String']['output']>;
};

export type Query = {
  __typename?: 'Query';
  character?: Maybe<Character>;
};


export type QueryCharacterArgs = {
  fullName: Scalars['String']['input'];
};

export type GetCharacterEvaluationQueryVariables = Exact<{
  fullName: Scalars['String']['input'];
}>;


export type GetCharacterEvaluationQuery = { __typename?: 'Query', character?: { __typename?: 'Character', fullName: string, description: string, evaluation?: { __typename?: 'DescriptionEval', relevancy?: string | null, explanation?: string | null } | null } | null };

export type GetCharacterPortraitQueryVariables = Exact<{
  fullName: Scalars['String']['input'];
}>;


export type GetCharacterPortraitQuery = { __typename?: 'Query', character?: { __typename?: 'Character', fullName: string, description: string, portraitLink?: string | null } | null };


export const GetCharacterEvaluationDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"GetCharacterEvaluation"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"fullName"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"character"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"fullName"},"value":{"kind":"Variable","name":{"kind":"Name","value":"fullName"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"evaluation"},"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"relevancy"}},{"kind":"Field","name":{"kind":"Name","value":"explanation"}}]}}]}}]}}]} as unknown as DocumentNode<GetCharacterEvaluationQuery, GetCharacterEvaluationQueryVariables>;
export const GetCharacterPortraitDocument = {"kind":"Document","definitions":[{"kind":"OperationDefinition","operation":"query","name":{"kind":"Name","value":"GetCharacterPortrait"},"variableDefinitions":[{"kind":"VariableDefinition","variable":{"kind":"Variable","name":{"kind":"Name","value":"fullName"}},"type":{"kind":"NonNullType","type":{"kind":"NamedType","name":{"kind":"Name","value":"String"}}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"character"},"arguments":[{"kind":"Argument","name":{"kind":"Name","value":"fullName"},"value":{"kind":"Variable","name":{"kind":"Name","value":"fullName"}}}],"selectionSet":{"kind":"SelectionSet","selections":[{"kind":"Field","name":{"kind":"Name","value":"fullName"}},{"kind":"Field","name":{"kind":"Name","value":"description"}},{"kind":"Field","name":{"kind":"Name","value":"portraitLink"}}]}}]}}]} as unknown as DocumentNode<GetCharacterPortraitQuery, GetCharacterPortraitQueryVariables>;