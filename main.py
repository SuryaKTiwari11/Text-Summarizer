import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

def simple_sent_tokenize(text):
    sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?|\!)\s', text)
    return [sentence.strip() for sentence in sentences if sentence.strip()]

def summarize_textrank(text, num_sentences=3):
    sentences = simple_sent_tokenize(text)
    if len(sentences) <= num_sentences:
        return text

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(sentences)

    sim_matrix = cosine_similarity(tfidf_matrix)

    nx_graph = nx.from_numpy_array(sim_matrix)
    scores = nx.pagerank(nx_graph)

    ranked_sentences = sorted(((scores[i], s) for i, s in enumerate(sentences)), reverse=True)

    top_sentences = sorted([s for _, s in ranked_sentences[:num_sentences]], key=lambda s: sentences.index(s))
    summary = ' '.join(top_sentences)
    return summary

try:
    with open("input.txt", "r", encoding="utf-8") as infile:
        text = infile.read()
except:
    text = """
    Natural Language Processing (NLP) is a field of Artificial Intelligence that focuses on the interaction between humans and computers using natural language.
    The ultimate objective of NLP is to read, decipher, understand, and make sense of human language in a valuable way.
    Most NLP techniques rely on machine learning to extract meaning from human language.
    Applications of NLP are everywhere — in spam detection, sentiment analysis, language translation, chatbots, and more.
    Recent advancements in deep learning have significantly improved NLP capabilities.
    """

summary = summarize_textrank(text, num_sentences=2)
print("Summary:\n", summary)

with open("output.txt", "w", encoding="utf-8") as outfile:
    outfile.write(summary)