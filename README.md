# swisspy

swisspy is a custom Python library made to contain the various functions and classes I write for everyday work at home and in the office. It is written in a modular way so that it can easily be deployed when I need certain functionality in other pieces of code. It is also a practice case for me in clean and modular programming in Python. I plan to continue building and adding to this as the need arises.

## pycaser

This functionality combines Python, Batch and AutoHotKey to enable the ability to change the case of selected text in-place with the press of a hotkey on a windows machine.

It currently has 4 options:

- `selected_text.proper_case()` Where 'Example text' becomes 'Example Text'
- `selected_text.lower_case()` Where 'Example text' becomes 'example text'
- `selected_text.upper_case()` Where 'Example text' becomes 'EXAMPLE TEXT'
- `selected_text.alternating_case()` Where 'Example text' becomes 'eXaMpLe tExT'

![How it works](https://i.imgur.com/91Llxy3.gif)


## txtgrabber

Occasionally I find myself having to parse data stored in .txt files for whatever reasons. This package contains various functions to make it easier through the 'TxtFile' object. This includes:

- Removing all blank rows at the start of the file (avoids errors when processing CSV style data)
- Trim whitespace at the beginning or end of a line
- Return the file has a list object before or after other changes
- Return specific lines through number reference
- Get row counts before and after removals or changes
- Output the an updated .txt file with changes included

Example usage can be seen in in the scripts folder.


## filetreeprocessor

Module for manipulating files and folders contained in a file tree. The script takes a folder as input and recursively gathers information on all files and subdirectories.

It stores this information in a **FileTree** object, making it available for use in various methods.

Only has functions to manipulate file names at current, but I would like to eventually add conditional file movements and copying.

### Methods

#### regex_rename

Taking a nested list of multiple regexes and action types, this method works through the file tree recursively applying all renaming actions one after the other on relevant files in the tree.

Includes optional trim, cleaning and checking functionality easily configured in object initialisation code.

Any amount of these 3 options can easily be added and run against the whole file tree in each run of the script.
    
replace
- Identify and replace a part of the file name based on a regex pattern

prefix
- Add a prefix to file names which match a provided regex pattern
    
suffix
- Add a suffix to file names which match a provided regex pattern

For an example of a list of renaming actions that can be run simulaneously across a FileTree object, see the template in the 'scripts/filetreeprocessor' folder.