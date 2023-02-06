:: stops the terminal from relaying these commands when executing
@echo off

:: Sets the current directory to the parent of the folder containing this batch file
cd %~dp0

:: Sets the cd to the folder two above the folder containing the batch file, which should be the swisspy folder
:: This will allow the python code to find appropriate modules
cd "..\.."

:: 'Calls' the activation bat file in the venv folder
:: This loads the specified virtual environment containing the external packages needed
CALL "venv\Scripts\activate.bat"

:: Runs appropriate script contained in the same folder as this batch file
"scripts\pycaser\pycaser lower.py"

:: Closes the shell after running
pause