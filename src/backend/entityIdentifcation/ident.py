import spacy

nlp = spacy.load('en_core_web_sm')

Json = {"Facebook public policy director for India, South and Central Asia Ankhi Das steps down": [["Facebook public policy director for India, South and Central Asia Ankhi Das steps down", "Ankhi Das, a senior Facebook executive in India, is leaving the social media company on Tuesday, two months after media reports claimed she allegedly interfered in the company\u2019s content moderation policy and showed favoritism to Bharatiya Janata Party (BJP).Das served as the Public Policy Director for Facebook India, South and Central Asia. A Wall Street Journal story had alleged favouritism by Facebook towards India\u2019s ruling party BJP on hate speech posts. It stated that Das opposed applying hate speech rules to posts by BJP leader T Raja Singh and three other BJP leaders and groups flagged internally for promoting violence. The story had sparked a political row in India.A Facebook official told ET on condition of anonymity that Das departure does not have anything to do with the recent press reports.\u201cAnkhi has decided to step down from her role in Facebook to pursue her interest in public service,\u201d said Ajit Mohan, VP & Managing Director, Facebook India. \u201cShe has been a part of my leadership team over the last 2 years, a role in which she has made enormous contributions. We are grateful for her service and wish her the very best for the future.\u201dDas joined Facebook in 2011 and was one of their earliest employees in India."], "Economic_Times", "10/27/2020, 16:30:48"]}

sentence = Json['Facebook public policy director for India, South and Central Asia Ankhi Das steps down'][0][0]


def analyse(sent):
    doc = nlp(sent)
    for ent in doc.ents:
        if ent.label_ == "ORG":
            print(ent.text, ent.start_char, ent.end_char, ent.label_)


analyse(sentence)
