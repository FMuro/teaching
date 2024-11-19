import os
import pandas as pd
from teaching.functions import best_matches, sorted_table, blackboard_list, parse_blackboard, split_grades, send_by_mail
import argparse
import csv
from datetime import datetime
import shutil

# CLI arguments

parser = argparse.ArgumentParser(
    prog='grading',
    description='Fill grading spreadsheets from PDF file names',
    epilog='Enjoy your teaching admin!')

# what to fill in
parser.add_argument('-b', '--blackboard', help="blackboard CSV or XLS files to fill in", required=True, nargs='+')
parser.add_argument('-c', '--column', help="column name to fill in", required=True, type=str)
# data source
source = parser.add_mutually_exclusive_group(required=True)
source.add_argument('-f', '--folder', help="folder containing the PDF files called like 'Pérez Pepe, 3,5.pdf'")
source.add_argument('--csv', help='CSV data file with two colums: name, grade')
# additional output files
parser.add_argument('--tocsv', help="produce two-column CSV file with names and grades", action='store_true')
parser.add_argument('-l', '--latex', help="produce LaTeX file with names and grades", action='store_true')
# mailing
parser.add_argument('-s', '--sevius', help="SEVIUS files to get the students' emails", nargs='+')
# verbosity
parser.add_argument('-v', '--verbose', action='store_true', help='print matching list with scores')

args = parser.parse_args()


def function():

    # parse additional output files selection
    tocsv = args.tocsv
    tolatex = args.latex

    # check requirement
    if args.sevius and args.csv:
        print("argument -s, --sevius requires -f, --folder")
        sys.exit(1)
    
    # dataframe with names and grades
    if args.csv:
        source_read = pd.read_csv(args.csv, sep=',', encoding='utf8')
    if args.folder:
        source_read = split_grades(args.folder, tocsv, tolatex, args.verbose)

    # parse dataframe as {source name: grade} and create list of names
    source_dict = dict(source_read.itertuples(index=False, name=None))
    source_names = list(source_dict.keys())

    # folder with Blackboard files to be filled in
    targets = args.blackboard

    # dictionary of parsed blackboard files {file: dataframe}
    blackboard_dict = {}
    for target in targets:
        blackboard_dict.update({target: parse_blackboard(target)})

    # dictionary {name: UVUS} from all target files
    target_names_dict = {}
    for target in targets:
        target_names_dict.update(blackboard_list(blackboard_dict[target]))
    # list of names in target files
    target_names = list(target_names_dict.keys())

    # create best match list and dictionary for source and target names
    # elements of the list are of the form [source name, best blackboard name match, score]
    # the dictionary is of the form {best blackboard name match: source name}
    matches_list, names_dict = best_matches(source_names, target_names)
    names_dict_keys = names_dict.keys()

    # print log if verbose mode is on ("-v" option) in decreasing failure likelihood order
    if args.verbose:
        print('\nScored list of matched names for GRADING:\n')
        sorted_table(matches_list, old_name="GRADES name", new_name="MATCHED name")

    # fill in the column in the target files
    for target in targets:
        for index, row in blackboard_dict[target].iterrows():
            name = row["Apellidos"] + " " + row["Nombre"]
            if name in names_dict_keys:
                blackboard_dict[target].loc[index, args.column] = source_dict[names_dict[name]]

    # save the filled in files
    print('\nCSV files to upload to Blackboard:\n')
    for target in targets:
        file_name, _ = os.path.splitext(target)
        blackboard_dict[target].to_csv(file_name+"_filled.csv", index=False, quotechar='"', quoting=csv.QUOTE_ALL, sep=',', decimal=',')
        print('file://'+os.path.splitext(os.path.abspath(os.path.normpath(target)))[0]+"_filled.csv")

    # create an Excel file which can be uploaded to PADEL
    # you must upload it to all the "actas" containing people that have taken the exam
    # each time, the grades of people which have taken the exam and are included in the "acta" will be updated
    # there will be error messages for people that have taken the exam but are not in the "acta"
    # these errors can be dismissed because after uploading the Excel file to all possible "actas" PADEL, all grade updates will be done
    script_path = os.path.dirname(os.path.realpath(__file__))
    acta_file = 'acta_'+datetime.now().strftime("%Y%m%d_%H%M%S")+'.xlsx'
    shutil.copy(os.path.join(
            script_path, 'acta.xlsx'), os.path.join(os.getcwd(),acta_file))
    acta = pd.read_excel(acta_file, header=1)
    acta['Documento'] = [target_names_dict[name] for name in names_dict_keys]
    acta['Nota numérica'] = [source_dict[names_dict[name]] for name in names_dict_keys]
    with pd.ExcelWriter(acta_file, mode='a', if_sheet_exists='overlay') as writer:
        acta.to_excel(writer,sheet_name='Worksheet',startrow=1, index=False)
    print('\nExcel file to upload to PADEL:')
    print('file://'+os.path.join(os.getcwd(),acta_file))
    
    if args.sevius:
        send_by_mail(args.sevius, args.folder, args.verbose)