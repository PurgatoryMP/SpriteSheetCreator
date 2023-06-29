import os
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget

from image_viewer_widget import ImageViewerWidget
from menu_bar_widget import MenuBar
from controls_widget import ControlWidget
from playback_widget import PlaybackWidget
from image_grid_widget import ImageSequenceWidget
from sprite_sheet_widget import SpriteSheetWidget
from status_bar_widget import StatusBar
from console_widget import ConsoleWidget
from importer import ImportExporter
import style_sheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title
        self.image_sequence = None
        self.setWindowTitle("Super Sprite")
        self.resize(1200, 800)

        # Define main window and docked widget style sheets
        self.setStyleSheet(style_sheet.dock_widget_style())
        self.setStyleSheet(style_sheet.main_window_style())

        # Define dock options
        self.setDockOptions(QMainWindow.AllowTabbedDocks |
                            QMainWindow.AllowNestedDocks)

        # Define the console first so we can print out messages to it while loading other widgets.
        self.main_console_widget = ConsoleWidget()
        console_dock_widget = QDockWidget("Console")
        console_dock_widget.setWidget(self.main_console_widget)
        console_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        console_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        # Define the controls so we can add them to the other widgets
        self.control_widget = ControlWidget(self.main_console_widget)
        control_dock_widget = QDockWidget("Controls")
        control_dock_widget.setWidget(self.control_widget)
        control_dock_widget.setMinimumWidth(250)
        control_dock_widget.setMaximumWidth(300)
        control_dock_widget.setMaximumHeight(600)
        control_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        control_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        self.image_sequence_widget = ImageSequenceWidget(self.control_widget, self.main_console_widget)
        image_sequence_dock_widget = QDockWidget("Image Sequence")
        image_sequence_dock_widget.setWidget(self.image_sequence_widget)
        image_sequence_dock_widget.setMaximumHeight(300)
        image_sequence_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        image_sequence_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        self.image_viewer_widget = ImageViewerWidget(self.main_console_widget)
        image_viewer_dock_widget = QDockWidget("Image Viewer")
        image_viewer_dock_widget.setWidget(self.image_viewer_widget)
        image_viewer_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        image_viewer_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        self.sprite_sheet_widget = SpriteSheetWidget(self.main_console_widget, self.control_widget)
        sprite_sheet_dock_widget = QDockWidget("Sprite Sheet")
        sprite_sheet_dock_widget.setWidget(self.sprite_sheet_widget)
        sprite_sheet_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        sprite_sheet_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        self.playback_widget = PlaybackWidget(self.main_console_widget, self.control_widget)
        playback_widget_dock_widget = QDockWidget("Playback")
        playback_widget_dock_widget.setWidget(self.playback_widget)
        playback_widget_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        playback_widget_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        # Setup the menu bar
        menu_bar = MenuBar(self.main_console_widget)
        menu_bar.import_image_sequence.connect(self.import_image_sequence)
        menu = menu_bar.create_menu_bar()
        self.setMenuBar(menu)

        # Set up the status bar
        self.menu_bar = MenuBar(self.main_console_widget)
        self.menu_bar.import_image_sequence.connect(self.import_image_sequence)  # Connect the signal using instance
        menu = self.menu_bar.create_menu_bar()
        self.setMenuBar(menu)

        # Connect the controls here
        self.control_widget.fpsValueChanged.connect(self.playback_widget.set_fps_value)
        # control_widget.startframeValueChanged.connect(playback_widget.set_fps_value)
        # control_widget.endframeValueChanged.connect(playback_widget.set_fps_value)

        self.control_widget.gridrowValueChanged.connect(self.sprite_sheet_widget.update_sprite_sheet)
        self.control_widget.gridcolumnValueChanged.connect(self.sprite_sheet_widget.update_sprite_sheet)
        self.control_widget.imagewidthValueChanged.connect(self.sprite_sheet_widget.update_sprite_sheet)
        self.control_widget.imageheightValueChanged.connect(self.sprite_sheet_widget.update_sprite_sheet)

        self.control_widget.playClicked.connect(self.playback_widget.start_playback)
        self.control_widget.stopClicked.connect(self.playback_widget.stop_playback)
        # self.image_sequence_widget.imageClicked.connect(self.barf)
        self.image_sequence_widget.imageClicked.connect(self.handle_image_clicked)

        # add the widgets to the main window.
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, image_sequence_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, playback_widget_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, image_viewer_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, control_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, sprite_sheet_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, console_dock_widget)

        self.main_console_widget.append_text("Finished loading widgets.\n")

    def handle_image_clicked(self, image_path):
        try:
            if image_path:
                self.image_viewer_widget.set_select_image(image_path)
        except Exception as err:
            self.main_console_widget.append_text(str(err.args))

    def handle_image_path_clicked(self, image_path):
        os.startfile(image_path)

    def import_image_sequence(self):
        # Implement the logic to import the image sequence here
        importer = ImportExporter(self.main_console_widget)

        self.image_sequence = importer.import_image_sequence()
        self.main_console_widget.append_text("image_sequence Loaded.")

        self.image_sequence_widget.load_sequence(self.image_sequence)
        self.main_console_widget.append_text("image_sequence_widget Loaded.")

        self.image_viewer_widget.load_image(self.image_sequence, 0)
        self.main_console_widget.append_text("image_viewer_widget Loaded.")

        self.playback_widget.load_image_sequence(self.image_sequence)
        self.main_console_widget.append_text("playback_widget Loaded.")

        self.sprite_sheet_widget.load_images(self.image_sequence)
        self.main_console_widget.append_text("sprite_sheet_widget Loaded.")


if __name__ == "__main__":
    # Create the application instance
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Start the event loop
    sys.exit(app.exec_())
