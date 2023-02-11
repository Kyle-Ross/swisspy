from filetreeprocessor import FileTree
from datetime import datetime
from time import sleep

# Starting the timing of the script
startTime = datetime.now()

# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

# CONFIG

# Defining the target folder
target_path = r"E:\Documents\PythonTestFolder\Target"

# Creating the object of the FileTree, which builds information from the file / folder tree of the target_path
file_tree_object = FileTree(target_path,
                            type_filter_mode='include',  # How you use the targets - include, exclude or all
                            file_type_targets=('.mp3', '.png'),  # File types targeted by the filter mode
                            check_mode=True,  # False by default, checks actions with you before changing names
                            folder_mode=True,  # False by default, True will include all folders
                            trim_mode=True,  # True by default, trims the new name
                            multi_space_mode=True)  # True by default, replaces multi-spaces with single

# There are 3 configurations for the regex targets above.
"""
Place a tuple with 3 items in the regex_targets list which will be passed to the regex_rename method 
of a FileTree object.

There are 3 options:
    replace
    - [0] | mode designation = 'replace'
    - [1] | regex identifying the part of the name to be replaced
    - [2] | the string that will replace the regex match in the name

    prefix
    - [0] | mode designation = 'prefix'
    - [1] | regex which will be used to match with the string
    - [2] | the string that will be inserted as the prefix for file names which match the regex

    suffix
    - [0] | mode designation = 'suffix'
    - [1] | regex which will be used to match with the string
    - [2] | the string that will be inserted as the suffix for file names which match the regex
        
When the regex_targets list is passed to the regex_rename method, multiple tuples in the targets list will be 
run in sequence, each recursively taking the result of the previous as its input.

"""

# A list containing 3 item tuples to assign specific renaming actions
regex_targets = [('prefix', r'\sMusic', 'IsMusic - '),
                 ('replace', r'\(HD\)', ''),
                 ('replace', r'Sound', 'Noises'),
                 ('replace', r'\s\([^(]*kbps\)$', ''),
                 ('suffix', r'\sGaming', ' - IsGaming')]

# |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

# STATIC - can leave this for most basic usage of the script

# Running the rename and new name generator function against the file / directory tree stored in the object
file_tree_object.regex_rename(regex_targets)

# Showing execution time
print("Script complete in...")
print(datetime.now() - startTime)

# Confirm and end script, closing window after 5 sec
print('')
print('Closing window in...')
for x in range(-3, 0):
    print('%i...' % (abs(x)))
    sleep(1)
print("Goodbye.")
