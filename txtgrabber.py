import os


class TxtFile:
    def __init__(self,
                 path,
                 remove_whitespace=True,
                 ignore_blanks_start=True,
                 ignore_blanks_end=True,
                 remove_all_blanks=False):
        """Class to be intialised on txt files to quickly get their data and perform
        basic transformations to the resulting list data"""
        # Get the lines of text from the file then close the file
        f = open(path, "r")
        raw_lines = f.readlines()
        f.close()

        # Define the total line count
        full_line_count: int = len(raw_lines)

        # Remove \n newlines
        self.lines = [x.replace('\n', '') for x in raw_lines]
        self.full_lines = self.lines  # Setting a var with a list of all lines with no changes except newline removal

        # Trim all whitespace - on by default
        stripped_lines = [x.strip() for x in self.lines]
        if remove_whitespace:
            self.lines = stripped_lines

        # Find the index of the first non-blank line
        for index, line in enumerate(stripped_lines):
            if line != '':
                self.first_not_blank = index
                break

        # Find the index of the last non-blank line
        for index, line in enumerate(stripped_lines[::-1]):
            if line != '':
                reverse_index = full_line_count - index
                self.last_not_blank = reverse_index
                break

        # Ignore blanks at the front and/or end of the file - both on by default
        if ignore_blanks_start and not ignore_blanks_end:
            self.lines = self.lines[self.first_not_blank:]
        elif ignore_blanks_end and not ignore_blanks_start:
            self.lines = self.lines[:self.last_not_blank]
        elif ignore_blanks_start and ignore_blanks_end:
            self.lines = self.lines[self.first_not_blank:self.last_not_blank]
        elif not ignore_blanks_start and not ignore_blanks_end:
            self.lines = self.lines  # No changes
        else:
            raise Exception("This shouldn't be possible")

        # Remove all blanks - off by default
        if remove_all_blanks:
            self.lines = [x for x in self.lines if x != '']

        # Define the final line count after all changes
        self.final_line_count = len(self.lines)

        # Defining any leftover variables
        self.path = path
        self.full_line_count = full_line_count
        self.output_path = None

    def get_line(self, line_number=1):
        """Returns a specified line from the txt file after all other changes"""
        if line_number == 0:
            line_number = 1
        line_number = line_number - 1
        return self.lines[line_number]

    def print_out(self, raw=False):
        """Prints out the changed contents of the txt file after changes, with an option for raw"""
        if not raw:
            for line in self.lines:
                print(line)
        if raw:
            for line in self.full_lines:
                print(line)
        return ''

    def file_output(self, output_folder_path, suffix='', overwrite_in_place=False):
        """Outputs the changed txt file to a path. Set suffix blank and overwrite to True to overwrite old file"""

        # Sets the output_path to the path of the target file if True, otherwise writes to the new target
        if overwrite_in_place:
            self.output_path = self.path
        else:
            self.output_path = os.path.join(output_folder_path, os.path.basename(self.path))

        # Adds the suffix, which is blank by default
        self.output_path = self.output_path.replace(".txt", "%s.txt" % suffix)

        # Writes the file to the output path
        with open(self.output_path, 'w') as f:
            f.write('\n'.join(self.lines))

        return 'File output to %s' % self.output_path
