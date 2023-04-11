import numpy as np
import openai
import pandas as pd
import json
import tiktoken
from django.conf import settings

COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

openai.api_key = settings.OPENAI_API_KEY

MAX_SECTION_LEN = 200
SEPARATOR = "\n* "
ENCODING = "gpt2"  # encoding for text-davinci-003

encoding = tiktoken.get_encoding(ENCODING)
separator_len = len(encoding.encode(SEPARATOR))

COMPLETIONS_API_PARAMS = {
    # We use temperature of 0.0 because it gives the most predictable, factual answer.
    "temperature": 0.0,
    "max_tokens": 500,
    "model": COMPLETIONS_MODEL,
}


def get_embedding(text: str, model: str = EMBEDDING_MODEL) -> list[float]:
    result = openai.Embedding.create(
      model=model,
      input=text
    )
    return result["data"][0]["embedding"]


def vector_similarity(x: list[float], y: list[float]) -> float:
    """
    Returns the similarity between two vectors.

    Because OpenAI Embeddings are normalized to length 1, the cosine similarity is the same as the dot product.
    """
    return np.dot(np.array(x), np.array(y))


def order_document_sections_by_query_similarity(query: str, contexts: dict[(str, str), np.array]) -> list[(float, (str, str))]:
    """
    Find the query embedding for the supplied query, and compare it against all of the pre-calculated document embeddings
    to find the most relevant sections.

    Return the list of document sections, sorted by relevance in descending order.
    """
    query_embedding = get_embedding(query)

    document_similarities = sorted([
        (vector_similarity(query_embedding, doc_embedding), doc_index) for doc_index, doc_embedding in contexts.items()
    ], reverse=True)

    return document_similarities


def construct_prompt(question: str, context_embeddings: dict, df: pd.DataFrame) -> str:
    """
    Fetch relevant
    """
    most_relevant_document_sections = order_document_sections_by_query_similarity(question, context_embeddings)

    chosen_sections = []
    chosen_sections_len = 0
    chosen_sections_indexes = []

    for _, section_index in most_relevant_document_sections:
        # Add contexts until we run out of space.
        # print(section_index)
        # print(_)
        section_index = int(section_index)
        document_section = df.loc[section_index]

        chosen_sections_len += document_section.tokens + separator_len
        if chosen_sections_len > MAX_SECTION_LEN:
            break

        chosen_sections.append(SEPARATOR + document_section.Content.replace("\n", " "))
        chosen_sections_indexes.append(str(section_index))

    # Useful diagnostic information
    print(f"Selected {len(chosen_sections)} document sections:")
    print("\n".join([
        f'{df.loc[int(idx)].Request}, {df.loc[int(idx)]["Type of request"]}, {df.loc[int(idx)]["Product"]}'
        for idx in chosen_sections_indexes
        ]))

    header = """Answer the question as truthfully as possible using the provided context, use a gently voice as you are an customer caring employee, and if the answer is not contained within the text below, say "I don't know."\n\nContext:\n"""

    return header + "".join(chosen_sections) + "\n\n Q: " + question + "\n A:"


def answer_query_with_context(
    query: str,
    df: pd.DataFrame,
    document_embeddings: dict[(str, str), np.array],
    show_prompt: bool = False
) -> str:
    prompt = construct_prompt(
        query,
        document_embeddings,
        df
    )

    if show_prompt:
        print(prompt)

    response = openai.Completion.create(
                prompt=prompt,
                **COMPLETIONS_API_PARAMS
            )

    return response["choices"][0]["text"].strip(" \n")


class ChatBot:

    def __init__(self):

        self.df = pd.read_csv("chatbot\\data_folder\\BKF_Questions.csv")
        self.df['tokens'] = self.df.apply(
            lambda row: len(row.Content.split()),
            axis=1
        )
        self.document_embeddings = json.load(open("chatbot\\data_folder\\doc_emb.json"))

    def answer_question(self, question: str):
        return answer_query_with_context(
            question,
            self.df,
            self.document_embeddings
        )
# df = pd.read_csv('D:\\CODE\\.py\\Notebooks\\BKF_Questions.csv')
# df['tokens'] = df.apply(lambda row: len(row.Content.split()) ,axis=1)
# document_embeddings = json.load(open("doc_emb.json"))
# print(answer_query_with_context("How is the delivery service of your store", df, document_embeddings))
