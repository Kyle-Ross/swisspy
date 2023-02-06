import sys
import os

"""Appends the current working directory to the environment variables, which
fixed a re-occurring bug where the script would not find the pycaser code
when run in terminal via a bat file

This code needs to be before the import line which is where the error was occurring"""
sys.path.append(os.getcwd())

from pycaser import CopiedString

selected_text = CopiedString()
selected_text.proper_case()
