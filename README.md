### Description:
This tool is for creating sprite sheets and converting image sequences into other formats.

### Build Notes:

1. First you must run `\SpriteSheetCreator\sprite_sheet_creator\venv\Scripts\activate.bat`.
2. In the project explorer, right-click the `main.py` file and choose "Open in Terminal".
3. Because PyCharm uses a virtual environment, you will need to include hidden imports for Pillow. Using PyInstaller to build the .exe, use the following command:

    ```shell
    pyinstaller --onefile --paths=.\venv\ --windowed --hidden-import=PIL --hidden-import=Pillow --hidden-import=psutil --hidden-import=pyperclip --icon=main_window_widget.ico main_window_widget.py
    ```

    This will generate a `main.exe` file in the `dist` directory.

### Testing:

Nothing here yet. Need to add testing documentation.

### Notes for Building:

I've included a `requirements.txt` file. The `cat` command may or may not be necessary.

Got it to run by installing these:

    ```shell
    $ cat requirements.txt
    Pillow
    PyQT5
    psutil
    pyperclip
    moviepy
    opencv-python-headless
    ```
