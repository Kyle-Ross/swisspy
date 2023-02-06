import os
from txtgrabber import TxtFile

# Gets the cwd and transforms that into the relative path for the test file in the resources/txtgrabber/ folder
cwd = os.getcwd()
relative_test_file_path = cwd.replace("\\scripts\\", "\\resources\\") + "\\Test file for txtgrabber.txt"

# Creates a TxtFile object
example_object = TxtFile(relative_test_file_path,
                         remove_whitespace=True,  # True by default
                         ignore_blanks_start=True,  # True by default
                         ignore_blanks_end=True,  # True by default
                         remove_all_blanks=False)  # False by default

# Examples of what the methods in this class can do, with output printed

print("""Get the file path used to create the object:
example_object.path""")
print(example_object.path)
print("---------------------")

print("""Get the index of the first non-blank row:
example_object.first_not_blank""")
print(example_object.first_not_blank)
print("---------------------")

print("""Get the index of the last non-blank row:
example_object.last_not_blank""")
print(example_object.last_not_blank)
print("---------------------")

print("""Get the count of all rows in lines after all changes:
example_object.final_line_count""")
print(example_object.final_line_count)
print("---------------------")

print("""Get the count of all rows before any changes:
example_object.full_line_count""")
print(example_object.full_line_count)
print("---------------------")

print("""Get all lines from the txt file in a list without changes:
example_object.full_lines""")
print(example_object.full_lines)
print("---------------------")

print("""Get all lines from the txt file after all changes:
example_object.lines""")
print(example_object.lines)
print("---------------------")

print("""Get a certain line in order from the txt file after changes:
example_object.get_line(2)""")
print(example_object.get_line(2))  # Defaults to the first row if blank
print("---------------------")

print("""Print out the contents of the file line by line, defaulting to the changed content but with a raw option:
example_object.print_out(raw=False)""")
print(example_object.print_out(raw=False))  # Raw is False by default
print("---------------------")

print("""Output a copy of the file with the changes:
print(example_object.file_output('F:\\User\\Documents',
                                 suffix=' - Updated test file',
                                 overwrite_in_place=True))""")
print(example_object.file_output('F:\\User\\Documents',  # Must have a string, but will not be used by default
                                 suffix=' - Updated test file',
                                 overwrite_in_place=True))  # Creates new file in the same folder by default
print("---------------------")
