from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QLabel, QSpinBox, QHBoxLayout, QPushButton, QVBoxLayout, QWidget, QScrollArea, \
    QFrame

import style_sheet


class ControlWidget(QWidget):

    fpsValueChanged = pyqtSignal(int)
    startframeValueChanged = pyqtSignal(int)
    endframeValueChanged = pyqtSignal(int)
    gridrowValueChanged = pyqtSignal(int)
    gridcolumnValueChanged = pyqtSignal(int)
    playClicked = pyqtSignal()
    stopClicked = pyqtSignal()

    def __init__(self, control_widget):
        super().__init__()

        console = control_widget
        console.append_text("Loading: Controls Widget.\n")

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
        self.start_frame_input.setStyleSheet(style_sheet.spinbox_style())
        # set the initial value for the start frame to 0
        self.start_frame_input.setValue(0)

        # Set up the end frame controls.
        end_frame_label = QLabel("End Frame:")
        end_frame_label.setStyleSheet(style_sheet.bubble_label_style())
        self.end_frame_input = QSpinBox()
        self.end_frame_input.setStyleSheet(style_sheet.spinbox_style())

        # Set up the FPS controls.
        fps_label = QLabel("Playback FPS:")
        fps_label.setStyleSheet(style_sheet.bubble_label_style())
        self.fps_input = QSpinBox()
        self.fps_input.setStyleSheet(style_sheet.spinbox_style())
        # set the initial value for the fps to 30
        self.fps_input.setValue(30)

        # Set up the image grid controls.
        grid_rows_label = QLabel("Grid Rows:")
        grid_rows_label.setStyleSheet(style_sheet.bubble_label_style())
        self.grid_rows_input = QSpinBox()
        self.grid_rows_input.setStyleSheet(style_sheet.spinbox_style())
        self.grid_rows_input.setValue(8)

        grid_columns_label = QLabel("Grid Columns:")
        grid_columns_label.setStyleSheet(style_sheet.bubble_label_style())
        self.grid_columns_input = QSpinBox()
        self.grid_columns_input.setStyleSheet(style_sheet.spinbox_style())
        self.grid_columns_input.setValue(8)

        # Set up the image size controls.
        image_width_label = QLabel("Image Width:")
        image_width_label.setStyleSheet(style_sheet.bubble_label_style())
        self.image_width_input = QSpinBox()
        self.image_width_input.setStyleSheet(style_sheet.spinbox_style())

        image_height_label = QLabel("Image Height:")
        image_height_label.setStyleSheet(style_sheet.bubble_label_style())
        self.image_height_input = QSpinBox()
        self.image_height_input.setStyleSheet(style_sheet.spinbox_style())
        # Set the default sprite sheet size.
        self.image_width_input.setValue(2048)
        self.image_height_input.setValue(2048)

        # Set the controls for the frame number output
        frame_number_label = QLabel("Frame Number:")
        frame_number_label.setStyleSheet(style_sheet.bubble_label_style())
        self.frame_number_display = QSpinBox()
        self.frame_number_display.setStyleSheet(style_sheet.spinbox_style())
        # set the initial value for the Frame Number to 0
        self.frame_number_display.setValue(0)

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

        controls = [
            (play_button, stop_button),
            (separator1, separator2),
            (frame_number_label, self.frame_number_display),
            (fps_label, self.fps_input),
            (separator3, separator4),
            (start_frame_label, self.start_frame_input),
            (end_frame_label, self.end_frame_input),
            (separator5, separator6),
            (grid_rows_label, self.grid_rows_input),
            (grid_columns_label, self.grid_columns_input),
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

        self.fps_input.valueChanged.connect(self.fpsValueChanged.emit)
        self.start_frame_input.valueChanged.connect(self.startframeValueChanged.emit)
        self.end_frame_input.valueChanged.connect(self.endframeValueChanged.emit)
        self.grid_rows_input.valueChanged.connect(self.gridrowValueChanged.emit)
        self.grid_columns_input.valueChanged.connect(self.gridcolumnValueChanged.emit)

        play_button.clicked.connect(self.playClicked.emit)
        stop_button.clicked.connect(self.stopClicked.emit)

        console.append_text("Finished Loading: Controls Widget.\n")

    def update_frame_number(self, value: int):
        """Updates the control value."""
        self.frame_number_display.setValue(value)

    def get_fps_value(self) -> int:
        value = self.fps_input.value()
        return value

    def get_start_frame_value(self) -> int:
        value = self.start_frame_input.value()
        return value

    def get_end_frame_value(self) -> int:
        value = self.end_frame_input.value()
        return value

    def get_grid_rows_value(self) -> int:
        value = self.grid_rows_input.value()
        return value

    def get_grid_columns_value(self) -> int:
        value = self.grid_columns_input.value()
        return value

