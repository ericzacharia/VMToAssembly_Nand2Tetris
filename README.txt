Project 8

Everything works.

ZachariaEricProject8.py is a program that reads in a file (.vm) or a folder that contains one or more .vm files, 
strips comments and white space, translates vm code into lengthy assembly language,
and writes to a newly created output file (.asm) in the same location as the input file(s) or folder.

Relative Path Input File: <filename>.vm
or
Global Path Input File: <filepath>/<filename>.vm
or 
Relative Path Input Folder: <foldername>
or
Global Path Input Folder: <folderpath>


Output file will have the same file name and location as the last folder name in the directory path, with extension ".asm"

To run ZachariaEricProject8.py, type this on the command line:

python3 <filepath>/ZachariaEricProject8.py <filepath>/<filename>.vm
or 
python3 <filepath>/ZachariaEricProject8.py <folderpath>
