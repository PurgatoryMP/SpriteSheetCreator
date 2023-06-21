### Description:
This tool is for creating sprite sheets from image sequences.

### Requirements:
-Python 3.7 or higher.
-tempfile
-pathlib
-Pillow
-QT5

### Build Notes:

1. First you must run \SpriteSheetCreator\sprite_sheet_creator\venv\Scripts\activate.bat
2. In project explorer right click the main.py file and choose open in terminal.
3. Because pycharm uses a virtual environment you will need to include hidden imports for Pillow. Using Pyinstaller to build the .exe use the following command.

`pyinstaller --onefile --paths=.\venv\ --windowed --hidden-import=PIL --hidden-import=Pillow main.py
`
This will generate a main.exe file in the dist directory.