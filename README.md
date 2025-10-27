# What does this do?

This `python` package provides some CLI utilities to deal with my teaching admin:

- [matching](#matching)
- [splitgrades](#splitgrades)
- [grading](#grading)
- [mailing](#mailing)
  

# Install

Run the following command in terminal:

```
pip install --upgrade git+https://github.com/FMuro/teaching.git#egg=teaching
```

Use this command to update the package too. 
Do you use `pipx`? This is typical if you have `python` installed on macOS through `homebrew`. Then the command to install is:

```
pipx install git+https://github.com/FMuro/teaching.git#egg=teaching
```

The command to update is:

```
pipx upgrade teaching
```


# Remove

```
pip uninstall teaching
```

If you installed it using `pipx`:

```
pipx uninstall teaching
```


# matching 

```
$ matching -h
usage: matching [-h] -f FOLDER (-b BLACKBOARD [BLACKBOARD ...] |
                -s SEVIUS [SEVIUS ...]) [-v]

Rename PDFs according to student lists from Blackboard or Sevius

options:
  -h, --help            show this help message and exit
  -f, --folder FOLDER   folder containing the PDF files
  -b, --blackboard BLACKBOARD [BLACKBOARD ...]
                        student lists from blackboard
  -s, --sevius SEVIUS [SEVIUS ...]
                        student lists from sevius
  -v, --verbose         print matching list with scores

Hope this helps!
```


# splitgrades

```
$ splitgrades  -h
usage: splitgrades [-h] -f FOLDER [-v]

Create grading spreadsheets from PDF file names

options:
  -h, --help            show this help message and exit
  -f, --folder FOLDER   folder containing the PDF files called like 'Pepe
                        Pérez, 3,5.pdf'
  -v, --verbose         print list with names and grades

Enjoy your teaching admin!
```


# grading

```
$ grading -h
usage: grading [-h] -b BLACKBOARD [BLACKBOARD ...] -c COLUMN (-f FOLDER |
               --csv CSV) [--tocsv] [-l] [-s SEVIUS [SEVIUS ...]] [-v]

Fill grading spreadsheets from PDF file names

options:
  -h, --help            show this help message and exit
  -b, --blackboard BLACKBOARD [BLACKBOARD ...]
                        blackboard CSV or XLS files to fill in
  -c, --column COLUMN   column name to fill in
  -f, --folder FOLDER   folder containing the PDF files called like 'Pérez
                        Pepe, 3,5.pdf'
  --csv CSV             CSV data file with two colums: name, grade
  --tocsv               produce two-column CSV file with names and grades
  -l, --latex           produce LaTeX file with names and grades
  -s, --sevius SEVIUS [SEVIUS ...]
                        SEVIUS files to get the students' emails
  -v, --verbose         print matching list with scores

Enjoy your teaching admin!
```


# mailing 

```
$ mailing -h
usage: mailing [-h] -s SEVIUS [SEVIUS ...] -f FOLDER [-v]

Mail PDF files to a list of people with names resembling the file names

options:
  -h, --help            show this help message and exit
  -s, --sevius SEVIUS [SEVIUS ...]
                        SEVIUS files to get the students' emails
  -f, --folder FOLDER   folder containing the PDF files called like 'Pérez
                        Pepe, 3,5.pdf'
  -v, --verbose         print matching list with scores

Enjoy your teaching admin!
```