import os
import sys
from PyQt5.QtCore import Qt, QTimer, QSize
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
import psutil


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

        # Define the controls, so we can add them to the other widgets
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

        # # Setup the menu bar
        self.menu_bar = MenuBar(self.main_console_widget)
        # Connect the menu bar signal using instance
        self.menu_bar.importimagesequence.connect(self.import_image_sequence)

        # TODO: Plugin the functions for these menu options
        # self.menu_bar.importgiffile.connect(self.import_image_sequence)
        # self.menu_bar.exportgiffile.connect(self.import_image_sequence)
        # self.menu_bar.convertgiftosequence.connect(self.import_image_sequence)
        # self.menu_bar.importmp4file.connect(self.import_image_sequence)
        # self.menu_bar.exportmp4file.connect(self.import_image_sequence)
        # self.menu_bar.convertmp4tosequence.connect(self.import_image_sequence)

        self.menu_bar.exitapp.connect(self.exit_application)

        # Add the menu bar to the main window
        menu = self.menu_bar.create_menu_bar()
        self.setMenuBar(menu)

        # Set up the status bar
        self.statusBar = StatusBar(self.main_console_widget)
        self.setStatusBar(self.statusBar)

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
        self.image_sequence_widget.imageClicked.connect(self.handle_image_clicked)

        self.image_viewer_widget.imagepathClicked.connect(self.open_file_path)

        # add the widgets to the main window.
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, image_sequence_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, playback_widget_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, image_viewer_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, control_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, sprite_sheet_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, console_dock_widget)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.get_memory_usage)
        self.timer.start(1000)

        self.resize_timer = QTimer()
        self.resize_timer.setInterval(500)  # Set the delay in milliseconds
        self.resize_timer.setSingleShot(True)
        self.resize_timer.timeout.connect(self.report_size)

        self.main_console_widget.append_text("Finished loading widgets.\n")

    def open_file_path(self, file_path):
        if file_path:
            directory = os.path.dirname(file_path)
            if directory:
                os.startfile(directory)


    def handle_image_clicked(self, image_path):
        try:
            if image_path:
                self.image_viewer_widget.set_select_image(image_path)
        except Exception as err:
            self.main_console_widget.append_text(str(err.args))

    def handle_image_path_clicked(self, image_path):
        if image_path:
            try:
                os.startfile(image_path)
            except Exception as err:
                self.main_console_widget.append_text(str(err.args))

    def import_image_sequence(self):
        # Implement the logic to import the image sequence here
        # Populate the widgets with the images contained in the selected directory

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

    def get_memory_usage(self):
        try:
            # Get the current process ID
            pid = psutil.Process()

            # Get the memory information
            memory_info = pid.memory_full_info()

            # Memory usage in bytes
            memory_usage = memory_info.uss

            # Convert to a human-readable format
            memory_usage_readable = psutil._common.bytes2human(memory_usage)

            # Display memory usage
            self.statusBar.set_mem_usage_text(str(memory_usage_readable))
        except Exception as err:
            self.main_console_widget.append_text(str(err.args))

    def resizeEvent(self, event):
        # Call the base class resizeEvent method
        super().resizeEvent(event)
        # Start or restart the resize timer
        self.resize_timer.start()

    def report_size(self):
        # Get the new size of the main window
        # new_size = self.size()
        # print(f"New size: {new_size.width()} x {new_size.height()}")

        # After the window has been resized, fit the images to the new widget size.
        self.sprite_sheet_widget.fit_to_widget()
        self.image_viewer_widget.fit_to_widget()

    def exit_application(self):
        self.close()


if __name__ == "__main__":
    # Create the application instance
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Start the event loop
    sys.exit(app.exec_())
