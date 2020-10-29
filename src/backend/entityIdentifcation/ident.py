import psycopg2
import spacy

conn = psycopg2.connect(
    host="localhost",
    database="HotOrNot",
    user="postgres",
    password="2206"
)


nlp = spacy.load('en_core_web_sm')


#Json = {"Facebook public policy director for India, South and Central Asia Ankhi Das steps down": [["Facebook public policy director for India, South and Central Asia Ankhi Das steps down", "Ankhi Das, a senior Facebook executive in India, is leaving the social media company on Tuesday, two months after media reports claimed she allegedly interfered in the company\u2019s content moderation policy and showed favoritism to Bharatiya Janata Party (BJP).Das served as the Public Policy Director for Facebook India, South and Central Asia. A Wall Street Journal story had alleged favouritism by Facebook towards India\u2019s ruling party BJP on hate speech posts. It stated that Das opposed applying hate speech rules to posts by BJP leader T Raja Singh and three other BJP leaders and groups flagged internally for promoting violence. The story had sparked a political row in India.A Facebook official told ET on condition of anonymity that Das departure does not have anything to do with the recent press reports.\u201cAnkhi has decided to step down from her role in Facebook to pursue her interest in public service,\u201d said Ajit Mohan, VP & Managing Director, Facebook India. \u201cShe has been a part of my leadership team over the last 2 years, a role in which she has made enormous contributions. We are grateful for her service and wish her the very best for the future.\u201dDas joined Facebook in 2011 and was one of their earliest employees in India."], "Economic_Times", "10/27/2020, 16:30:48"]}

#sentence = Json['Facebook public policy director for India, South and Central Asia Ankhi Das steps down'][0][0]

def analyse(sent):
    doc = nlp(sent)
    orgs = []
    for ent in doc.ents:
        if ent.label_ == 'ORG':
            orgs.append(ent.text)
    return orgs


def get_articles():
    cur = conn.cursor()
    cur.execute('''SELECT * FROM articles WHERE articles.entities IS NULL''')
    articles = cur.fetchmany(10)
    return articles


def upload(article_id, article_entites):
    cur = conn.cursor()
    if article_entites == '[]':
        cur.execute('''UPDATE articles SET entities = %s WHERE articles.id = %s ''', ("NONE", article_id))
    else:
        cur.execute('''UPDATE articles SET entities = %s WHERE articles.id = %s ''', (article_entites, article_id))
    conn.commit()


if __name__ == '__main__':
    while(True):
        for article in get_articles():
            id = article[0]
            entities = analyse(article[1][1])
            upload(id, str(entities))
        print("Round Complete")

