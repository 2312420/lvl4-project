import psycopg2

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


if __name__ == '__main__':
    articles = get_articles()
    print(articles)