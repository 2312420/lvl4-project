# Common enity identifcation used for article_ident and sentence_ident

import spacy
nlp = spacy.load('en_core_web_sm')


def get_entities(transcript):
    doc = nlp(transcript)
    return doc
