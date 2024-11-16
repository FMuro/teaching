from teaching.functions import split_grades
import argparse

# CLI arguments

parser = argparse.ArgumentParser(
    prog='splitgrades',
    description='Create grading spreadsheets from PDF file names',
    epilog='Enjoy your teaching admin!')

parser.add_argument('-f', '--folder', help="folder containing the PDF files called like 'Pepe Pérez, 3,5.pdf'", required=True)
parser.add_argument('-v', '--verbose', action='store_true',
                    help='print matching list with scores')

args = parser.parse_args()

# folder with the PDF files, whose names are the students' names followed by their grades


def function():

    split_grades(args.folder, True, True, args.verbose)