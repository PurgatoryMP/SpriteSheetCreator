import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QDockWidget

from image_viewer_widget import ImageViewerWidget
from menu_bar_widget import create_menu_bar
from controls_widget import ControlWidget
from playback_widget import PlaybackWidget
from image_grid_widget import ImageSequenceWidget
from sprite_sheet_widget import SpriteSheetWidget
from status_bar_widget import StatusBar
from console_widget import ConsoleWidget
import style_sheet


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window title
        self.setWindowTitle("Super Sprite")

        self.setStyleSheet(style_sheet.dock_widget_style())
        self.setStyleSheet(style_sheet.main_window_style())

        self.setDockOptions(QMainWindow.AllowTabbedDocks |
                            QMainWindow.AllowNestedDocks)

        menu_bar = create_menu_bar()
        self.setMenuBar(menu_bar)

        status_bar = StatusBar()
        self.setStatusBar(status_bar)

        image_sequence_directory = r"G:\Models\2023\Unicorn Dance\ohyeah"
        file_path1 = r"G:\Models\2023\Unicorn Dance\ohyeah\image_sequence_0.png"

        d_console_widget = ConsoleWidget()
        console_dock_widget = QDockWidget("Console")
        console_dock_widget.setWidget(d_console_widget)
        console_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        console_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        control_widget = ControlWidget(d_console_widget)
        control_dock_widget = QDockWidget("Controls")
        control_dock_widget.setWidget(control_widget)
        control_dock_widget.setMinimumWidth(250)
        control_dock_widget.setMaximumWidth(265)
        control_dock_widget.setMaximumHeight(600)
        control_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        control_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        image_sequence_widget = ImageSequenceWidget(image_sequence_directory)
        image_sequence_dock_widget = QDockWidget("Image Sequence")
        image_sequence_dock_widget.setWidget(image_sequence_widget)
        image_sequence_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        image_sequence_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        image_viewer_widget = ImageViewerWidget(file_path1)
        image_viewer_dock_widget = QDockWidget("Image Viewer")
        image_viewer_dock_widget.setWidget(image_viewer_widget)
        image_viewer_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        image_viewer_dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        sprite_sheet_widget = SpriteSheetWidget(image_sequence_directory)
        sprite_sheet__dock_widget = QDockWidget("Sprite Sheet")
        sprite_sheet__dock_widget.setWidget(sprite_sheet_widget)
        sprite_sheet__dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        sprite_sheet__dock_widget.setStyleSheet(style_sheet.dock_widget_style())

        playback_widget = PlaybackWidget(image_sequence_directory, d_console_widget, control_widget)
        playback_widget_dock_widget = QDockWidget("Playback")
        playback_widget_dock_widget.setWidget(playback_widget)
        playback_widget_dock_widget.setAllowedAreas(Qt.DockWidgetArea.AllDockWidgetAreas)
        playback_widget_dock_widget.setStyleSheet(style_sheet.dock_widget_style())


        # add the widgets to the main window.
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, image_sequence_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, playback_widget_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, image_viewer_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, control_dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, sprite_sheet__dock_widget)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, console_dock_widget)

        d_console_widget.append_text("Finished loading widgets.")


if __name__ == "__main__":
    # Create the application instance
    app = QApplication(sys.argv)

    # Create and show the main window
    window = MainWindow()
    window.show()

    # Start the event loop
    sys.exit(app.exec_())
