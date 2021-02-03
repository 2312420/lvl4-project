from sentence_ident import analyse
import csv
from fuzzywuzzy import fuzz
from common import get_entities
from datetime import datetime

#https://www.kaggle.com/rohitr4307/ner-dataset


def convert(lis_str):
    # Converts string into list
    new_lis = lis_str.replace("['", '')
    new_lis = new_lis.replace("']", '')
    new_lis = new_lis.split("', '")
    return new_lis


# Compares list of valid entities and list of potential entities and updates a dicts
# True Negative, True Positive, False Positive and False Negative amounts
def compare_and_update(dict, valid_ents, our_ents):
    correct = 0
    TP = TN = FN = FP = 0
    if valid_ents == [] and our_ents == []:
        TN += 1
    else:
        correct_ents = []
        for our in our_ents:
            for valid in valid_ents:
                if valid not in correct_ents:
                    ratio = fuzz.ratio(our, valid)
                    if ratio >= 60:
                        correct += 1
                        correct_ents.append(valid)


        TP = correct
        FP = len(our_ents) - correct
        FN = len(valid_ents) - correct

    dict['TN'] += TN
    dict['TP'] += TP
    dict['FP'] += FP
    dict['FN'] += FN
    return dict


# Returns list to be outputted to csv
def calculate(name ,dict):
    TN = dict['TN']
    TP = dict['TP']
    FN = dict['FN']
    FP = dict['FP']
    accuracy = (TP + TN) / (TP + TN + FP + FN)
    precision = (TP) / (TP + FP)
    recall = (TP) / (TP + TN)
    F1 = 2 * ( (precision * recall) / (precision + recall))
    return [name, TP, TN, FP, FN, accuracy, precision, recall, F1]


with open('data_sets/NER_Dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0

    # Metrics from http://www.davidsbatista.net/blog/2018/05/09/Named_Entity_Evaluation/
    truePositive = 0
    falseNegative = 0
    falsePositive = 0

    Orgs = {
        "TN": 0,
        "TP": 0,
        "FN": 0,
        "FP": 0,
    }
    Locs = {
        "TN": 0,
        "TP": 0,
        "FN": 0,
        "FP": 0,
    }
    Pers = {
        "TN": 0,
        "TP": 0,
        "FN": 0,
        "FP": 0,
    }
    Misc = {
        "TN": 0,
        "TP": 0,
        "FN": 0,
        "FP": 0,
    }

    for row in csv_reader:
        if line_count != 0:
            text = row[1].replace("['", '').replace("']", '').replace("', '", ' ')
            text_lis = text.split(" ")#convert(row[1])
            objs = convert(row[3])

            valid_orgs = []
            valid_pers = []
            valid_locs = []
            valid_misc = []

            for i in range(len(text_lis)):
                if objs[i][0] == 'B':
                    # Start of new entity
                    if objs[i] == "B-org":
                        # Organization
                        valid_orgs.append(text_lis[i])
                    elif objs[i] == "B-per":
                        # Person
                        valid_pers.append(text_lis[i])
                    elif objs[i] == "B-geo" or objs[i] == "B-gpe":
                        # Location
                        valid_locs.append(text_lis[i])
                    else:
                        valid_misc.append(text_lis[i])

                elif objs[i][0] == 'I':
                    # Continuation of previous entity
                    if objs[i] == "I-org":
                        # Continuation of organization
                        valid_orgs[-1] = valid_orgs[-1] + " " + text_lis[i]
                    elif objs[i] == "I-per":
                        # Continuation of Person
                        valid_pers[-1] = valid_pers[-1] + " " + text_lis[i]
                    elif objs[i] == "I-geo" or objs[i] == "I-gpe":
                        # Continuation of Location
                        valid_locs[-1] = valid_locs[-1] + " " + text_lis[i]
                    else:
                        valid_misc[-1] = valid_misc[-1] + " " + text_lis[i]

            doc = get_entities(text)
            our_orgs = []
            our_pers = []
            our_locs = []
            our_misc = []

            for ent in doc.ents:
                if ent.type == "ORG":
                    # Organization
                    our_orgs.append(ent.text)
                elif ent.type == "GPE" or ent.type == "LOC" or ent.type == "NORP":
                    # Location
                    our_locs.append(ent.text)
                elif ent.type == "PERSON":
                    # Person
                    our_pers.append(ent.text)
                else:
                    our_misc.append(ent.text)

            Orgs = compare_and_update(Orgs, valid_orgs, our_orgs)
            Locs = compare_and_update(Locs, valid_locs, our_locs)
            Pers = compare_and_update(Pers, valid_pers, our_pers)
            Misc = compare_and_update(Misc, valid_misc, our_misc)


        line_count += 1
        print(line_count)
        if line_count == 20000:
            break

    Overall = {
        "TN": 0,
        "TP": 0,
        "FN": 0,
        "FP": 0,
    }

    Overall["TP"] += (Orgs["TP"] + Locs["TP"] + Pers["TP"] + Misc["TP"])
    Overall["TN"] += (Orgs["TN"] + Locs["TN"] + Pers["TN"] + Misc["TN"])
    Overall["FP"] += (Orgs["FP"] + Locs["FP"] + Pers["FP"] + Misc["FP"])
    Overall["FN"] += (Orgs["FN"] + Locs["FN"] + Pers["FN"] + Misc["FN"])

    now = datetime.now().strftime("%d-%m-%Y, %H-%M")
    note = "StanzaContext"
    with open('results/' + now + "(" + note + ").csv", "x") as o:
        csv_writer = csv.writer(o, delimiter=',', )
        csv_writer.writerow(['Entity_Type', 'True Positive', 'True Negative', "False Positive", "False Negative", "Accuracy", "Precision", "Recall", "F1"])
        csv_writer.writerow(calculate("Organisation", Orgs))
        csv_writer.writerow(calculate("Person", Pers))
        csv_writer.writerow(calculate("Location", Locs))
        csv_writer.writerow(calculate("Misc", Misc))
        csv_writer.writerow(calculate("Overall", Overall))





