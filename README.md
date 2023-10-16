# infinite-jest-generator 🎭

Generate AI-driven images of characters from David Foster Wallace's magnum opus, "Infinite Jest".

![Sample Image](link_to_a_sample_image_here.png)

## Description

infinite-jest-generator leverages the power of AI to bring to life the characters from the classic novel "Infinite Jest".

Technically it could work for any novel you have a PDF of, but I made this for a specific bookclub.

## Features

- Generate detailed images of main characters like Hal Incandenza, Don Gately, and Joelle Van Dyne.

## Implementation Details

### Retrieval

Iterating through various vectordb solutions, so far:

- chromadb, super great setup, working on stability with self-hosted in GCP
- weaviate, managed is nice but default ada embeddings perform far worse than sentance transformer, working on updating that

### Generation

GPT-4

### Image Gen

- Dalle-2 built in openai api, kinda murdery
- Stability API to stable diffusion, base model & no tuning so also kinda murdery

## Installation & Setup

1. Clone the repository:

```
git clone https://github.com/your_username/infinite-jest-generator.git
```

2. Navigate to the project directory:

```
cd infinite-jest-generator
```

3. Create the `data` directory and save the pdf you want to query there

```
mkdir data
cp <source directory>/bookname.pdv ./data
```

4. Create a `.env` file with your openAI credentials

```
OPENAI_ORG=<org id>
OPENAI_API_KEY=<api key>
```

5. Install the required dependencies:

```
pip install -r requirements.txt
```

6. Run the application:

```
python app.py
```

7. Navigate to `localhost:8000/graphql` to access the graphql playground (frontend incoming)

## Usage

1. Launch the application.
2. Enter in a character name
3. Click "Generate" and marvel at the AI-generated artwork!

## Demo

For a live demo, visit [this link](https://ij-frontend-ka2xis5sma-uc.a.run.app/).

## License

This project is licensed under the MIT License.

## Disclaimer

This project is a work of art and for demonstration purposes only. It is in no way affiliated with or endorsed by the estate of David Foster Wallace or the publishers of "Infinite Jest".
