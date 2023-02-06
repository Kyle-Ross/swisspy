import random
import time
import pyperclip


def paste_in(string):
    """Pastes the input, for use after each method"""
    print(string)
    pyperclip.copy(string)


class CopiedString:
    def __init__(self):
        def copy_clipboard():
            """Copies selection at object initialisation"""
            # pya.hotkey('ctrl', 'c')
            time.sleep(.01)  # ctrl-c is usually very fast but your program may execute faster
            return pyperclip.paste()

        self.copied_string = copy_clipboard()
        self.replacement_string = ""

    def upper_case(self):
        """Converts to upper case"""
        self.replacement_string = self.copied_string.upper()
        paste_in(self.replacement_string)

    def lower_case(self):
        """Convert to lower case"""
        self.replacement_string = self.copied_string.lower()
        paste_in(self.replacement_string)

    def proper_case(self):
        """Converts to proper case"""
        self.replacement_string = self.copied_string.title()
        paste_in(self.replacement_string)

    def alternating_case(self):
        """Converts to alternating case with random starting character"""
        start_index = random.randint(1, 2)
        new_string_as_list = []
        for index, char in enumerate(self.copied_string):
            # Error cases for non-case characters so they are skipped
            try:
                # 50/50 chance the first char will be lower
                if start_index == 1:
                    if index % 2 == 0:
                        new_string_as_list.append(char.upper())
                    else:
                        new_string_as_list.append(char.lower())
                # 50/50 chance the first char will be upper
                else:
                    if index % 2 == 0:
                        new_string_as_list.append(char.lower())
                    else:
                        new_string_as_list.append(char.upper())
            except TypeError and AttributeError:
                continue
        self.replacement_string = ''.join(new_string_as_list)
        paste_in(self.replacement_string)
