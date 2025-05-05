import os
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

# Manual sentence tokenization function to avoid punkt_tab dependency
def simple_sent_tokenize(text):
    # Split text by common sentence delimiters
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
    # Remove empty strings and whitespace
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def summarize_textrank(text, num_sentences=3):
    # Step 1: Sentence tokenization using our manual function
    sentences = simple_sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text

    # Step 2: TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Step 3: Build similarity matrix
    sim_matrix = cosine_similarity(tfidf_matrix)

    # Step 4: Build graph and apply TextRank (PageRank)
    nx_graph = nx.from_numpy_array(sim_matrix)
    scores = nx.pagerank(nx_graph)

    # Step 5: Rank sentences
    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    # Step 6: Select top-N and retain original order
    top_sentences = sorted([s for _, s in ranked_sentences[:num_sentences]], key=lambda s: sentences.index(s))
    summary = ' '.join(top_sentences)
    return summary

# Read input from input.txt
try:
    with open("input.txt", "r", encoding="utf-8") as infile:
        text = infile.read()
except:
    # Example usage if input.txt is not available
    text = """
    Natural Language Processing (NLP) is a field of Artificial Intelligence that focuses on the interaction between humans and computers using natural language.
    The ultimate objective of NLP is to read, decipher, understand, and make sense of human language in a valuable way.
    Most NLP techniques rely on machine learning to extract meaning from human language.
    Applications of NLP are everywhere — in spam detection, sentiment analysis, language translation, chatbots, and more.
    Recent advancements in deep learning have significantly improved NLP capabilities.
    """

summary = summarize_textrank(text, num_sentences=2)
print("Summary:\n", summary)

# Write summary to output.txt
with open("output.txt", "w", encoding="utf-8") as outfile:
    outfile.write(summary)