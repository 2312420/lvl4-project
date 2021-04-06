import common as c

base_url = "http://backend-api:5000"


# Analyse article transcript for organisation entities
def analyse(transcript):
    doc = c.get_entities(transcript)
    orgs = []
    for ent in doc.ents:
        if ent.type == 'ORG':
            orgs.append(ent.text)
    return orgs

