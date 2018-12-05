import csv


def csv_reader(file_obj):
    reader = csv.reader(file_obj)
    for row in reader:
        print(" ".join(row))


def csv_entry_list_reader(file_obj) -> list:
    reader = csv.DictReader(file_obj, delimiter=',')
    entry_list = []
    for row in reader:
        entry_list.append(dict(row))
    return entry_list
