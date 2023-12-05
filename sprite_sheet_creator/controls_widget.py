from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QSpinBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QScrollArea, \
    QFrame, QCheckBox

import style_sheet


class ControlWidget(QWidget):
    """A widget for controlling playback and settings.

    This widget provides controls for managing playback, such as play and stop buttons, as well as
    settings for frame range, FPS, image grid, and image size. It emits signals when the control values
    are changed.
    """

    # Define all the signals.
    fpsValueChanged = pyqtSignal(int)
    display_frame_Changed = pyqtSignal(int)
    start_frame_Value_Changed = pyqtSignal(int)
    end_frame_Value_Changed = pyqtSignal(int)
    grid_row_Value_Changed = pyqtSignal(int)
    grid_column_Value_Changed = pyqtSignal(int)
    image_width_Value_Changed = pyqtSignal(int)
    image_height_Value_Changed = pyqtSignal(int)
    playClicked = pyqtSignal()
    stopClicked = pyqtSignal()
    use_grid_checkboxStateChanged = pyqtSignal(bool)
    use_index_checkboxStateChanged = pyqtSignal(bool)
    use_scale_checkboxStateChanged = pyqtSignal(bool)

    def __init__(self, main_console_widget):
        """Initialize the ControlWidget.

        Args:
            console_widget (QWidget): The console widget in which messages and errors are displayed.
        """
        super().__init__()

        self.console = main_console_widget

        # Set up the play button controls.
        self.play_button = QPushButton("Play")
        self.play_button.setStyleSheet(style_sheet.play_btn_style())

        # Set up the stop button controls.
        self.stop_button = QPushButton("Stop")
        self.stop_button.setStyleSheet(style_sheet.stop_btn_style())

        # Set up the start frame controls.
        self.start_frame_label = QLabel("Start Frame:")
        self.start_frame_label.setStyleSheet(style_sheet.bubble_label_style())
        self.start_frame_input = QSpinBox()
        self.start_frame_input.setRange(0, 9999)
        self.start_frame_input.setStyleSheet(style_sheet.spinbox_style())
        # set the initial value for the start frame to 0
        self.start_frame_input.setValue(0)

        # Set up the end frame controls.
        self.end_frame_label = QLabel("End Frame:")
        self.end_frame_label.setStyleSheet(style_sheet.bubble_label_style())
        self.end_frame_input = QSpinBox()
        self.end_frame_input.setRange(0, 9999)
        self.end_frame_input.setStyleSheet(style_sheet.spinbox_style())

        # Set up the FPS controls.
        self.fps_label = QLabel("Playback FPS:")
        self.fps_label.setStyleSheet(style_sheet.bubble_label_style())
        self.fps_input = QSpinBox()
        self.fps_input.setRange(0, 128)
        self.fps_input.setStyleSheet(style_sheet.spinbox_style())
        # set the initial value for the fps to 30
        self.fps_input.setValue(24)

        # Set up the image grid controls.
        self.grid_rows_label = QLabel("Grid Rows:")
        self.grid_rows_label.setStyleSheet(style_sheet.bubble_label_style())
        self.grid_rows_input = QSpinBox()
        self.grid_rows_input.setRange(0, 9999)
        self.grid_rows_input.setStyleSheet(style_sheet.spinbox_style())
        self.grid_rows_input.setValue(8)

        self.grid_columns_label = QLabel("Grid Columns:")
        self.grid_columns_label.setStyleSheet(style_sheet.bubble_label_style())
        self.grid_columns_input = QSpinBox()
        self.grid_columns_input.setRange(0, 9999)
        self.grid_columns_input.setStyleSheet(style_sheet.spinbox_style())
        self.grid_columns_input.setValue(8)

        # Set up the image size controls.
        self.image_width_label = QLabel("Image Width:")
        self.image_width_label.setStyleSheet(style_sheet.bubble_label_style())
        self.image_width_input = QSpinBox()
        self.image_width_input.setRange(0, 4096)
        self.image_width_input.setStyleSheet(style_sheet.spinbox_style())

        self.image_height_label = QLabel("Image Height:")
        self.image_height_label.setStyleSheet(style_sheet.bubble_label_style())
        self.image_height_input = QSpinBox()
        self.image_height_input.setRange(0, 4096)
        self.image_height_input.setStyleSheet(style_sheet.spinbox_style())

        # Set the default sprite sheet size.
        self.image_width_input.setValue(2048)
        self.image_height_input.setValue(2048)

        self.combined_sprite_sheet_width = 0
        self.combined_sprite_sheet_height = 0
        self.defined_sprite_sheet_width = 0
        self.defined_sprite_sheet_height = 0

        # Set the controls for the frame number output
        self.frame_number_label = QLabel("Frame Number:")
        self.frame_number_label.setStyleSheet(style_sheet.bubble_label_style())
        self.frame_number_display = QSpinBox()
        self.frame_number_display.setRange(0, 9999)
        self.frame_number_display.setStyleSheet(style_sheet.spinbox_style())
        # set the initial value for the Frame Number to 0
        self.frame_number_display.setValue(0)

        self.use_grid_checkbox = QCheckBox("Grid Overlay")
        self.use_grid_checkbox.setStyleSheet(style_sheet.checkbox_style())
        self.use_grid_checkbox.setChecked(False)
        self.use_grid_checkbox.setToolTip(
            "toggle on or off the outline around each cell for clear visibility.\n"
            "This layer is baked into the sprite sheet if left enabled on export.")

        self.use_index_checkbox = QCheckBox("Index Overlay")
        self.use_index_checkbox.setStyleSheet(style_sheet.checkbox_style())
        self.use_index_checkbox.setChecked(False)
        self.use_index_checkbox.setToolTip(
            "toggle on or off the frame number for clear visibility.\n"
            "This layer is baked into the sprite sheet if left enabled on export.")

        self.use_scale_checkbox = QCheckBox("Original scale")
        self.use_scale_checkbox.setStyleSheet(style_sheet.checkbox_style())
        self.use_scale_checkbox.setChecked(False)
        self.use_scale_checkbox.setToolTip(
            "Enabled: Use the source image scale for each cell.\n"
            "Disabled: Down scale each frame to fit the defined image scale.")

        # Display settings in console.
        # self.console.append_text("INFO: Control Settings:-------------")
        # self.console.append_text("INFO: FPS = {}".format(self.fps_input.value()))
        # self.console.append_text("INFO: Grid Rows = {}".format(self.grid_rows_input.value()))
        # self.console.append_text("INFO: Grid Columns = {}".format(self.grid_columns_input.value()))
        # self.console.append_text("INFO: Grid Overlay = {}".format(self.use_grid_checkbox.isChecked()))
        # self.console.append_text("INFO: Index Overlay = {}".format(self.use_index_checkbox.isChecked()))
        # self.console.append_text("INFO: Use Original Scale = {}".format(self.use_scale_checkbox.isChecked()))
        # self.console.append_text("INFO: sprite sheet width = {}".format(self.image_width_input.value()))
        # self.console.append_text("INFO: sprite sheet height = {}".format(self.image_height_input.value()))

        self.separator1 = QLabel("Playback:")
        self.separator1.setStyleSheet(style_sheet.seperator_label_style())

        self.separator2 = QFrame()
        self.separator2.setFrameShape(QFrame.HLine)
        self.separator2.setFrameShadow(QFrame.Sunken)
        self.separator2.setFixedHeight(2)

        self.separator3 = QLabel("Frame Range:")
        self.separator3.setStyleSheet(style_sheet.seperator_label_style())

        self.separator4 = QFrame()
        self.separator4.setFrameShape(QFrame.HLine)
        self.separator4.setFrameShadow(QFrame.Sunken)
        self.separator4.setFixedHeight(2)

        self.separator5 = QLabel("Sprite Sheet:")
        self.separator5.setStyleSheet(style_sheet.seperator_label_style())

        self.separator6 = QFrame()
        self.separator6.setFrameShape(QFrame.HLine)
        self.separator6.setFrameShadow(QFrame.Sunken)
        self.separator6.setFixedHeight(2)

        self.separator7 = QFrame()
        self.separator7.setFrameShape(QFrame.HLine)
        self.separator7.setFrameShadow(QFrame.Sunken)
        self.separator7.setFixedHeight(2)

        # self.separator8 = QFrame()
        # self.separator8.setFrameShape(QFrame.HLine)
        # self.separator8.setFrameShadow(QFrame.Sunken)
        # self.separator8.setFixedHeight(2)

        controls = [
            (self.play_button, self.stop_button),
            (self.separator1, self.separator2),
            (self.frame_number_label, self.frame_number_display),
            (self.fps_label, self.fps_input),
            (self.separator3, self.separator4),
            (self.start_frame_label, self.start_frame_input),
            (self.end_frame_label, self.end_frame_input),
            (self.separator5, self.separator6),
            (self.use_grid_checkbox, self.use_index_checkbox),
            (self.grid_rows_label, self.grid_rows_input),
            (self.grid_columns_label, self.grid_columns_input),
            (self.use_scale_checkbox, self.separator7),
            (self.image_width_label, self.image_width_input),
            (self.image_height_label, self.image_height_input)
        ]

        self.controls_layout = QVBoxLayout()

        for label, input_ in controls:
            control_layout = QHBoxLayout()
            control_layout.addWidget(label)
            control_layout.addWidget(input_)
            self.controls_layout.addLayout(control_layout)

        # Create a scroll area and set the layout
        self.scroll_area = QScrollArea()
        self.scroll_area.setStyleSheet(style_sheet.scroll_bar_style())
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumWidth(250)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_widget = QWidget()
        self.scroll_widget.setLayout(self.controls_layout)
        self.scroll_area.setWidget(self.scroll_widget)

        # Set the scroll area as the main widget
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.scroll_area)

        # Connect the controls
        self.fps_input.valueChanged.connect(self.fpsValueChanged.emit)
        self.frame_number_display.valueChanged.connect(self.display_frame_Changed.emit)
        self.start_frame_input.valueChanged.connect(self.start_frame_Value_Changed.emit)
        self.end_frame_input.valueChanged.connect(self.end_frame_Value_Changed.emit)
        self.grid_rows_input.valueChanged.connect(self.grid_row_Value_Changed.emit)
        self.grid_columns_input.valueChanged.connect(self.grid_column_Value_Changed.emit)
        self.image_width_input.valueChanged.connect(self.image_width_Value_Changed.emit)
        self.image_height_input.valueChanged.connect(self.image_height_Value_Changed.emit)
        self.use_grid_checkbox.stateChanged.connect(self.use_grid_checkboxStateChanged.emit)
        self.use_index_checkbox.stateChanged.connect(self.use_index_checkboxStateChanged.emit)
        self.use_scale_checkbox.stateChanged.connect(self.use_scale_checkboxStateChanged.emit)
        self.play_button.clicked.connect(self.playClicked.emit)
        self.stop_button.clicked.connect(self.stopClicked.emit)

        self.console.append_text("INFO: Controls Widget Loaded.")

    def update_frame_number(self, value: int):
        """Update the frame number display.

        This method updates the value displayed in the frame number display.

        Args:
            value (int): The new frame number value.
        """
        self.frame_number_display.setValue(value)

    def get_fps_value(self) -> int:
        """Get the current FPS value.

        Returns:
            int: The current FPS value.
        """
        value = self.fps_input.value()
        return value

    def set_fps_value(self, value) -> None:
        """Set the FPS value.

        Args:
            value: The new FPS value.
        """
        self.fps_input.setValue(value)

    def set_display_value(self, value):
        """Set the frame number display value.

        Args:
            value: The new frame number display value.
        """
        self.frame_number_display.setValue(value)

    def get_display_value(self):
        """Get the frame number display value.

        Returns:
            int: The new frame number display value.
        """
        value = self.frame_number_display.value()
        return value

    def get_start_frame_value(self) -> int:
        """Get the current start frame value.

        Returns:
            int: The current start frame value.
        """
        value = self.start_frame_input.value()
        return value

    def set_start_frame_value(self, value) -> None:
        """Set the start frame value.

        Args:
            value: The new start frame value.
        """
        self.start_frame_input.setValue(value)

    def get_end_frame_value(self) -> int:
        """Get the current end frame value.

        Returns:
            int: The current end frame value.
        """
        value = self.end_frame_input.value()
        return value

    def set_end_frame_value(self, value) -> None:
        """Set the end frame value.

        Args:
            value: The new end frame value.
        """
        self.end_frame_input.setValue(value)

    def get_grid_rows_value(self) -> int:
        """Get the current grid rows value.

        Returns:
            int: The current grid rows value.
        """
        value = self.grid_rows_input.value()
        return value

    def set_grid_rows_value(self, value: int) -> None:
        """Set the grid rows value.

        Args:
            value (int): The new grid rows value.
        """
        self.grid_rows_input.setValue(value)

    def get_grid_columns_value(self) -> int:
        """Get the current grid columns value.

        Returns:
            int: The current grid columns value.
        """
        value = self.grid_columns_input.value()
        return value

    def set_grid_columns_value(self, value: int) -> None:
        """Set the grid columns value.

        Args:
            value (int): The new grid columns value.
        """
        self.grid_columns_input.setValue(value)

    def get_image_width_value(self) -> int:
        """Get the current image width value.

        Returns:
            int: The current image width value.
        """
        value = self.image_width_input.value()
        return value

    def set_image_width_value(self, value: int) -> None:
        """Set the image width value.

        Args:
            value (int): The new image width value.
        """
        self.image_width_input.setValue(value)

    def get_image_height_value(self) -> int:
        """Get the current image height value.

        Returns:
            int: The current image height value.
        """
        value = self.image_height_input.value()
        return value

    def set_image_height_value(self, value: int) -> None:
        """Set the image height value.

        Args:
            value (int): The new image height value.
        """
        self.image_height_input.setValue(value)

    def toggle_scale_value_control(self, value: bool) -> None:
        """
         toggles the image scale value controls on and off depending on if the user has checked the option to use original scale.
        """
        if not value:
            self.image_width_input.setEnabled(True)
            self.image_height_input.setEnabled(True)
            self.image_width_input.setStyleSheet(style_sheet.spinbox_style())
            self.image_height_input.setStyleSheet(style_sheet.spinbox_style())

        else:
            self.image_width_input.setEnabled(False)
            self.image_height_input.setEnabled(False)
            self.image_width_input.setStyleSheet(style_sheet.spinbox_style_disabled())
            self.image_height_input.setStyleSheet(style_sheet.spinbox_style_disabled())


