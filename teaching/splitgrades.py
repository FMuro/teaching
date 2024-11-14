import os
import csv
from teaching.functions import PDF_names, rename_files, split_name_grade
import argparse
from tabulate import tabulate
import pandas as pd

# CLI arguments

parser = argparse.ArgumentParser(
    prog='splitgrades',
    description='Create grading spreadsheets from PDF file names',
    epilog='Enjoy your teaching admin!')

parser.add_argument('-f', '--folder', help="folder containing the PDF files called like 'Pepe Pérez, 3,5.pdf'", required=True)
parser.add_argument('-v', '--verbose', action='store_true',
                    help='print matching list with scores')

args = parser.parse_args()


def function():
    # folder with the PDF files, whose names are the students' names followed by their grades
    path = args.folder

    # get the list of PDF file names (without extension) in path
    filenames = PDF_names(path)

    # get list of lists of the form [name, grade] sorted by name
    names_grades = [[name.upper(), grade] for name, grade in [split_name_grade(filename) for filename in filenames]]
    names_grades.sort(key=lambda x: x[0])
    
    # print grades to terminal if verbose
    if args.verbose:
        print(tabulate(names_grades, headers=['NOMBRE', 'NOTA'], numalign="decimal"))

    # create output files (CSV and LaTeX)
    root = os.path.basename(os.path.abspath(os.path.normpath(path)))
    
    csv_output = root+'_grades_list.csv'
    pd.DataFrame(names_grades, columns=['Name', 'Grade']).to_csv(csv_output, index=False, quotechar='"', quoting=csv.QUOTE_ALL, sep=',')

    print('\nCSV file with names and grades:', csv_output)

    latex_output = open(root+'_grades_list.tex', 'w')
    latex_output.write('% pdflatex '+root+'_grades_list.tex\n')
    latex_output.write('\\documentclass{article}\n\\usepackage{booktabs}\n\\begin{document}\n')
    latex_output.write(tabulate(names_grades, headers=['NOMBRE', 'NOTA'], tablefmt="latex_booktabs", numalign="decimal"))
    latex_output.write('\n\\end{document}')
    latex_output.close()
    
    print('\nLaTeX file with names and grades:', latex_output.name)