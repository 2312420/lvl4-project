import yfinance as yf
import spacy

nlp = spacy.load('en_core_web_sm')


# Get list of all companies
def get_companies():
    pass


# Get list of possible tags
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


# Check if tag already exist in database
def check_tag():
    return False


# Update company with new tag
def give_tag():
    pass


if __name__ == '__main__':
    tags = get_tags("FB")
    print(tags)
