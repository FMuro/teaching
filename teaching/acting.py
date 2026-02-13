import os
import pandas as pd
from teaching.functions import best_matches, fill_in_acta, sorted_table, blackboard_list, parse_blackboard, split_grades, send_by_mail, fill_in_acta
import argparse
import csv
import sys

# CLI arguments

parser = argparse.ArgumentParser(
    prog='acting',
    description='Fill University of Seville\'s official grading spreadsheets (actas) from Blackboard spreadsheets',
    epilog='Enjoy your teaching admin!')

# data source
parser.add_argument('-b', '--blackboard', help="blackboard CSV or XLS files with the grades", required=True, nargs='+')
parser.add_argument('-c', '--column', help="name of column with the grades", required=True, type=str)
# verbosity
parser.add_argument('-v', '--verbose', action='store_true', help='print matching list with scores')

args = parser.parse_args()


def function():

    # folder with Blackboard files to be filled in
    sources = args.blackboard

    # dictionary of parsed blackboard files {file: dataframe}
    blackboard_dict = {}
    for source in sources:
        blackboard_dict.update({source: parse_blackboard(source)})

    # dictionary {name: UVUS} from all source files
    names_UVUS_dict = {}
    for source in sources:
        names_UVUS_dict.update(blackboard_list(blackboard_dict[source]))

    # dictionary {name: grade in column} from all source files when grade is not empty
    names_grades_dict = {}
    for source in sources:
        names_grades_dict.update({row["Apellidos"] + " " + row["Nombre"]: row[args.column] for index, row in blackboard_dict[source].iterrows() if not pd.isna(row[args.column])})
    # list of names with grade in column
    names_with_grade = list(names_grades_dict.keys())
    print(pd.Series(names_grades_dict).to_string())

    # fill in acta
    documento_list = [names_UVUS_dict[name] for name in names_with_grade]
    nota_list = [names_grades_dict[name] for name in names_with_grade]
    fill_in_acta(documento_list, nota_list)
