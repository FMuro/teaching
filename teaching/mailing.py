import os
import sys
from teaching.functions import PDF_names, best_matches, sorted_table, parse_sevius, split_name_grade
import argparse
import pandas as pd
import csv

parser = argparse.ArgumentParser(
    prog='mailing',
    description='Mail PDF files to a list of people with names resembling the file names',
    epilog='Enjoy your teaching admin!')

parser.add_argument(
    '-s', '--sevius', help="SEVIUS files to get the students' emails", required=True, nargs='+')
parser.add_argument(
    '-f', '--folder', help="folder containing the PDF files called like 'Pérez Pepe, 3,5.pdf'", required=True)
parser.add_argument('-v', '--verbose', action='store_true',
                    help='print matching list with scores')

args = parser.parse_args()

def function():

    # SEVIUS files
    data = args.sevius

    # folder with the PDF files, whose names should be more or less the previous full names
    path = args.folder

    # base folder name for outputs
    base_folder = os.path.basename(os.path.abspath(os.path.normpath(path)))

    # get dictionary {PDF file name without grade: PDF file name}
    filenames_dict = {split_name_grade(file)[0]: file for file in PDF_names(path)}
    filenames_trimmed = list(filenames_dict.keys())

    # get dictionary {student name: email} from SEVIUS files
    name_email_dict = {}
    for file in data:
        name_email_dict.update(parse_sevius(file))

    # create the list of student names
    names = list(name_email_dict.keys())

    # get best matches list, whose elements are lists of the form [file name, full name, score]
    # and best matches dictionary {student name: matched trimmed PDF file name}
    best_matches_list, best_matches_dict = best_matches(filenames_trimmed, names)

    # list of names with match
    names_with_match = best_matches_dict.keys()

    # write CSV file with columns "file", "email"
    pd.DataFrame({'file':[filenames_dict[best_matches_dict[name]]+'.pdf' for name in names_with_match], 'email': [name_email_dict[name] for name in names_with_match]}).to_csv(base_folder+'_mailing.csv', index=False, quotechar='"', quoting=csv.QUOTE_ALL, sep=',')

    # print log if verbose mode is on ("-v" option) in decreasing failure likelihood order
    if args.verbose:
        sorted_table(best_matches_list, old_name="FILE name", new_name="MATCHED name")
