import os
import re
import sys
import pickle

import chromadb
import tiktoken
import openai
import nltk

import PyPDF2 as pdf
from sentence_transformers import SentenceTransformer

openai.organization = "org-ZuOE6yBYZ9VQVlkltTqj4UzF"
openai.api_key = "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"


def split_text_with_overlap(text, num_sentences=3, overlap=1):
    nltk.download("punkt")
    sentences = nltk.sent_tokenize(text)
    chunks = []
    start_idx = 0
    while start_idx < len(sentences):
        end_idx = min(start_idx + num_sentences, len(sentences))
        chunk = " ".join(sentences[start_idx:end_idx])
        chunks.append(chunk)
        start_idx += num_sentences - overlap

    return chunks


def load_or_open_chunks_and_pages(book_name: str = "infinite-jest", root_dir: str = "../../data/"):
    # Open and load the PDF
    # Check if the txt file exists
    pdf_name = f"{root_dir}{book_name}.pdf"
    # txt_name = f"{root_dir}{book_name}.txt"
    chunk_name = f"{root_dir}{book_name}-chunks.txt"
    page_name = f"{root_dir}{book_name}-pages.txt"

    if os.path.isfile(page_name) and os.path.isfile(chunk_name):
        with open(chunk_name, "rb") as ijc:
            infiniteJestChunks = pickle.load(ijc)

        with open(page_name, "rb") as ijp:
            infiniteJestPages = pickle.load(ijp)
    else:
        print(" Text not found, generating now")
        pdfFileObj = open(pdf_name, "rb")

        infiniteJestReader = pdf.PdfReader(pdfFileObj)

        infiniteJestPages = []
        infiniteJestString = ""

        for page in infiniteJestReader.pages:
            text = page.extract_text()
            # Merge hyphenated words
            text = re.sub(r"(\w+)-\n(\w+)", r"\1\2", text)
            # Fix newlines in the middle of sentences
            text = re.sub(r"(?<!\n\s)\n(?!\s\n)", " ", text.strip())
            # Remove multiple newlines
            text = re.sub(r"\n\s*\n", "\n\n", text)
            infiniteJestPages.append(text)
            infiniteJestString += text

        infiniteJestChunks = split_text_with_overlap(infiniteJestString, 20, 3)

        with open("./infinite-jest-pages.txt", "wb") as ijp:
            pickle.dump(infiniteJestPages, ijp)

        with open("./infinite-jest-chunks.txt", "wb") as ijc:
            pickle.dump(infiniteJestChunks, ijc)
        pdfFileObj.close()

    return infiniteJestPages, infiniteJestChunks


def initialize_vector_db(chunks: list, embeddings: list = None):
    id_list = [str(item) for item in range(0, len(chunks))]
    # todo(arb): this step takes a while, should just store it somewhere
    chroma_client = chromadb.Client()
    collection = chroma_client.create_collection(name="infinite_jest")
    collection.add(
        embeddings=embeddings,
        documents=chunks,
        ids=id_list,
    )

    return chroma_client, collection


def limit_docs_by_tokens(documents: list, model: str = "gpt-3.5-turbo", token_limit: int = 2000):
    # Include as many of the results documents that will fit
    encoding = tiktoken.encoding_for_model(model)
    token_limited_results = []
    tokens_remaining = token_limit
    for doc in documents:
        number_of_tokens = len(encoding.encode(doc))
        # If the current doc is too big, keep checking in case there's a smaller one
        if number_of_tokens > tokens_remaining:
            continue
        token_limited_results.append(doc)
        tokens_remaining -= number_of_tokens

    return token_limited_results


def get_character_description_summary(docs: list, character: str = "Hal Incandenza"):
    # pass results to OpenAI & ask it to summarize
    system_prompt = f"You are a helpful AI assistant that takes chunks of text about a character \
        and produces a summary of that character's physical appearance. You should extract and \
        summarize physical descriptors only, ignore non-physical details about the character. \
        ```{docs}```"
    messages = [
        {"role": "system", "content": f"{system_prompt}"},
        {
            "role": "user",
            "content": f"Please provide me a detailed physical description of the character {character}",
        },
    ]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.1,
    )

    return response.choices[0].message.content


def generate_image(description: str):
    response = openai.Image.create(
        prompt=description, n=1, size="512x512"
    )
    image_url = response["data"][0]["url"]
    return image_url


def main():
    book_name = "infinite-jest"
    print("Loading chunks and pages")
    ij_chunks, ij_pages = load_or_open_chunks_and_pages(book_name)
    # print("Loading embeddings")
    # embeddings = load_or_generate_embeddings(ij_chunks, book_name)
    print("Creating chromadb")
    chroma_client, collection = initialize_vector_db(ij_pages)
    character = sys.argv[1]

    print("Querying chromadb")
    results = collection.query(
        query_texts=[f"a physical description of {character}"], n_results=15)
    result_docs = results["documents"][0]
    token_limited_results = limit_docs_by_tokens(result_docs)
    # print(token_limited_results)

    print("Generating summary")
    description = get_character_description_summary(
        token_limited_results, character)

    print(description)

    print("Generating image")
    image_url = generate_image(description)
    print(image_url)
    print("Done!")


if __name__ == "__main__":
    main()


# GRAVEYARD
# print(results["documents"][0][0])
# print(len(results["documents"][0]))

# Parse through the returned results and extract physical descriptions
# summarized_results = []
# for res in results["documents"][0]:
#     system_prompt = f"You are a helpful AI assistant that extracts physical descriptions of a character \
#         from a set of passages from a novel. Your only job is to return a list of physical descriptions \
#         of the character's appearance. If there are no physical descriptions of the specified character \
#         in the provided text, or it is ambiguous which character the descriptions apply to, simply return the string 'None' \
#         ```{res}```"
#     messages = [
#         {"role": "system", "content": f"{system_prompt}"},
#         {"role": "user", "content": f"Please extract physical descriptions of the character {character}"}
#     ]
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=messages,
#         temperature=0.1,
#     )
#     if response.choices[0].message.content != 'None':
#         summarized_results.append(response.choices[0].message.content)

def load_or_generate_embeddings(
    infiniteJestChunks: list, book_name: str = "infinite-jest"
):
    # todo(arb) this currently does not work, using default embeddings for now
    embeddings_file_name = f"{book_name}-embeddings.txt"

    if os.path.isfile(embeddings_file_name):
        with open(embeddings_file_name, "rb") as ije:
            embeddings = pickle.load(ije)
    else:
        print(" Embeddings not found, generating now")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(infiniteJestChunks)
        with open(embeddings_file_name, "wb") as ije:
            pickle.dump(embeddings, ije)
    return embeddings
