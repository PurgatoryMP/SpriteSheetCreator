from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QSpinBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QScrollArea, \
    QFrame, QCheckBox

import style_sheet


class ControlWidget(QWidget):
    """A widget for controlling playback and settings.

        This widget provides controls for managing playback, such as play and stop buttons, as well as
        settings for frame range, FPS, image grid, and image size. It emits signals when the control values
        are changed.

        Args:
            control_widget (QWidget): The parent widget to which this control widget belongs.

        Signals:
            fpsValueChanged (int): Emitted when the FPS value is changed.
            startframeValueChanged (int): Emitted when the start frame value is changed.
            endframeValueChanged (int): Emitted when the end frame value is changed.
            gridrowValueChanged (int): Emitted when the grid rows value is changed.
            gridcolumnValueChanged (int): Emitted when the grid columns value is changed.
            imagewidthValueChanged (int): Emitted when the image width value is changed.
            imageheightValueChanged (int): Emitted when the image height value is changed.
            playClicked: Emitted when the play button is clicked.
            stopClicked: Emitted when the stop button is clicked.
        """

    fpsValueChanged = pyqtSignal(int)
    displayframeChanged = pyqtSignal(int)
    startframeValueChanged = pyqtSignal(int)
    endframeValueChanged = pyqtSignal(int)
    gridrowValueChanged = pyqtSignal(int)
    gridcolumnValueChanged = pyqtSignal(int)
    imagewidthValueChanged = pyqtSignal(int)
    imageheightValueChanged = pyqtSignal(int)
    playClicked = pyqtSignal()
    stopClicked = pyqtSignal()
    use_grid_checkboxStateChanged = pyqtSignal(bool)
    use_scale_checkboxStateChanged = pyqtSignal(bool)

    def __init__(self, main_console_widget):
        """Initialize the ControlWidget.

        Args:
            console_widget (QWidget): The console widget in which messages and errors are displayed.
        """
        super().__init__()

        self.console = main_console_widget
        self.console.append_text("INFO: Loading Controls Widget.----------------")

        # Set up the play button controls.
        play_button = QPushButton("Play")
        play_button.setStyleSheet(style_sheet.play_btn_style())

        # Set up the stop button controls.
        stop_button = QPushButton("Stop")
        stop_button.setStyleSheet(style_sheet.stop_btn_style())

        # Set up the start frame controls.
        start_frame_label = QLabel("Start Frame:")
        start_frame_label.setStyleSheet(style_sheet.bubble_label_style())
        self.start_frame_input = QSpinBox()
        self.start_frame_input.setRange(0, 9999)
        self.start_frame_input.setStyleSheet(style_sheet.spinbox_style())
        # set the initial value for the start frame to 0
        self.start_frame_input.setValue(0)

        # Set up the end frame controls.
        end_frame_label = QLabel("End Frame:")
        end_frame_label.setStyleSheet(style_sheet.bubble_label_style())
        self.end_frame_input = QSpinBox()
        self.end_frame_input.setRange(0, 9999)
        self.end_frame_input.setStyleSheet(style_sheet.spinbox_style())

        # Set up the FPS controls.
        fps_label = QLabel("Playback FPS:")
        fps_label.setStyleSheet(style_sheet.bubble_label_style())
        self.fps_input = QSpinBox()
        self.fps_input.setRange(0, 128)
        self.fps_input.setStyleSheet(style_sheet.spinbox_style())
        # set the initial value for the fps to 30
        self.fps_input.setValue(24)

        # Set up the image grid controls.
        grid_rows_label = QLabel("Grid Rows:")
        grid_rows_label.setStyleSheet(style_sheet.bubble_label_style())
        self.grid_rows_input = QSpinBox()
        self.grid_rows_input.setRange(0, 9999)
        self.grid_rows_input.setStyleSheet(style_sheet.spinbox_style())
        self.grid_rows_input.setValue(8)

        grid_columns_label = QLabel("Grid Columns:")
        grid_columns_label.setStyleSheet(style_sheet.bubble_label_style())
        self.grid_columns_input = QSpinBox()
        self.grid_columns_input.setRange(0, 9999)
        self.grid_columns_input.setStyleSheet(style_sheet.spinbox_style())
        self.grid_columns_input.setValue(8)

        # Set up the image size controls.
        image_width_label = QLabel("Image Width:")
        image_width_label.setStyleSheet(style_sheet.bubble_label_style())
        self.image_width_input = QSpinBox()
        self.image_width_input.setRange(0, 4096)
        self.image_width_input.setStyleSheet(style_sheet.spinbox_style())

        image_height_label = QLabel("Image Height:")
        image_height_label.setStyleSheet(style_sheet.bubble_label_style())
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
        frame_number_label = QLabel("Frame Number:")
        frame_number_label.setStyleSheet(style_sheet.bubble_label_style())
        self.frame_number_display = QSpinBox()
        self.frame_number_display.setRange(0, 9999)
        self.frame_number_display.setStyleSheet(style_sheet.spinbox_style())
        # set the initial value for the Frame Number to 0
        self.frame_number_display.setValue(0)

        self.use_grid_checkbox = QCheckBox("Grid Overlay")
        self.use_grid_checkbox.setChecked(False)
        self.use_grid_checkbox.setToolTip(
            "toggle on or off the outline around each cell for clear visibility.\n"
            "This layer is baked into the sprite sheet if left enabled on export.")

        self.use_scale_checkbox = QCheckBox("Original scale")
        self.use_scale_checkbox.setChecked(False)
        self.use_scale_checkbox.setToolTip(
            "Enabled: Use the source image scale for each cell.\n"
            "Disabled: Down scale each frame to fit the defined image scale.")

        self.console.append_text("INFO: Control Settings:-------------")
        self.console.append_text("INFO: FPS = {}".format(self.fps_input.value()))
        self.console.append_text("INFO: Grid Rows = {}".format(self.grid_rows_input.value()))
        self.console.append_text("INFO: Grid Columns = {}".format(self.grid_columns_input.value()))
        self.console.append_text("INFO: Grid Overlay = {}".format(self.use_grid_checkbox.isChecked()))
        self.console.append_text("INFO: Use Original Scale = {}".format(self.use_scale_checkbox.isChecked()))
        self.console.append_text("INFO: sprite sheet width = {}".format(self.image_width_input.value()))
        self.console.append_text("INFO: sprite sheet height = {}".format(self.image_height_input.value()))

        separator1 = QLabel("Playback:")
        separator1.setStyleSheet(style_sheet.seperator_label_style())

        separator2 = QFrame()
        separator2.setFrameShape(QFrame.HLine)
        separator2.setFrameShadow(QFrame.Sunken)
        separator2.setFixedHeight(2)

        separator3 = QLabel("Frame Range:")
        separator3.setStyleSheet(style_sheet.seperator_label_style())

        separator4 = QFrame()
        separator4.setFrameShape(QFrame.HLine)
        separator4.setFrameShadow(QFrame.Sunken)
        separator4.setFixedHeight(2)

        separator5 = QLabel("Sprite Sheet:")
        separator5.setStyleSheet(style_sheet.seperator_label_style())

        separator6 = QFrame()
        separator6.setFrameShape(QFrame.HLine)
        separator6.setFrameShadow(QFrame.Sunken)
        separator6.setFixedHeight(2)

        separator7 = QFrame()
        separator7.setFrameShape(QFrame.HLine)
        separator7.setFrameShadow(QFrame.Sunken)
        separator7.setFixedHeight(2)

        separator8 = QFrame()
        separator8.setFrameShape(QFrame.HLine)
        separator8.setFrameShadow(QFrame.Sunken)
        separator8.setFixedHeight(2)

        controls = [
            (play_button, stop_button),
            (separator1, separator2),
            (frame_number_label, self.frame_number_display),
            (fps_label, self.fps_input),
            (separator3, separator4),
            (start_frame_label, self.start_frame_input),
            (end_frame_label, self.end_frame_input),
            (separator5, separator6),
            (self.use_grid_checkbox, separator7),
            (grid_rows_label, self.grid_rows_input),
            (grid_columns_label, self.grid_columns_input),
            (self.use_scale_checkbox, separator8),
            (image_width_label, self.image_width_input),
            (image_height_label, self.image_height_input)
        ]

        layout = QVBoxLayout()

        for label, input_ in controls:
            control_layout = QHBoxLayout()
            control_layout.addWidget(label)
            control_layout.addWidget(input_)
            layout.addLayout(control_layout)

        # Create a scroll area and set the layout
        scroll_area = QScrollArea()
        scroll_area.setStyleSheet(style_sheet.scroll_bar_style())
        scroll_area.setWidgetResizable(True)
        scroll_area.setMinimumWidth(250)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        scroll_widget = QWidget()
        scroll_widget.setLayout(layout)
        scroll_area.setWidget(scroll_widget)

        # Set the scroll area as the main widget
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(scroll_area)

        # Connect the controls
        self.fps_input.valueChanged.connect(self.fpsValueChanged.emit)
        self.frame_number_display.valueChanged.connect(self.displayframeChanged.emit)
        self.start_frame_input.valueChanged.connect(self.startframeValueChanged.emit)
        self.end_frame_input.valueChanged.connect(self.endframeValueChanged.emit)
        self.grid_rows_input.valueChanged.connect(self.gridrowValueChanged.emit)
        self.grid_columns_input.valueChanged.connect(self.gridcolumnValueChanged.emit)
        self.image_width_input.valueChanged.connect(self.imagewidthValueChanged.emit)
        self.image_height_input.valueChanged.connect(self.imageheightValueChanged.emit)
        self.use_grid_checkbox.stateChanged.connect(self.use_grid_checkboxStateChanged.emit)
        self.use_scale_checkbox.stateChanged.connect(self.use_scale_checkboxStateChanged.emit)
        play_button.clicked.connect(self.playClicked.emit)
        stop_button.clicked.connect(self.stopClicked.emit)

        self.console.append_text("INFO: Finished Loading Controls Widget.")

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


