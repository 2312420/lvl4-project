from sentence_ident import analyse
import csv

#https://www.kaggle.com/rohitr4307/ner-dataset


def convert(lis_str):
    # Converts string into list
    new_lis = lis_str.replace("['", '')
    new_lis = new_lis.replace("']", '')
    new_lis = new_lis.split("', '")
    return new_lis


with open('data_sets/NER_Dataset.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            text = convert(row[1])
            objs = convert(row[3])

            orgs = []
            for i in range(len(text)):
                if objs[i] == "B-org":
                    orgs.append(text[i])

            print(orgs)

        line_count += 1

        if line_count == 5:
            break


