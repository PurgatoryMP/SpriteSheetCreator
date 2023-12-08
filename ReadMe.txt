### Description:
This tool is for creating sprite sheets and converting image sequences into other formats.

### Build Notes:

1. First you must run \SpriteSheetCreator\sprite_sheet_creator\venv\Scripts\activate.bat
2. In project explorer right click the main.py file and choose open in terminal.
3. Because pycharm uses a virtual environment you will need to include hidden imports for Pillow. Using Pyinstaller to build the .exe use the following command.


pyinstaller --onefile --paths=.\venv\ --windowed --hidden-import=PIL --hidden-import=Pillow --hidden-import=psutil --hidden-import=pyperclip --icon=main_window_widget.ico main_window_widget.py


This will generate a main.exe file in the dist directory.

### Testing:

Nothing here yet.
Need to add testing documentation.



Notes for building.

got it to run by installing these:

$ cat requirements.txt
Pillow
PyQT5
psutil
pyperclip
moviepy
opencv-python-headless