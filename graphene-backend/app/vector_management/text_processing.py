import os
import pickle
import re
import logging
from enum import Enum

import nltk
from sentence_transformers import SentenceTransformer
import tiktoken
import PyPDF2 as pdf


class ChunkType(Enum):
    PAGE = "Page"
    CHUNK20 = "Chunk20"
    CHUNK10 = "Chunk10"


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


def load_or_open_chunks_and_pages(book_name: str = "infinite-jest", root_dir: str = "../../data/") -> tuple[list, list, list]:
    # Open and load the PDF
    # Check if the txt file exists
    logging.info("Checking for text files")
    pdf_name = f"{root_dir}{book_name}.pdf"
    # txt_name = f"{root_dir}{book_name}.txt"
    chunk_20_name = f"{root_dir}{book_name}-chunks-20.txt"
    chunk_10_name = f"{root_dir}{book_name}-chunks-10.txt"
    page_name = f"{root_dir}{book_name}-pages.txt"

    if os.path.isfile(page_name) and os.path.isfile(chunk_20_name) and os.path.isfile(chunk_10_name):
        logging.info("  Text found, loading chunks and pages now")
        with open(chunk_20_name, "rb") as ijc20:
            infiniteJestChunks = pickle.load(ijc20)

        with open(chunk_10_name, "rb") as ijc10:
            infiniteJestChunks = pickle.load(ijc10)

        with open(page_name, "rb") as ijp:
            infiniteJestPages = pickle.load(ijp)
    else:
        logging.info(" Text not found, generating now")
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

        infiniteJestChunks20 = split_text_with_overlap(
            infiniteJestString, 20, 3)
        infiniteJestChunks10 = split_text_with_overlap(
            infiniteJestString, 10, 3)

        with open("./infinite-jest-pages.txt", "wb") as ijp:
            pickle.dump(infiniteJestPages, ijp)

        with open("./infinite-jest-chunks-20.txt", "wb") as ijc20:
            pickle.dump(infiniteJestChunks20, ijc20)

        with open("./infinite-jest-chunks-10.txt", "wb") as ijc10:
            pickle.dump(infiniteJestChunks10, ijc10)

        pdfFileObj.close()

    return infiniteJestPages, infiniteJestChunks20, infiniteJestChunks10


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


def load_or_generate_embeddings(
    infiniteJestChunks: list, book_name: str = "infinite-jest", chunk_type: ChunkType = ChunkType.CHUNK20, root_dir: str = "../../data/"
):
    logging.info(f"Checking for {chunk_type.value} embeddings")
    # todo(arb) this currently does not work, using default embeddings for now
    embeddings_file_name = f"{root_dir}{book_name}-{chunk_type.value}-embeddings.txt"

    if os.path.isfile(embeddings_file_name):
        with open(embeddings_file_name, "rb") as ije:
            embeddings = pickle.load(ije)
    else:
        logging.info(" Embeddings not found, generating now")
        model = SentenceTransformer("all-MiniLM-L6-v2")
        embeddings = model.encode(infiniteJestChunks)
        with open(embeddings_file_name, "wb") as ije:
            pickle.dump(embeddings, ije)
    return embeddings
