### Description:
This tool is for creating sprite sheets from image sequences.

### Requirements:
-Python 3.7 or higher.
-Pillow
-QT5

### Build Notes:

1. First you must run \SpriteSheetCreator\sprite_sheet_creator\venv\Scripts\activate.bat
2. In project explorer right click the main.py file and choose open in terminal.
3. Because pycharm uses a virtual environment you will need to include hidden imports for Pillow. Using Pyinstaller to build the .exe use the following command.

`pyinstaller --onefile --paths=.\venv\ --windowed --hidden-import=PIL --hidden-import=Pillow --add-data "Assets;Assets" main.py
`
This will generate a main.exe file in the dist directory.

### LSL script:

1. Open and copy\paste the contents of the SpriteSheetScript.lsl script to a new script in secondlife.
2. Drag and drop the sprite sheet image into the objects contents to begin playing the animation.

The link and face number for the playback is defined in the globals of the SpriteSheetScript script.

### Screen Captures:

https://gyazo.com/36a2240fb68af7c09067985c83b0dd04
https://gyazo.com/df7c671178f94fc36e5d4725fcb770a9
https://gyazo.com/4d0ed986133eebca58d77db12c671cfe