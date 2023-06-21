"""
Image Grid Application

This script provides a PyQt5-based application for importing and displaying a sequence of images in a grid layout.
The main window consists of several dock widgets and controls for managing the image sequence and playback.

Dependencies:
    - os
    - tempfile
    - PIL (Python Imaging Library)
    - PyQt5

Classes:
    - MainWindow: Represents the main window for the Image Grid application.

Methods:
    - __init__(): Initializes the ImageGridApp and sets up the main window, dock widgets, menu, and controls.
    - create_checker_pattern(width, height, square_size): Create a checker pattern image.
    - import_images(): Imports and displays images from a selected directory.
    - next_frame(): Moves to the next frame in the playback sequence.
    - update_playback_label(): Updates the playback label with the current frame from the image sequence.
    - update_start_frame(): Updates the start frame based on user input in the control widget.
    - update_end_frame(): Updates the end frame based on user input in the control widget.
    - update_fps(): Updates the frames per second (FPS) for the playback timer.
    - update_image_grid(): Updates the image grid with a sequence of visible images.
    - update_sprite_sheet(): Updates the sprite sheet based on the specified image sequence.
"""

import os
import tempfile

from pathlib import Path
from PIL import Image
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QFileDialog, QLabel, QMenuBar, QAction, \
    QDockWidget, QLineEdit, QVBoxLayout, QScrollArea, QPushButton, QHBoxLayout, QSpinBox

from threading import Thread


