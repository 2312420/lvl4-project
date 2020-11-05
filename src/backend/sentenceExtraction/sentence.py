import re
import psycopg2
import nltk.data

conn = psycopg2.connect(
    host="localhost",
    database="HotOrNot",
    user="postgres",
    password="2206"
)


def get_articles():
    cur = conn.cursor()
    cur.execute('''SELECT * FROM articles WHERE analyzed = false ''')
    articles = cur.fetchmany(10)
    return articles


def extract_sentences(article):
    title = article[1][0]
    text = article[1][1]
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(text)
    return sentences


def update_article(article_id):
    cur = conn.cursor()
    cur.execute('''UPDATE articles SET analyzed = %s WHERE articles.id = %s''', ("true", article_id))
    conn.commit()


def upload_sentence(article_id, article_sentence):
    cur = conn.cursor()
    cur.execute('''INSERT INTO sent (text, article_id) VALUES (%s, %s) ''', (article_sentence, article_id))
    conn.commit()


if __name__ == '__main__':
    nltk.download('punkt')
    articles = get_articles()
    for article in articles:
        id = article[0]
        for sentence in extract_sentences(article):
            upload_sentence(id, sentence)
            update_article(id)

