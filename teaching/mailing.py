from teaching.functions import send_by_mail
import argparse

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

    send_by_mail(args.sevius, args.folder, args.verbose)