class MainWindow(QMainWindow):
    """
    This class represents a main window for the Image Grid application.

    The Image Grid application allows the user to import and display a sequence of images.
    The main window consists of several dock widgets and controls for managing the image sequence and playback.

    Methods:
        __init__(): Initializes the ImageGridApp and sets up the main window, dock widgets, menu, and controls.
        import_images(): Imports and displays images from a selected directory.
        next_frame(): Moves to the next frame in the playback sequence.
        update_playback_label(): Updates the playback label with the current frame from the image sequence.
        update_start_frame(): Updates the start frame based on user input in the control widget.
        update_end_frame(): Updates the end frame based on user input in the control widget.
        update_fps(): Updates the frames per second (FPS) for the playback timer.
        update_image_grid(): Updates the image grid with a sequence of visible images.
        update_sprite_sheet(): Updates the sprite sheet based on the specified image sequence.
    """

    def __init__(self):
        """
        Initializes the ImageGridApp.
        Sets up the main window, dock widgets, menu, and controls.
        """
        super().__init__()

        checker_image = self.create_checker_pattern(16, 16, 8)
        widget_background = f'background-image: url("{checker_image}"); border: 1px solid black;'

        self.setWindowTitle("Sprite Sheet Creator")
        self.setStyleSheet("background-color: White;")
        self.resize(1024, 512)

        # Set up central widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Set up the grid layout
        self.layout = QGridLayout(self.central_widget)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)

        # Set up the image dock widget
        self.image_dock_widget = QDockWidget("Image Grid", self)
        self.image_dock_widget.setStyleSheet("background-color: white; border: 1px solid black;")
        self.image_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.image_dock_widget.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.layout.addWidget(self.image_dock_widget, 1, 0, 9, 2)  # Adjust the row and column spans as needed

        # self.playback_display_bar = QMenuBar(self)

        # Set up the playback dock widget
        self.playback_dock_widget = QDockWidget("Playback", self)
        self.playback_dock_widget.setStyleSheet(widget_background)
        self.playback_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.playback_dock_widget.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.layout.addWidget(self.playback_dock_widget, 1, 2, 9, 2)  # Adjust the row and column spans as needed

        # Set up the controls dock widget
        self.controls_dock_widget = QDockWidget("Controls", self)
        self.controls_dock_widget.setStyleSheet("background-color: white; border: 1px solid black;")
        self.controls_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.controls_dock_widget.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.layout.addWidget(self.controls_dock_widget, 1, 4, 9, 2)  # Adjust the row and column spans as needed

        # TODO: Add zoom function to this widget.
        # Set up the sprite sheet dock widget
        self.sprite_sheet_dock_widget = QDockWidget("Sprite Sheet", self)
        self.sprite_sheet_dock_widget.setStyleSheet(widget_background)
        self.sprite_sheet_dock_widget.setAllowedAreas(Qt.LeftDockWidgetArea | Qt.RightDockWidgetArea)
        self.sprite_sheet_dock_widget.setFeatures(QDockWidget.AllDockWidgetFeatures)
        self.layout.addWidget(self.sprite_sheet_dock_widget, 1, 6, 9, 2)  # Adjust the row and column spans as needed

        # Set up the sprite sheet scroll area
        self.sprite_sheet_scroll_area = QScrollArea()
        self.sprite_sheet_widget = QLabel()
        self.sprite_sheet_scroll_area.setWidget(self.sprite_sheet_widget)
        self.sprite_sheet_scroll_area.setWidgetResizable(True)
        self.sprite_sheet_dock_widget.setWidget(self.sprite_sheet_scroll_area)
        # self.sprite_sheet_widget = self.sprite_sheet_scroll_area.widget()

        # Set up the menu bar
        self.menu_bar = QMenuBar(self)
        self.setMenuBar(self.menu_bar)

        # Set up the style sheet for the menu bar
        menu_bar_style = """
            QMenuBar {
                background-color: white;
            }

            QMenuBar::item:selected {
                background-color: lightGrey;
                color: black;
            }

            QMenuBar::item:pressed {
                background-color: DarkGrey;
                color: black;
            }
            
            QMenu {
                background-color: white;
            }
            
            QMenu::item:selected {
                background-color: lightGrey;
                color: black;
            }

            QMenu::item:pressed {
                background-color: LightGreen;
                color: black;
            }
            
        """

        self.menu_bar.setStyleSheet(menu_bar_style)

        # Set up the file menu
        self.file_menu = self.menu_bar.addMenu("File")

        # Set up the import action
        self.import_action = QAction("Import Image Sequence", self)
        self.import_action.triggered.connect(self.import_images)
        self.file_menu.addAction(self.import_action)

        # Set up the save action
        self.save_action = QAction("Save Image As", self)
        self.save_action.triggered.connect(self.save_image_as)
        self.file_menu.addAction(self.save_action)

        # TODO: Add an a menu bar option to save as .gif
        # TODO: Add an a menu bar option to save as .MP4
        # TODO: Add an a menu bar option to convert a video to an image sequence.

        # Set up the playback timer

        self.playback_timer = QTimer(self)
        self.playback_timer.timeout.connect(self.next_frame)
        self.playback_interval = 1000 // 24  # 24 frames per second
        self.current_frame = 0
        self.image_sequence = []

        # Set up the controls widget
        self.controls_widget = QWidget(self.controls_dock_widget)
        self.controls_layout = QVBoxLayout(self.controls_widget)
        self.controls_dock_widget.setWidget(self.controls_widget)

        play_button_style = """
            QPushButton {
                background-color: LightGreen;
                font-size: 26px;
                border-radius: 8px;  
                width: 150px;
                height: 100px;
            }

            QPushButton:hover {
                background-color: Green;
                color: black;
            }

            QPushButton:pressed {
                background-color: DarkGreen;
                color: black;
            }
        """
        stop_button_style = """
            QPushButton {
                border: 1px solid Black;
                font-size: 26px;
                border-radius: 8px;          
                width: 150px;
                height: 100px;
            }

            QPushButton:hover {
                background-color: Red;
                color: black;
            }

            QPushButton:pressed {
                background-color: DarkRed;
                color: black;
            }
        """
        label_style = """
                    QLabel {
                        background-color: White;
                        color: Black;
                        font-size: 16px;
                        border: 1px solid Black;
                        border-radius: 8px;
                        padding: 6px;
                    }
                    QLineEdit {
                        background-color: White;
                        color: Black;
                        font-size: 16px;
                        border: 1px solid Black;
                        border-radius: 8px;
                        padding: 6px;
                    }
                """

        # Set up the play button controls
        self.play_button = QPushButton("Play")
        self.play_button.setStyleSheet(play_button_style)

        # Set up the stop button controls
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(stop_button_style)

        #TODO: Convert these controls to QSpinBox, Currently doing so seems to break the sprite sheet and playback.

        # Set up the start frame controls
        self.start_frame_label = QLabel("Start Frame:")
        self.start_frame_label.setStyleSheet(label_style)
        self.start_frame_input = QLineEdit()
        self.start_frame_input.setStyleSheet(label_style)

        # Set up the end frame controls
        self.end_frame_label = QLabel("End Frame:")
        self.end_frame_label.setStyleSheet(label_style)
        self.end_frame_input = QLineEdit()
        self.end_frame_input.setStyleSheet(label_style)

        # Set up the FPS controls
        self.fps_label = QLabel("Playback FPS:")
        self.fps_label.setStyleSheet(label_style)
        self.fps_input = QLineEdit()
        self.fps_input.setStyleSheet(label_style)

        QSpinBox_style = """
            QSpinBox {
                background-color: White;
                color: Black;
                font-size: 16px;
                border: 1px solid Black;
                border-radius: 8px;
                padding: 6px;
            }
        
            QSpinBox::up-button, QSpinBox::down-button {
                width: 30px;
            }
            
            QSpinBox::up-button {
                subcontrol-border: 1px solid Black;
                subcontrol-origin: border;
                subcontrol-position: top right;
                text: "+";
            }
            
            QSpinBox::down-button {
                subcontrol-border: 1px solid Black;
                subcontrol-origin: border;
                subcontrol-position: bottom right;
            }
        """

        # TODO: Add functinality to the grid inputs to define the number or rows and columns in the sprite sheet.

        # Set up the image grid controls
        self.grid_rows_label = QLabel("Grid Rows:")
        self.grid_rows_label.setStyleSheet(label_style)
        self.grid_rows_input = QSpinBox()
        self.grid_rows_input.setStyleSheet(QSpinBox_style)
        self.grid_rows_input.setValue(8)

        self.grid_columns_label = QLabel("Grid Columns:")
        self.grid_columns_label.setStyleSheet(label_style)
        self.grid_columns_input = QSpinBox()
        self.grid_columns_input.setStyleSheet(QSpinBox_style)
        self.grid_columns_input.setValue(8)

        # Set up the image size controls
        self.image_width_label = QLabel("Image Width:")
        self.image_width_label.setStyleSheet(label_style)
        self.image_width_input = QLineEdit()
        self.image_width_input.setStyleSheet(label_style)
        self.image_height_label = QLabel("Image Height:")
        self.image_height_label.setStyleSheet(label_style)
        self.image_height_input = QLineEdit()
        self.image_height_input.setStyleSheet(label_style)

        # Create horizontal layouts for labels and inputs
        label_input_layouts = []
        for label, input_ in [
            (self.play_button, self.stop_button),
            (self.start_frame_label, self.start_frame_input),
            (self.end_frame_label, self.end_frame_input),
            (self.fps_label, self.fps_input),
            (self.grid_rows_label, self.grid_rows_input),
            (self.grid_columns_label, self.grid_columns_input),
            (self.image_width_label, self.image_width_input),
            (self.image_height_label, self.image_height_input)
        ]:
            layout = QHBoxLayout()
            layout.addWidget(label)
            layout.addWidget(input_)
            label_input_layouts.append(layout)

        for layout in label_input_layouts:
            self.controls_layout.addLayout(layout)

        # Connect the input fields to update functions
        self.play_button.clicked.connect(self.start_timer)
        self.stop_button.clicked.connect(self.stop_timer)

        self.start_frame_input.returnPressed.connect(self.update_start_frame)
        self.end_frame_input.returnPressed.connect(self.update_end_frame)

        self.fps_input.returnPressed.connect(self.update_fps)

        self.grid_rows_input.valueChanged.connect(self.update_grid_rows)
        self.grid_columns_input.valueChanged.connect(self.update_grid_columns)

        self.image_width_input.returnPressed.connect(self.update_image_size)
        self.image_height_input.returnPressed.connect(self.update_image_size)

        
    def update_grid_rows(self):
        value = self.grid_rows_input.value()
        if value <= 0:
            value = 0
        print("grid_rows_input: {}".format(value))
        
    def update_grid_columns(self):        
        value = self.grid_columns_input.value()
        if value <= 0:
            value = 0
        print("grid_columns_input: {}".format(value))

    def stop_timer(self):
        self.playback_timer.stop()

    def start_timer(self):
        self.playback_timer.start()

    def create_checker_pattern(self, width: int, height: int, square_size: int) -> str:
        """
        Create a checker pattern image.

        Args:
            width (int): The width of the image.
            height (int): The height of the image.
            square_size (int): The size of each square in pixels.

        Returns:
            str: The file path of the generated checker pattern image.
        """
        try:
            image = QImage(width, height, QImage.Format_RGBA8888)
            color1 = QColor(50, 50, 50, 255)  # Dark grey color
            color2 = QColor(50, 50, 50, 0)  # Transparent color

            for y in range(height):
                for x in range(width):
                    if (x // square_size) % 2 == (y // square_size) % 2:
                        image.setPixelColor(x, y, color1)
                    else:
                        image.setPixelColor(x, y, color2)

            # Save the image to a temporary file
            temp_file_path = tempfile.mktemp(suffix='.png')
            image.save(temp_file_path)

            # convert the path
            image_path = temp_file_path.replace("\\", "/")

            return image_path
        except Exception as err:
            self.debug(str(err.args))

    def import_images(self) -> None:
        """
        Imports and displays images from a selected directory.

        This method opens a file dialog to allow the user to select a directory.
        It then retrieves all image files (png and jpg) from the selected directory,
        creates labels for each image, and displays them in a grid layout.

        Note: This method assumes the existence of instance variables such as self.image_sequence,
        self.image_dock_widget, self.start_frame_input, self.end_frame_input, self.fps_input,
        self.playback_dock_widget, self.playback_label, self.controls_dock_widget, self.controls_widget,
        self.current_frame, self.playback_timer, self.playback_interval, and self.update_sprite_sheet().

        Returns:
            None
        """
        try:
            # TODO: Move this image importer into its own module.

            # Open file dialog to select directory
            directory = QFileDialog.getExistingDirectory(self, "Select Directory")
            if directory:
                # Retrieve image files from the selected directory
                # image_files = [file for file in os.listdir(directory) if file.endswith(".png") or file.endswith(".jpg")]
                image_files = list(Path(directory).glob("*.png")) + list(Path(directory).glob("*.jpg"))

                self.image_sequence = [os.path.join(directory, file) for file in image_files]

                num_images = len(self.image_sequence)
                grid_size = int(num_images ** 0.5)

                # Create a content widget for the image dock widget
                image_dock_content = QWidget(self.image_dock_widget)
                image_dock_layout = QGridLayout(image_dock_content)
                image_dock_layout.setSpacing(0)
                image_dock_layout.setContentsMargins(0, 0, 0, 0)

                for i, image_path in enumerate(self.image_sequence):
                    # Create pixmap and adjust image size
                    pixmap = QPixmap(image_path)
                    pixmap = pixmap.scaledToHeight(100, Qt.SmoothTransformation)

                    # Create label for the image and add it to the layout
                    image_label = QLabel()
                    image_label.setPixmap(pixmap)
                    image_dock_layout.addWidget(image_label, i // grid_size, i % grid_size)

                # Set the layout for the image dock content widget
                image_dock_content.setLayout(image_dock_layout)
                self.image_dock_widget.setWidget(image_dock_content)
                self.addDockWidget(Qt.LeftDockWidgetArea, self.image_dock_widget)

                # Set initial values for frame inputs and FPS input
                self.start_frame_input.setText("0")
                self.end_frame_input.setText(str(num_images - 1))
                self.fps_input.setText("24")

                # Set the default sprite sheet size.
                self.image_width_input.setText("2048")
                self.image_height_input.setText("2048")

                # Create a content widget for the playback dock widget
                playback_dock_content = QWidget(self.playback_dock_widget)
                playback_dock_layout = QGridLayout(playback_dock_content)
                playback_dock_layout.setSpacing(0)
                playback_dock_layout.setContentsMargins(0, 0, 0, 0)

                self.playback_label = QLabel()
                playback_dock_layout.addWidget(self.playback_label)

                # Set the layout for the playback dock content widget
                playback_dock_content.setLayout(playback_dock_layout)
                self.playback_dock_widget.setWidget(playback_dock_content)
                self.addDockWidget(Qt.RightDockWidgetArea, self.playback_dock_widget)

                # Set the controls dock widget and add it to the layout
                self.controls_dock_widget.setWidget(self.controls_widget)
                self.addDockWidget(Qt.RightDockWidgetArea, self.controls_dock_widget)

                # Initialize current frame and start the playback timer
                self.current_frame = 0
                self.playback_timer.start(self.playback_interval)
                self.update_playback_label()

                # Update the sprite sheet widget with the first image
                self.update_sprite_sheet()

                # Set up the scroll area for the sprite sheet widget
                scroll_area = QScrollArea()
                scroll_area.setWidget(self.sprite_sheet_widget)
                scroll_area.setWidgetResizable(True)
                self.sprite_sheet_dock_widget.setWidget(scroll_area)

        except Exception as err:
            self.debug(str(err.args))

    def next_frame(self) -> None:
        """
        Moves to the next frame in the module's playback sequence.

        Exception:
            If an error occurs during the process.

        Returns:
            None
        """
        try:
            # Increment the current frame by 1
            start_frame_text = self.start_frame_input.text()
            end_frame_text = self.end_frame_input.text()

            if start_frame_text and end_frame_text:
                start_frame = int(start_frame_text)
                end_frame = int(end_frame_text)

                # print(start_frame, end_frame)

                self.current_frame += 1
                if self.current_frame > end_frame:
                    # Reset the current frame to the start frame
                    self.current_frame = start_frame

            # Update the playback label to reflect the new frame
            self.update_playback_label()

        except Exception as err:
            self.debug("Next Frame error. {}".format(err.args))

    def update_playback_label(self) -> None:
        """
        Update the playback label with the current frame from the image sequence.

        Returns:
            None
        """
        try:
            if self.image_sequence:
                # Load the current frame as a QPixmap
                pixmap = QPixmap(self.image_sequence[self.current_frame])

                # Scale the image to a height of 300 pixels using smooth transformation
                pixmap = pixmap.scaledToHeight(300, Qt.SmoothTransformation)

                # Set the scaled pixmap as the image for the playback label
                self.playback_label.setPixmap(pixmap)

        except Exception as err:
            self.debug(str(err.args))

    def update_start_frame(self) -> None:
        """
        Updates the start frame based on user input in the control widget.

        Returns:
            None
        """
        try:
            # Get the start frame value from the input text
            start_frame_text = self.start_frame_input.text()

            if start_frame_text:
                # Convert the start frame value to an integer
                start_frame = int(start_frame_text)
                end_frame = int(self.end_frame_input.text())

                # Validate the start frame value
                if start_frame < 0:
                    start_frame = 0
                if start_frame > end_frame:
                    start_frame = end_frame

                # Update the start frame input text
                self.start_frame_input.setText(str(start_frame))
                # Update the current frame
                self.current_frame = start_frame
                # Update the playback label
                self.update_playback_label()
                # Update the image grid
                self.update_image_grid()
                # Update the sprite sheet
                self.update_sprite_sheet()

        except ValueError:
            # Handle the case where the start frame value is not a valid integer
            print("Invalid start frame value. Please enter a valid integer.")

    def update_end_frame(self) -> None:
        """
        Updates the end frame based on user input in the control widget.

        Returns:
            None
        """
        try:
            # Get the text from the end frame input field
            end_frame_text = self.end_frame_input.text()

            if end_frame_text:
                # Convert start frame and end frame text to integers
                start_frame = int(self.start_frame_input.text())
                end_frame = int(end_frame_text)

                # Ensure that end frame is within the range of the image sequence
                if end_frame >= len(self.image_sequence):
                    end_frame = len(self.image_sequence) - 1

                # Ensure that end frame is not less than start frame
                if end_frame < start_frame:
                    end_frame = start_frame

                # Set the updated end frame value in the end frame input field
                self.end_frame_input.setText(str(end_frame))

                # Update the current frame to the start frame
                self.current_frame = start_frame

                # Update the playback label
                self.update_playback_label()

                # Update the image grid
                self.update_image_grid()

                # Update the sprite sheet
                self.update_sprite_sheet()

        except ValueError:
            print("Invalid end frame value. Please enter a valid integer.")

    def update_fps(self) -> None:
        """
        Updates the frames per second (FPS) for the playback timer.

        Returns:
            None
        """
        try:
            # Retrieve the FPS value from the input text
            fps = int(self.fps_input.text())

            # Check if the FPS value is less than or equal to zero
            if fps <= 0:
                fps = 1  # Set a minimum FPS value of 1

            # Calculate the interval in milliseconds for the playback timer
            self.playback_interval = 1000 // fps

            # Set the interval of the playback timer
            self.playback_timer.setInterval(self.playback_interval)

        except Exception as err:
            # Print the error message if an exception occurs
            self.debug(str(err.args))

    def update_image_grid(self) -> None:
        """
        Updates the image grid with a sequence of visible images.

        This function retrieves a sequence of visible images based on the specified start and end frames.
        It adjusts the grid size to ensure an even number of rows and columns and displays the images in the grid.

        Raises:
            Exception: If an error occurs during the process.

        Returns:
            None
        """
        try:
            if self.image_sequence:
                start_frame = int(self.start_frame_input.text())
                end_frame = int(self.end_frame_input.text())

                if start_frame and end_frame:
                    visible_images = self.image_sequence[start_frame:end_frame + 1]

                    num_images = len(visible_images)
                    grid_size = int(num_images ** 0.5)
                    print("grid_size: {}".format(grid_size))

                    # Adjust grid size to ensure an even number of rows and columns
                    if grid_size % 2 != 0:
                        grid_size += 1

                    print("grid_size Adjust: {}".format(grid_size))

                    # Create the widget and layout for the image dock
                    image_dock_content = QWidget(self.image_dock_widget)
                    image_dock_layout = QGridLayout(image_dock_content)
                    image_dock_layout.setSpacing(0)
                    image_dock_layout.setContentsMargins(0, 0, 0, 0)

                    # Add each visible image to the grid
                    for i, image_path in enumerate(visible_images):
                        pixmap = QPixmap(image_path)
                        pixmap = pixmap.scaledToHeight(100, Qt.SmoothTransformation)  # Adjust the image size as needed
                        image_label = QLabel()
                        image_label.setPixmap(pixmap)
                        image_dock_layout.addWidget(image_label, i // grid_size, i % grid_size)

                    # Set the layout for the image dock
                    image_dock_content.setLayout(image_dock_layout)
                    self.image_dock_widget.setWidget(image_dock_content)

        except Exception as err:
            self.debug(str(err.args))

    def update_sprite_sheet(self) -> None:
        """
        Updates the sprite sheet based on the specified image sequence.

        Returns:
            None
        """

        try:
            # Check if there is an image sequence
            if self.image_sequence:

                # Get start and end frame values from input fields and convert them to integers
                start_frame = int(self.start_frame_input.text())
                end_frame = int(self.end_frame_input.text())

                # Set the dimensions of the sprite sheet
                sprite_sheet_width = int(self.image_width_input.text())
                sprite_sheet_height = int(self.image_height_input.text())

                # grid_rows = self.grid_rows_input.value()
                # grid_columns = self.grid_columns_input.value()

                # Calculate the grid size based on the frame range
                grid_size = int(len(self.image_sequence[start_frame:end_frame + 1]) ** 0.5)

                print("init_grid_size: {}".format(grid_size))

                if grid_size % 2 != 0:
                    grid_size += 1

                print("grid_size: {}".format(grid_size))

                # Calculate the dimensions of each image in the grid
                image_width = sprite_sheet_width // grid_size
                image_height = sprite_sheet_height // grid_size

                print("image_width: {} image_height:{}".format(image_width, image_height))

                # Create a new sprite sheet image
                sprite_sheet_image = Image.new('RGBA', (sprite_sheet_width, sprite_sheet_height), (0, 0, 0, 0))

                # Iterate over each image in the specified range
                for i, image_path in enumerate(self.image_sequence[start_frame:end_frame + 1]):
                    # Calculate the row and column index of the current image
                    row = i // grid_size
                    col = i % grid_size

                    # Open the image and resize it to fit the image dimensions in the grid
                    image = Image.open(image_path)
                    image = image.resize((image_width, image_height), resample=Image.LANCZOS)

                    # Calculate the position of the image in the sprite sheet
                    x = col * image_width
                    y = row * image_height

                    # print("row: {} col:{}".format(row, col))
                    # print("pos_x: {} pos_y:{}".format(x, y))

                    # Paste the image onto the sprite sheet
                    sprite_sheet_image.paste(image, (x, y))

                # Scale the sprite sheet to a specific height while maintaining aspect ratio
                scale_factor = sprite_sheet_width / sprite_sheet_image.height
                scaled_sprite_sheet = sprite_sheet_image.resize(
                    (int(sprite_sheet_image.width * scale_factor), sprite_sheet_height), resample=Image.LANCZOS)

                # Convert the PIL Image to a QImage
                qimage = QImage(scaled_sprite_sheet.tobytes(), scaled_sprite_sheet.size[0], scaled_sprite_sheet.size[1],
                                QImage.Format_RGBA8888)

                # Convert the QImage to a QPixmap
                sprite_sheet_pixmap = QPixmap.fromImage(qimage)

                # Set the final sprite sheet as the image displayed in the sprite sheet widget
                self.sprite_sheet_widget.setPixmap(sprite_sheet_pixmap)

                # print("update_sprite_sheet: {}x{}".format(update_sprite_sheet, image_height_text))

        except Exception as err:
            self.debug(str(err.args))

    def update_image_size(self):
        """
        Updates the image size based on user input in the control widget.

        Returns:
            None
        """
        try:
            # Get the image width and height values from the input texts
            image_width_text = self.image_width_input.text()
            image_height_text = self.image_height_input.text()

            if image_width_text and image_height_text:
                # Convert the image width and height values to integers
                image_width = int(image_width_text)
                image_height = int(image_height_text)

                # Validate the image width and height values
                if image_width <= 0:
                    image_width = 1
                if image_height <= 0:
                    image_height = 1

                # Update the image width and height input texts
                self.image_width_input.setText(str(image_width))
                self.image_height_input.setText(str(image_height))

                # Update the sprite sheet
                self.update_sprite_sheet()

                print("update_image_size: {}x{}".format(image_width_text, image_height_text))

        except ValueError:
            # Handle the case where the image width or height value is not a valid integer
            print("Invalid image width or height value. Please enter a valid integer.")

    def save_image_as(self) -> None:
        """
        Save the sprite sheet image as a PNG file.

        The image is saved based on the provided parameters and user input.

        Returns:
            None
        """
        try:
            if self.image_sequence:
                # Convert the pixmap of the sprite sheet widget to a QImage
                sprite_sheet_image = QImage(self.sprite_sheet_widget.pixmap().toImage())

                # Calculate the number of rows and columns in the sprite sheet
                num_rows = int(len(self.image_sequence[int(self.start_frame_input.text()):int(self.end_frame_input.text()) + 1]) ** 0.5)
                num_columns = num_rows

                # Calculate the frame range and frames per second (fps)
                frame_range = int(self.end_frame_input.text()) - int(self.start_frame_input.text()) + 1
                fps = int(self.fps_input.text())

                # Generate the filename based on the parameters
                filename = f"SheetName_000_{num_rows}_{num_columns}_{frame_range}_{fps}.png"

                # Open a file dialog to get the save file path
                file_path, _ = QFileDialog.getSaveFileName(self, "Save Image As", filename, filter="PNG Image (*.png)")
                if file_path:
                    # Save the sprite sheet image to the specified file path
                    sprite_sheet_image.save(file_path)

        except Exception as err:
            # Handle any exceptions and print the error message
            self.debug(str(err.args))

    @staticmethod
    def debug(message) -> None:
        """
        Displays the error message in the console.
        Args:
            message (str): The error message.

        Returns:
            None

        """
        print("Error: {}".format(message))


if __name__ == "__main__":
    try:
        app = QApplication([])
        window = MainWindow()
        window.show()
        app.exec()
    except Exception as err:
        print(err.args)
