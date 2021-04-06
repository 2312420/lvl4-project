# Common enity identifcation used for article_ident and sentence_ident
import stanza

stanza.download('en', processors='tokenize,ner', model_dir='/app/stanza_resources')
nlp = stanza.Pipeline(lang='en', processors='tokenize,ner', dir='/app/stanza_resources')


# Get list of entites from transcript
def get_entities(transcript):
     doc = nlp(transcript)
     return doc


