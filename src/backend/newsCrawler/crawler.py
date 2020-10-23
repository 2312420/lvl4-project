import psycopg2
import json
from datetime import datetime
from newspaper import Article
import feedparser as fp

conn = psycopg2.connect(
    host="localhost",
    database="HotOrNot",
    user="postgres",
    password="2206"
)

sources = {
    "WSJ_Markets": {
        "rss": "https://feeds.a.dj.com/rss/RSSMarketsMain.xml"
    },
    "WSJ_Technology":{
        "rss": "https://feeds.a.dj.com/rss/RSSWSJD.xml"
    },
    "WSJ_US_business":{
        "rss": "https://feeds.a.dj.com/rss/WSJcomUSBusiness.xml"
    },
    "TIME_business":{
        "rss": "http://feeds.feedburner.com/time/business"
    },
    "BBC_business":{
        "rss": "https://feeds.bbci.co.uk/news/business/rss.xml"
    },
    "CNBC":{
        "rss": "https://www.cnbc.com/id/19746125/device/rss/rss.xml"
    },
    "FinancialTimes":{
        "rss": "https://www.ft.com/?format=rss"
    },
    "FortuneRssFeed":{
        "rss": "http://fortune.com/feed"
    },
    "Economic_Times":{
        "rss": "https://economictimes.indiatimes.com/rssfeedsdefault.cms"
    }
}


# Gets list of current articles for specified source
def get_articles(articles_source):
    rss = articles_source['rss']
    d = fp.parse(rss)
    articles = []
    for entry in d['entries']:
        content = Article(entry.link)
        content.download()
        content.parse()
        articles.append([entry.title , content.text])

    return articles


# Checks if article is already in the database
def check(article_title):
    cur = conn.cursor()
    cur.execute('''SELECT * FROM articles WHERE articles.id = %s ''', (article_title,))
    ver = cur.fetchone()
    if ver is None:
        return True
    else:
        return False


# Creates new entry for article in the database
def upload(article_title,article_data):
    cur = conn.cursor()
    date = time = datetime.now()
    cur.execute('''INSERT INTO articles(id,data,date,time) VALUES(%s,%s,%s,%s)''', (article_title, json.dumps(article_data), date, time))
    conn.commit()


if __name__ == '__main__':
    while True:
        for source in sources:
            print("Fetching from " + source)
            timenow = datetime.now()
            data = get_articles(sources[source])
            print((datetime.now() - timenow))
            for article in data:
                title = article[0]
                if check(title):
                    print("Uploading to database...")
                    upload(title, article)
        print("Round Complete")