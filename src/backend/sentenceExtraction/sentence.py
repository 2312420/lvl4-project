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
    cur.execute('''SELECT * FROM articles''')
    articles = cur.fetchmany(10)
    return articles


def extract_sentences(article):
    title = article[1][0]
    text = article[1][1]
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    sentences = tokenizer.tokenize(text)
    return sentences


if __name__ == '__main__':
    nltk.download('punkt')
    articles = get_articles()
    print(extract_sentences(articles[0]))