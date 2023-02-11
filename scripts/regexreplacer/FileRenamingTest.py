from filetreeprocessor import FilesFolderClass
from datetime import datetime
from time import sleep

# Starting the timing of the script
startTime = datetime.now()

# Defining the target folder
target_path = r"E:\Documents\PythonTestFolder\Target"

# Creating the object of the FilesFolderClass
filefolderobject = FilesFolderClass(target_path,
                                    type_filter_mode='include',
                                    file_type_targets=('.mp3', '.png'),
                                    check_mode=True)

# A list containing tuples with a regex to match against and the replacement to insert
regex_targets = [('prefix', 'ignored', 'Prefix - '),
                 ('replace', r'\(HD\)', ''),
                 ('replace', r'Sound', 'Noises'),
                 ('replace', r'\s\([^(]*kbps\)$', ''),
                 ('suffix', 'ignored', '- Suffix')]

# Running the regex_rename method which will rename the files using the specified regexes, one after the other
# The output from the 1st change is used as the input in the second change, and so on until the end of the regex list,
# across all targeted files
filefolderobject.regex_rename(regex_targets)

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
