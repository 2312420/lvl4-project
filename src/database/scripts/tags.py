import yfinance as yf
import spacy

nlp = spacy.load('en_core_web_sm')


def get_tags(stock_code):
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


if __name__ == '__main__':
    tags = get_tags("AAPL")
    print(tags)
