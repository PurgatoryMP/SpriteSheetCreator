#Requirements:
-Python 3.7 or higher.
-Pillow
-QT5

#Description:

This tool creates a sprite sheet using a sequence of images.

#Notes:

In project explorer right click the main.py file and choose open in terminal.

Using Pyinstaller to build the .exe use the following command.

pyinstaller --onefile --paths=.\venv\ --hidden-import=PIL --hidden-import=Pillow --windowed -w "main.py"

This will generate a main.exe file in the dist directory.

