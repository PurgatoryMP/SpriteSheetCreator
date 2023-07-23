import os
import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTreeView, QTextEdit, QSplitter, QVBoxLayout, QWidget, QFileSystemModel, QStandardItemModel, QHeaderView
from PyQt5.QtCore import Qt, QDir, QModelIndex, QStandardItem


class LogViewerModel(QFileSystemModel):
    def __init__(self):
        super().__init__()
        self.root_path = os.path.join(os.getenv("LOCALAPPDATA"), "Temp")
        self.setRootPath(self.root_path)

    def data(self, index, role):
        if role == Qt.DisplayRole:
            file_path = self.filePath(index)
            if os.path.isdir(file_path):
                return super().data(index, role)
            elif os.path.isfile(file_path) and "Maya" in os.path.dirname(file_path) and file_path.endswith(".log"):
                return os.path.basename(file_path)

        return super().data(index, role)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Tree List View and Text Editor")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget and layout
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        # Create a splitter to hold the Tree ListView and Text Editor
        splitter = QSplitter(self)
        layout.addWidget(splitter)

        # Create the Tree ListView
        tree_view = QTreeView(self)
        self.log_viewer_model = LogViewerModel()
        tree_view.setModel(self.log_viewer_model)
        tree_view.setRootIndex(self.log_viewer_model.index(self.log_viewer_model.root_path))
        tree_view.expandAll()

        # Add custom headers to the TreeView
        header_model = QStandardItemModel(1, 1)
        header_model.setHorizontalHeaderItem(0, QStandardItem("Files"))
        tree_view.setHeader(QHeaderView(Qt.Horizontal))
        tree_view.header().setModel(header_model)

        tree_view.clicked.connect(self.show_log_content)
        splitter.addWidget(tree_view)

        # Create the Text Editor
        self.text_editor = QTextEdit(self)
        splitter.addWidget(self.text_editor)

    def show_log_content(self, index):
        file_path = self.log_viewer_model.filePath(index)
        if os.path.isfile(file_path):
            with open(file_path, "r") as log_file:
                log_content = log_file.read()
                self.text_editor.setPlainText(log_content)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
