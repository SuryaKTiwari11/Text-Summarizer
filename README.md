# Text Summarizer

A Python application that summarizes text using the TextRank algorithm.

## Features

- Automatic text summarization based on TextRank algorithm
- Customizable number of sentences in the summary
- User-friendly GUI with light and dark themes
- Word count and compression ratio statistics
- File import/export capabilities

## Requirements

- Python 3.x
- Required packages:
  - nltk
  - sklearn
  - networkx
  - tkinter (usually included with Python)

## Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/Text-Summarizer.git
cd Text-Summarizer

# Install required packages
pip install -r requirements.txt
```

## Usage

Run the application by executing:

```bash
python gui.py
```

1. Enter text in the input area or load it from a file
2. Select the number of sentences for the summary
3. Click "Summarize" to generate a summary
4. Save the result to a file if needed

## How it Works

The summarization engine uses a simplified implementation of the TextRank algorithm:

1. Splits the text into sentences
2. Creates a similarity matrix using TF-IDF representation
3. Builds a graph where sentences are nodes and similarities are edges
4. Applies PageRank algorithm to rank sentences by importance
5. Extracts the top N sentences while maintaining original order

## License

MIT License