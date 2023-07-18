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
from transformers import PegasusTokenizer, TFPegasusForConditionalGeneration, pipeline

from articlefinder import ArticleFinder


class ArticleSummarizer:
    def __init__(self, article_url):
        self.nlp = English()
        self.nlp.add_pipe('sentencizer')
        self.parser = English()
        article = Article(article_url)
        article.download()
        article.parse()

        model_name = "google/pegasus-xsum"

        self.pegasus_tokenizer = PegasusTokenizer.from_pretrained(model_name)

        self.pegasus_model = TFPegasusForConditionalGeneration.from_pretrained(model_name)

        self.article_text = article.text

    def pegasus_summary(self):
        tokens = self.pegasus_tokenizer(self.article_text, truncation=True, padding="longest", return_tensors="pt")

        encoded_summary = self.pegasus_model(**tokens)
        decoded_summary = self.pegasus_tokenizer.decode(encoded_summary[0], skip_special_tokens=True)
        return decoded_summary
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

        summary_string = ""
        for i in summary:
            summary_string += ' '.join(i.text.split()) + "\n"

        return summary_string

#
if __name__ == '__main__':
    articles = ArticleFinder("tips").get_random_article()
    articleSum = ArticleSummarizer(articles['url'])
    articleSum_text = articleSum.generate_summary(14)

    print(f"{articleSum_text.__name__}:\n{articleSum_text}")
    print(f"{articleSum.pegasus_summary().__name__}:\n{articleSum.pegasus_summary()}")



