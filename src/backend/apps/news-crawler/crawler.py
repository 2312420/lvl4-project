import json
from datetime import datetime
from newspaper import Article, ArticleException
import feedparser as fp
import requests

base_url = "http://backend-api:5000/"
titles = []


# Gets list of sources from DB
def get_source():
    url = base_url + '/sources'
    r = requests.get(url)
    return r.json()


# Gets list of current articles for specified source
def get_articles(rss):
    d = fp.parse(rss)
    articles = []
    error = False
    for entry in d['entries']:
        try:
            content = Article(entry.link)
            content.download()
            content.parse()
            articles.append([entry.title, content.text])
        except Exception as e:
            error = True
    if error:
        print("Something went wrong when downloading articles")
    return articles


# Checks if article has already been downloaded by the crawler
def check(article_title):
    if article_title in titles:
        return False
    else:
        return True


# Posts given article to db via api
def output(article_data, article_source_id):
    url = base_url + "/article"
    payload = {"title": article_data[0], "transcript": article_data[1], "source_id": article_source_id}
    r = requests.post(url, json=payload)


if __name__ == '__main__':
    sources = get_source()
    while True:
        for source in sources:
            print("Fetching from " + source['short_hand'])
            data = get_articles(source['rss'])
            count = 0
            for article in data:
                title = article[0]
                if check(title):
                    count += 1
                    output(article, source['id'])
            print("new articles found: " + str(count))
        print("Round Complete")
