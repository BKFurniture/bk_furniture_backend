import numpy as np
import openai
import pandas as pd
import json
import tiktoken
import os
from django.conf import settings
from django.apps import AppConfig


COMPLETIONS_MODEL = "text-davinci-003"
EMBEDDING_MODEL = "text-embedding-ada-002"

openai.api_key = settings.OPENAI_API_KEY

MAX_SECTION_LEN = 300
SEPARATOR = "\n* "
ENCODING = "gpt2"  # encoding for text-davinci-003

encoding = tiktoken.get_encoding(ENCODING)
separator_len = len(encoding.encode(SEPARATOR))

COMPLETIONS_API_PARAMS = {
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
    return np.dot(np.array(x), np.array(y))


def order_document_sections_by_query_similarity(query: str, contexts: dict[(str, str), np.array]) -> list[(float, (str, str))]:
    query_embedding = get_embedding(query)

    document_similarities = sorted(
        [
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
    chosen_sections_points = []

    for _, section_index in most_relevant_document_sections:
        section_index = int(section_index)
        document_section = df.loc[section_index]

        chosen_sections_len += document_section.tokens + separator_len
        if chosen_sections_len > MAX_SECTION_LEN:
            break

        chosen_sections.append(SEPARATOR + document_section.Content.replace("\n", " "))
        chosen_sections_indexes.append(str(section_index))
        chosen_sections_points.append(_)
    header = """
    We are BK Furniture store, we sells the best quality furnitures. We are here to help customer with your furniture needs.
    You are aswering the questions as you are Vy, our customer service representative bot.
    Answer the question as truthfully as possible using the provided context.
    If the answer is not contained within the text below, say "I don't know".
    If the question is not mentioning about our furniture or information about our store, say "I don't know".
    If the question is not clear, say "Sorry, I don't understand" or ask if you could help them.
    \n\nContext:\n"""

    return header + "".join(chosen_sections) + "\n\n Q: " + question + "\n A:"


def answer_query_with_context(
    query: str,
    df: pd.DataFrame,
    document_embeddings: dict[(str, str), np.array],
) -> str:
    prompt = construct_prompt(
        query,
        document_embeddings,
        df
    )

    response = openai.Completion.create(
                prompt=prompt,
                **COMPLETIONS_API_PARAMS
            )

    return response["choices"][0]["text"].strip(" \n")


class ChatBot:

    def __init__(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))

        self.df = pd.read_csv(os.path.join(dir_path, 'data_folder', 'BKF_Questions.csv'))
        self.df['tokens'] = self.df.apply(
            lambda row: len(row.Content.split()),
            axis=1
        )
        self.document_embeddings = json.load(open(os.path.join(dir_path, 'data_folder', 'doc_emb.json')))

    def answer_question(self, question: str):
        return answer_query_with_context(
            question,
            self.df,
            self.document_embeddings
        )


class WebappConfig(AppConfig):
    name = 'davinci3'
    chatbot = ChatBot()
