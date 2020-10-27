import psycopg2
import json
from datetime import datetime
from newspaper import Article, ArticleException
import feedparser as fp

#conn = psycopg2.connect(
#    host="localhost",
#    database="HotOrNot",
#    user="postgres",
#    password=""
#)

sources = {}
with open('sources.json') as json_file:
    sources = json.load(json_file)

titles = []
with open('data.txt') as file:
    for line in file:
        j = json.loads(line)
        for title in j.keys():
            titles.append(title)


# Gets list of current articles for specified source
def get_articles(articles_source):
    rss = articles_source['rss']
    d = fp.parse(rss)
    articles = []
    for entry in d['entries']:
        try:
            content = Article(entry.link)
            content.download()
            content.parse()
            articles.append([entry.title, content.text])
        except ArticleException:
            print("Something went wrong when downloading article")

    return articles


# Checks if article is already in the database
#def check(article_title):
#    cur = conn.cursor()
#    cur.execute('''SELECT * FROM articles WHERE articles.id = %s ''', (article_title,))
#    ver = cur.fetchone()
#    if ver is None:
#        return True
#    else:
#        return False
#
#
# Creates new entry for article in the database, not being uses during this version
# def upload(article_title,article_data):
#    cur = conn.cursor()
#    date = time = datetime.now()
#    cur.execute('''INSERT INTO articles(id,data,date,time) VALUES(%s,%s,%s,%s)''', (article_title, json.dumps(article_data), date, time))
#    conn.commit()


# Checks if article has already been downloaded
def check(article_title):
    if article_title in titles:
        return False
    else:
        return True


# Outputs json to text file
def output(article_title, article_data, article_source):
    j = {article_title: [article_data, article_source, datetime.now().strftime("%m/%d/%Y, %H:%M:%S")]}
    with open("data.txt", "a") as file:
        file.write(json.dumps(j) + '\n')


if __name__ == '__main__':
    while True:
        for source in sources:
            print("Fetching from " + source)
            data = get_articles(sources[source])
            count = 0
            for article in data:
                title = article[0]
                if check(title):
                    count += 1
                    output(title, article, source)
            print("new articles found: " + str(count))
        print("Round Complete")
