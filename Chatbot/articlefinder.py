import requests
import random
from bs4 import BeautifulSoup


class ArticleFinder:
    def __init__(self, topic):
        self.topic = topic
        self.articles = self.search_articles()

    # Currently only checks https://www.nerdwallet.com
    # Possibility to add more websites in the future (time-dependent)
    def search_articles(self):
        search_query_url =f"https://www.nerdwallet.com/search/results?q={self.topic}"
        response = requests.get(search_query_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        search_results = soup.find_all('li', {'class': 'search-results-article-container'})
        articles = []

        for result in search_results:
            a_tag = result.find('a')
            title = a_tag.string
            url = a_tag['href']
            articles.append({'title':title, 'url':url})

        return articles

    def get_articles(self):
        return self.articles

    def get_random_article(self):
        random_index = random.randint(0, len(self.articles) - 1)
        return self.articles[random_index]


# if __name__ == '__main__':
#     af = ArticleFinder("tips")
#     af_articles = af.get_articles()
#     for i in af_articles:
#         print(i)
