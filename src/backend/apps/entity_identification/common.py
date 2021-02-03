# Common enity identifcation used for article_ident and sentence_ident

#import spacy
#
#nlp = spacy.load('en_core_web_sm')


#def get_entities(transcript):
#    doc = nlp(transcript)
#    return doc



import stanza


stanza.download('en', processors='tokenize,ner')
nlp = stanza.Pipeline(lang='en', processors='tokenize,ner')


def get_entities(transcript):
     doc = nlp(transcript)
     return doc

