# Text Summarizer Implementation Explanation

## Overview

This document explains the implementation details of the Text Summarizer application. The summarizer uses the TextRank algorithm, a graph-based extractive summarization technique inspired by Google's PageRank algorithm.

## Libraries and Dependencies

### NLTK (Natural Language Toolkit)

- **Purpose**: Provides tools for natural language processing.
- **Usage in our project**: Although included, the code uses a custom sentence tokenizer instead of NLTK's built-in one to avoid extra dependencies.

### scikit-learn

- **Purpose**: Machine learning library for Python.
- **Usage in our project**:
    - `TfidfVectorizer`: Converts text into a numerical representation using TF-IDF (Term Frequency-Inverse Document Frequency).
    - `cosine_similarity`: Calculates similarity between sentence vectors.

### NetworkX

- **Purpose**: Library for creating, manipulating, and studying complex networks/graphs.
- **Usage in our project**: Implements the PageRank algorithm to rank sentences based on their importance in the graph.

### Tkinter

- **Purpose**: Standard GUI library for Python.
- **Usage in our project**: Creates the user interface with text input/output areas, control buttons, and styling options.

## Algorithm: TextRank for Extractive Text Summarization

### Background

TextRank is an unsupervised graph-based ranking algorithm derived from Google's PageRank. It creates a graph where sentences are nodes and the edges represent similarity between sentences. More similar sentences have stronger connections.

### Implementation Steps

1. **Sentence Tokenization** (`simple_sent_tokenize` function)
     - The text is split into individual sentences using regular expression patterns.
     - This avoids dependency on NLTK's sentence tokenizer which requires downloading additional data.

2. **TF-IDF Vectorization**
     - Each sentence is converted into a numerical vector using TF-IDF.
     - TF-IDF weighs terms based on their frequency in a sentence and rarity across all sentences.
     - **Mathematical representation**: TF-IDF(t, s, S) = TF(t, s) × IDF(t, S)
         - Where t is a term, s is a sentence, and S is the collection of all sentences.
         - TF(t, s) = frequency of term t in sentence s.
         - IDF(t, S) = log(N/n_t), where N is the total number of sentences and n_t is the number of sentences containing term t.

3. **Similarity Matrix Construction**
     - Cosine similarity is calculated between each pair of sentences.
     - **Mathematical representation**: Similarity(A, B) = (A·B)/(||A||×||B||)
     - Creates a dense graph where each sentence is connected to every other sentence with weighted edges.

4. **Graph Construction and PageRank Application**
     - A graph is built using the similarity matrix, with sentences as nodes.
     - NetworkX library applies the PageRank algorithm to this graph.
     - The algorithm iteratively updates importance scores of nodes based on the importance of their neighbors.
     - **PageRank formula**: PR(Vi) = (1-d) + d × ∑(PR(Vj)/OutDegree(Vj))
         - Where Vi are the vertices, d is a damping factor (typically 0.85).
         - The importance of a sentence is determined by the importance of sentences similar to it.

5. **Sentence Selection**
     - Sentences are ranked according to their PageRank scores.
     - Top N sentences are selected based on user preference (default: 3).
     - Selected sentences are reordered to match their original sequence in the text to preserve coherence.

## Technical Implementation Details

### Main Text Summarization Process (`main.py`)

The core algorithm is implemented in `main.py` which:

1. Takes input text (from file or direct input).
2. Tokenizes the text into sentences.
3. Converts sentences into TF-IDF vectors.
4. Builds a graph representation with similarity weights.
5. Applies PageRank to determine sentence importance.
6. Extracts and orders the top N sentences.
7. Returns the summary and saves it to output.txt.

### GUI Implementation (`gui.py`)

The graphical user interface provides:

1. Text input area for pasting or loading text.
2. Controls for adjusting summary parameters (number of sentences).
3. Theme options (light/dark) and font size adjustment.
4. Word count statistics and compression ratio calculation.
5. File operations (load/save functionality).

## Time and Space Complexity

- **Time Complexity**: O(n²) where n is the number of sentences.
    - The bottleneck is computing the similarity matrix between all pairs of sentences.
    - PageRank algorithm typically converges in a small number of iterations.
- **Space Complexity**: O(n²)
    - Storing the similarity matrix requires quadratic space.
    - For very large documents, this could become memory-intensive.

## Advantages of TextRank for Summarization

1. **Unsupervised Learning**: No training data required.
2. **Language Independence**: Works across different languages with minimal adaptation.
3. **Context Awareness**: Captures relationships between sentences through the graph structure.
4. **Extractive Nature**: Preserves original wording, ensuring factual accuracy.

## Limitations

