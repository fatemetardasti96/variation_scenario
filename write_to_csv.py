import csv 


def seperator_to_csv(seperator_list, filename):
    with open(filename,"w") as f:
        wr = csv.writer(f, delimiter = ';', lineterminator = '\n')
        for row in seperator_list:
            wr.writerow(row)