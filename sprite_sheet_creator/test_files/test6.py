from PySide2 import QtCore, QtWidgets, QtGui

class MayaLogViewer(QtWidgets.QMainWindow):
    def __init__(self):
        super(MayaLogViewer, self).__init__()

        # Set up the main window
        self.setWindowTitle("Maya Log Viewer")
        self.resize(800, 600)

        # Create the dockable widget
        self.log_widget = LogWidget()
        dock_widget = QtWidgets.QDockWidget("Maya Logs", self)
        dock_widget.setWidget(self.log_widget)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock_widget)


class LogWidget(QtWidgets.QWidget):
    def __init__(self):
        super(LogWidget, self).__init__()

        # Create the table view for Maya logs
        self.table_view = QtWidgets.QTableView(self)
        self.table_view.setSortingEnabled(True)  # Enable sorting by creation date

        # Set up the table model
        self.model = QtGui.QStandardItemModel(self)
        self.model.setHorizontalHeaderLabels(["Log File Name", "Creation Date"])
        self.load_logs()  # Load Maya logs into the table model

        # Set the table model for the table view
        self.table_view.setModel(self.model)

        # Set the layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.table_view)

    def load_logs(self):
        import os
        import glob
        import tempfile

        # Define the Maya log directory
        log_dir = os.path.join(tempfile.gettempdir(), "Maya")

        # Get a list of log files
        log_files = glob.glob(os.path.join(log_dir, "Maya*.log"))

        # Sort log files by creation date
        log_files = sorted(log_files, key=os.path.getctime)

        # Populate the table model with log file names and creation dates
        for log_file in log_files:
            file_name = os.path.basename(log_file)
            creation_date = QtCore.QDateTime.fromSecsSinceEpoch(os.path.getctime(log_file))
            creation_date_string = creation_date.toString("yyyy-MM-dd hh:mm:ss")
            self.model.appendRow([
                QtGui.QStandardItem(file_name),
                QtGui.QStandardItem(creation_date_string)
            ])


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    main_window = MayaLogViewer()
    main_window.show()
    app.exec_()
