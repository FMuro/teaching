from thefuzz import process
from scipy import optimize
from scipy.sparse import csr_matrix
import numpy as np
import os
from pathlib import Path
import collections
import shutil
from unidecode import unidecode
from tabulate import tabulate
import pandas as pd
from unicodedata import normalize
import re
import csv
import sys


# normalize a string removing/modifying special characters from strings (diacritics, spaces, capitals, etc.)

def flatten_name(string):
    return unidecode(string).strip().replace(" ", "").replace(",", "").casefold()


# get the list of PDF file names (without extension) in path

def PDF_names(path):
    return [normalize('NFC', os.path.splitext(filename)[0]) for filename in os.listdir(path) if filename.endswith('.pdf')]

# parse blackboard files

def parse_blackboard(file):
    extensions = Path(file).suffixes
    if '.xls' in extensions:
        with open(file, encoding='utf-16') as f:
            content = pd.read_csv(f, sep='\t', encoding='utf8')
    elif '.csv' in extensions:
        content = pd.read_csv(file, sep=',', encoding='utf8')
    else:
        print('Blackboard parser: file extension not supported')
        sys.exit(1)
    return content
    # parse lines as elements of a list
    

# get dictionary {name: UVUS} from parsed blackboard file

def blackboard_list(content):
    row_list = {}
    for index, row in content.iterrows():
        row_list.update({row["Apellidos"]+" "+row["Nombre"]: row["Nombre de usuario"]})
    return row_list


# parse sevius file as dictionary {name: email}

def parse_sevius(file):

    # determine file extension
    extension = os.path.splitext(file)[1]

    # Read everything first without headers
    if extension == '.csv':
        content_raw = pd.read_csv(file, sep=',', encoding='utf8', header=None)
    elif extension == '.xlsx':
        content_raw = pd.read_excel(file, header=None)

    # Find the first row where the first column equals 'Documento'
    start_row = content_raw.index[content_raw.iloc[:, 0] == 'Documento'][0]

    # Read again skipping rows before that point and let pandas assign headers
    if extension == '.csv':
        content = pd.read_csv(file, sep=',', encoding='utf8', skiprows=start_row)
    elif extension == '.xlsx':
        content = pd.read_excel(file, skiprows=start_row)
    
    # create dictionary {name: email}
    dict_name_email = {}
    for index, row in content.iterrows():
        dict_name_email.update({row["Apellidos, Nombre"].replace(',',''): row["Correo electrónico"]})
    return dict_name_email


# merge lists and remove duplicates

def merge_lists(list_of_lists):
    return list(set([item for sublist in list_of_lists for item in sublist]))


# extract person name and grade from filename like 'Pepe Pérez, 3,5.pdf'
# supported input decimal separators; , . '
# decimal separator is replaced by .

def split_name_grade(filename):
    try:
        name = re.search("[^\\d|,|;|\\'|\\.]*", filename).group(0).replace(" +", " ")
    except:
        name = ""
    try:
        grade = float(re.search("\\d*[,|\\'|\\.]?\\d+", filename).group(0).replace("'", ".").replace(",", "."))
    except:
        grade = ""
    try:
        if grade == int(grade):
            grade = int(grade)
    except:
        pass
    return name, grade

# get the score matrix comparing strings in two lists

def score_matrix(list1, list2):
    rows_list = []
    columns_list = []
    scores_list = []
    list1 = [flatten_name(item) for item in list1]
    list2 = [flatten_name(item) for item in list2]
    for item, count in collections.Counter(list1).items():
        matches = process.extract(item, list2)
        for match in matches:
            rows_list.append(list1.index(item))
            columns_list.append(list2.index(match[0]))
            scores_list.append(match[1])
    rows = np.array(rows_list)
    columns = np.array(columns_list)
    scores = np.array(scores_list)
    return csr_matrix((scores, (rows, columns)), shape=(
        len(list1), len(list2))).toarray()


# given two lists, create a new list whose elements are of the form [element of first list, best match in second list, score]
# and a dictionary of the form {best match in second list: element of first list}

def best_matches(list1, list2):
    M = score_matrix(list1, list2)
    # solve the linear sum assignment problem
    [list1_positions, list2_positions] = optimize.linear_sum_assignment(
        M, maximize=True)
    return [[list1[list1_positions[i]], list2[list2_positions[i]], M[list1_positions[i], list2_positions[i]]]
            for i in range(len(list1_positions))], {list2[list2_positions[i]]: list1[list1_positions[i]]
                                                    for i in range(len(list1_positions))}


# rename source folder files according to a list of pairs of the form [filename, newname] and copy them to output folder

def rename_files(source_path, output_path, list):
    for item in list:
        shutil.copy(os.path.join(
            source_path, item[0]+'.pdf'), os.path.join(output_path, item[1]+'.pdf'))


# print table from list of lists of the form [string1, string2, score] ordered by score (descending)

def sorted_table(list, old_name = 'OLD name', new_name = 'NEW name'):
    sorted_list = sorted(list, key=lambda x: x[2])
    print(tabulate(sorted_list, headers=[old_name, new_name, 'SCORE']))

def split_grades(path, tocsv = False, tolatex = False, verbose = False):

    # get the list of PDF file names (without extension) in path
    filenames = PDF_names(path)

    # get list of lists of the form [name, grade] sorted by name
    names_grades = [[name.upper(), grade] for name, grade in [split_name_grade(filename) for filename in filenames]]
    names_grades.sort(key=lambda x: x[0])

    # dataframe with names and grades
    dataframe = pd.DataFrame(names_grades, columns=['Name', 'Grade'])
    
    # print grades to terminal if verbose
    if verbose:
        print('\nList of names and grades:\n')
        print(tabulate(names_grades, headers=['NOMBRE', 'NOTA'], numalign="decimal"))

    # create output files (CSV and LaTeX)
    root = os.path.basename(os.path.abspath(os.path.normpath(path)))
    
    if tocsv:
        csv_output = root+'_grades_list.csv'
        dataframe.to_csv(csv_output, index=False, quotechar='"', quoting=csv.QUOTE_ALL, sep=',')
        print('\nCSV file with names and grades:')
        print('file://'+os.path.join(os.getcwd(),csv_output))

    if tolatex:
        latex_output = open(root+'_grades_list.tex', 'w')
        latex_output.write('% pdflatex '+root+'_grades_list.tex\n')
        latex_output.write('\\documentclass{article}\n\\usepackage{booktabs}\n\\begin{document}\n')
        latex_output.write(tabulate(names_grades, headers=['NOMBRE', 'NOTA'], tablefmt="latex_booktabs", numalign="decimal"))
        latex_output.write('\n\\end{document}')
        latex_output.close()
        print('\nLaTeX file with names and grades:')
        print('file://'+os.path.join(os.getcwd(),latex_output.name))

    return dataframe

def send_by_mail(sevius_files, folder, verbose = False):

    # base folder name for outputs
    base_folder = os.path.basename(os.path.abspath(os.path.normpath(folder)))

    # get dictionary {PDF file name without grade: PDF file name}
    filenames_dict = {split_name_grade(file)[0]: file for file in PDF_names(folder)}
    filenames_trimmed = list(filenames_dict.keys())

    # get dictionary {student name: email} from SEVIUS files
    name_email_dict = {}
    for file in sevius_files:
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
    if verbose:
        print('\nScored list of matched names for MAILING:\n')
        sorted_table(best_matches_list, old_name="FILE name", new_name="MATCHED name")

    print('\nCSV file with names and emails:')
    print('file://'+os.path.join(os.getcwd(),base_folder+'_mailing.csv'))
