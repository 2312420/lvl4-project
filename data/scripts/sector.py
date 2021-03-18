import yfinance as yf
import psycopg2

conn = psycopg2.connect("dbname='localdb' user='postgres' host='localhost' password='2206'")

cur = conn.cursor()

cur.execute("SELECT * FROM company")
comps = cur.fetchall()

for company in comps:
    print(company[0])
    try:
        stock_data = yf.Ticker(company[0])

        info = stock_data.info

        ind = info['industry']

        cur.execute("SELECT * FROM tags WHERE tag_title = %s", [ind])

        tags = cur.fetchall()

        if tags == []:
            cur.execute("INSERT INTO tags(tag_title) VALUES (%s)", [ind])
            conn.commit()

            cur.execute("SELECT * FROM tags WHERE tag_title = %s", [ind])
            tags = cur.fetchall()

        tag_id = tags[0][0]

        print(tag_id)
        cur.execute("INSERT INTO company_tags(company_code, tag_id) VALUES (%s, %s)", [company[0], tag_id])
        conn.commit()
        #cur.execute("UPDATE company SET industry = %s, sector = %s WHERE stock_code = %s ", [ind, sector,company[0]])
        #conn.commit()
    except:
        print("something went wrong")
