import os
import pickle
import re

import nltk
import chromadb
import tiktoken
import PyPDF2 as pdf


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
    print("Checking for text files")
    pdf_name = f"{root_dir}{book_name}.pdf"
    # txt_name = f"{root_dir}{book_name}.txt"
    chunk_name = f"{root_dir}{book_name}-chunks.txt"
    page_name = f"{root_dir}{book_name}-pages.txt"

    if os.path.isfile(page_name) and os.path.isfile(chunk_name):
        print("  Text found, loading chunks and pages now")
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
