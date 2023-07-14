import sys
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
import string
from spacy.lang.en import English
from newspaper import Article

from heapq import nlargest
punctuations = string.punctuation
from spacy.language import Language
nlp = English()
nlp.add_pipe('sentencizer')
parser = English()

def pre_process(document):
    clean_tokens = [ token.lemma_.lower().strip() for token in document]
    clean_tokens = [ token for token in clean_tokens if token not in STOP_WORDS and token not in punctuations]
    tokens = [token.text for token in document]
    lower_case_tokens = list(map(str.lower, tokens))
    
    return lower_case_tokens

def generate_numbers_vectors(tokens):
    frequency = [tokens.count(token) for token in tokens]
    token_dict = dict(list(zip(tokens, frequency)))
    maximum_freq = sorted(token_dict.values())[-1]
    normalised_dict = {token_key: token_dict[token_key]/maximum_freq for token_key in token_dict.keys()}
    return normalised_dict


def sentences_importance(text, normalised_dict):
    importance = {}
    for sentence in nlp(text).sents:
        for token in sentence:
            target_token = token.text.lower()
            if target_token in normalised_dict.keys():
                if sentence in importance.keys():
                    importance[sentence] = normalised_dict[target_token]
                else:
                    importance[sentence] = normalised_dict[target_token]
    return importance

def generate_summary(rank, text):
    target_document = parser(text)
    importance = sentences_importance(text, generate_numbers_vectors(pre_process(target_document)))
    summary = nlargest(rank, importance, key=importance.get)
    return summary



url =  "https://www.investopedia.com/articles/younginvestors/08/eight-tips.asp"
article = Article(url) 
article.download()
article.parse()

article_text =  article.text
num_sentences_to_generate = 3
summary_text = generate_summary(num_sentences_to_generate,article_text )

for i in summary_text:
    print(i)