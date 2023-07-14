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

from articlefinder import ArticleFinder


class ArticleSummarizer:
    def __init__(self, article_url):
        self.nlp = English()
        self.nlp.add_pipe('sentencizer')
        self.parser = English()
        self.article = Article(article_url)
        self.article.download()
        self.article.parse()
        self.article_text = self.article.text
    def pre_process(self, document):
        clean_tokens = [ token.lemma_.lower().strip() for token in document]
        clean_tokens = [ token for token in clean_tokens if token not in STOP_WORDS and token not in punctuations]
        tokens = [token.text for token in document]
        lower_case_tokens = list(map(str.lower, tokens))

        return lower_case_tokens

    def generate_numbers_vectors(self, tokens):
        frequency = [tokens.count(token) for token in tokens]
        token_dict = dict(list(zip(tokens, frequency)))
        maximum_freq = sorted(token_dict.values())[-1]
        normalised_dict = {token_key: token_dict[token_key]/maximum_freq for token_key in token_dict.keys()}
        return normalised_dict


    def sentences_importance(self, text, normalised_dict):
        importance = {}
        for sentence in self.nlp(text).sents:
            for token in sentence:
                target_token = token.text.lower()
                if target_token in normalised_dict.keys():
                    if sentence in importance.keys():
                        importance[sentence] = normalised_dict[target_token]
                    else:
                        importance[sentence] = normalised_dict[target_token]
        return importance

    def generate_summary(self, rank):
        target_document = self.parser(self.article_text)
        importance = self.sentences_importance(self.article_text, self.generate_numbers_vectors(self.pre_process(target_document)))
        summary = nlargest(rank, importance, key=importance.get)
        return summary


# if __name__ == '__main__':
#     articles = ArticleFinder("tips").get_random_article()
#     articleSum = ArticleSummarizer(articles['url'])
#     articleSum_text = articleSum.generate_summary(20)
#     print(articleSum_text)


