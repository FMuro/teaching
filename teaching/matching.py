from teaching.functions import PDF_names, best_matches, rename_files, sorted_table, blackboard_list, parse_blackboard, parse_sevius
import os
import argparse

# CLI arguments

parser = argparse.ArgumentParser(
    prog='matching',
    description='Rename PDFs according to student lists from Blackboard or Sevius',
    epilog='Hope this helps!')

parser.add_argument('-b', '--blackboard', help='student lists from blackboard', nargs='+')
parser.add_argument('-s', '--sevius', help='student lists from sevius', nargs='+')
parser.add_argument('-f', '--folder', help='folder containing the PDF files', required=True)
parser.add_argument('-v', '--verbose', action='store_true',
                    help='print matching list with scores')

args = parser.parse_args()

def function():

    # check requirement
    if not args.blackboard and not args.sevius:
        print("argument -b or -s is required")
        sys.exit(1)

    # list of names
    names = []
    if args.blackboard:
        for item in args.blackboard:
            names += blackboard_list(parse_blackboard(item))
    if args.sevius:
        for item in args.sevius:
            names += list(parse_sevius(item).keys())
    names = list(set(names))

    # folder with the PDF files, whose names should be more or less the previous real names
    path = args.folder

    # get the list of PDF file names (without extension) in path
    filenames = PDF_names(path)

    # base folder name
    base_folder = os.path.basename(os.path.abspath(os.path.normpath(path)))

    # create output subfolder if it doesn't already exist
    output_folder = base_folder+'_matched'
    os.makedirs(output_folder, exist_ok=True)

    # create best match list for filenames and realnames
    # elements of this list are of the form [filename, best name match, score]
    best_matches_list, _ = best_matches(filenames, names)

    # print log if verbose mode is on ("-v" option) in decreasing failure likelihood order
    if args.verbose:
        sorted_table(best_matches_list)

    # trim scores
    for match in best_matches_list:
        match.pop()

    # rename source folder files according to dictionary whose keys are the files's names, place them in output folder and create a log file in source folder
    rename_files(path, output_folder, best_matches_list)