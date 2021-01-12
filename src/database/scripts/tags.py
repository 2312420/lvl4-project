import yfinance as yf
import spacy
import requests

nlp = spacy.load('en_core_web_sm')
base_url = "http://127.0.0.1:5000"

# Get list of all companies
def get_companies():
    pass


# Get list of possible tags
def get_possible_tags(stock_code):
    stock = yf.Ticker(stock_code)
    info = stock.info
    possible_tags = []

    # Add company sector to tag list
    possible_tags.append(info['sector'])

    # Get tags from business summary
    doc = nlp(info['longBusinessSummary'])
    for ent in doc.ents:
        if ent.label_ != "ORDINAL" and ent.label_ != "DATE":
            if ent.text not in possible_tags:
                possible_tags.append(ent.text)

    return possible_tags


# Check if tag exists, if not then adds tag and returns id
def get_tag(tag_title):
    url = base_url + "/tag/" + tag_title
    r = requests.get(url)
    if r.status_code == 200:
        return r.json()
    else:
        url = base_url + "/tag"
        payload = {"title": tag_title}
        r = requests.post(url, json=payload)
        print(r.json())
        return r.json()


# Update company with new tag
def give_tag(tag_id, stock_code):
    url = base_url + "/tag/" + str(tag_id) + "/" + stock_code
    r = requests.post(url)
    print(r)


if __name__ == '__main__':

    stock_code = "FB"
    for tag_title in get_possible_tags(stock_code):
        tag = get_tag(tag_title)
        give_tag(tag['tag_id'], stock_code)