1. **Extractive Only**: Cannot paraphrase or generate new content (unlike abstractive summarization).
2. **Length Sensitivity**: Performance may vary based on document length.
3. **Domain Dependence**: May perform differently across different types of texts.
4. **No Semantic Understanding**: Relies on lexical similarity rather than deeper meaning.

## Potential Improvements

1. **Sentence Embedding**: Replace TF-IDF with modern sentence embeddings (Word2Vec, BERT).
2. **Abstractive Summarization**: Incorporate neural network models for paraphrasing capability.
3. **Keyword Extraction**: Add functionality to highlight key terms in the summary.
4. **Multi-document Summarization**: Extend to summarize multiple related documents.

---

## Detailed Explanation of the TextRank Algorithm

TextRank is a graph-based ranking algorithm for extractive text summarization, inspired by Google's PageRank. Here’s how it works in the context of this project:

### 1. Sentence Tokenization

- The input text is split into individual sentences using a custom regular expression-based function (`simple_sent_tokenize`).
- This avoids external dependencies and ensures compatibility.

### 2. TF-IDF Vectorization

- Each sentence is converted into a numerical vector using TF-IDF (Term Frequency-Inverse Document Frequency).
- TF-IDF highlights words that are important in a sentence but not common across all sentences.
- **Formula:**
    - TF-IDF(t, s, S) = TF(t, s) × IDF(t, S)
    - Where t = term, s = sentence, S = all sentences.

### 3. Similarity Matrix Construction

- Cosine similarity is computed between every pair of sentence vectors.
- This results in a matrix where each value represents how similar two sentences are.
- **Formula:**
    - Similarity(A, B) = (A·B) / (||A|| × ||B||)

### 4. Graph Construction

- Sentences are nodes in a graph.
- Edges are weighted by the similarity scores between sentences.

### 5. PageRank Application

- The PageRank algorithm is applied to the graph using NetworkX.
- Sentences that are similar to many other important sentences receive higher scores.
- **Formula:**
    - PR(Vi) = (1-d) + d × ∑(PR(Vj)/OutDegree(Vj))
    - Where d is the damping factor (typically 0.85).

### 6. Sentence Selection and Ordering

- Sentences are ranked by their PageRank scores.
- The top N sentences are selected for the summary.
- Selected sentences are reordered to match their original order in the text for coherence.

### Key Points

- **Unsupervised:** No training data required.
- **Extractive:** Only original sentences are used, ensuring factual accuracy.
- **Efficient:** Works well for a variety of text types and lengths, though performance may vary for very large documents.

---

## Code Component Explanations

### What does the cosine similarity function do in the code?

The cosine similarity function calculates the cosine of the angle between two vectors in a multi-dimensional space. In the context of text summarization, it is used to measure the similarity between two sentence vectors. The closer the cosine value is to 1, the more similar the sentences are. This is crucial for building the similarity matrix that forms the basis of the TextRank algorithm.

### What does the TF-IDF vectorizer do in the code?

The TF-IDF vectorizer converts a collection of text documents into a matrix of TF-IDF features. It transforms each sentence into a numerical vector based on the frequency of terms in the sentence relative to their frequency across all sentences. This representation is essential for calculating the similarity between sentences, which is a key step in the TextRank algorithm.

### What does the simple_sent_tokenize function do in the code?

The `simple_sent_tokenize` function is a custom implementation for splitting text into sentences. It uses regular expressions to identify sentence boundaries, such as periods, exclamation marks, and question marks. This function avoids external dependencies (like NLTK's sentence tokenizer) and ensures that the text is tokenized correctly for further processing in the summarization algorithm.

### What does the NetworkX library do in the code?

The NetworkX library is used for creating, manipulating, and analyzing complex networks or graphs. In the context of this project, it is employed to build a graph representation of sentences where nodes represent sentences and edges represent the similarity between them. The PageRank algorithm from NetworkX is then applied to rank the sentences based on their importance in the graph, which is a crucial step in the TextRank summarization process.

### What do NLTK, scikit-learn, and NetworkX libraries do in the code?

- **NLTK**: Although included, the code uses a custom sentence tokenizer instead of NLTK's built-in one to avoid extra dependencies. NLTK is generally used for natural language processing tasks like tokenization, stemming, and tagging.
- **scikit-learn**: Provides the `TfidfVectorizer` for converting sentences into TF-IDF vectors and `cosine_similarity` for measuring similarity between these vectors. These are essential for building the similarity matrix in the TextRank algorithm.
- **NetworkX**: Used to construct a graph where sentences are nodes and similarities are edge weights. NetworkX's PageRank implementation ranks sentences by importance, enabling extraction of the most relevant sentences for the summary.


