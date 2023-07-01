from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
import style_sheet

class FileTableWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Set up the layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create the table view
        self.table_widget = QTableWidget(self)
        self.table_widget.setStyleSheet(style_sheet.table_widget_style())
        layout.addWidget(self.table_widget)

        # Set the header
        self.set_header()

    def set_header(self):
        """
        Sets the header at the top of the table.
        """
        header_labels = ["Created At:", "File Name:", "File Path:", "File Size:", "Width", "Height", "Bit Depth"]
        self.table_widget.setColumnCount(len(header_labels))
        self.table_widget.setHorizontalHeaderLabels(header_labels)

    def append_data(self, creation_time, file_name, file_path, file_size, image_width, image_height, image_depth):
        """
        Adds an entry to the table.
        """
        row_count = self.table_widget.rowCount()
        self.table_widget.insertRow(row_count)

        # Fill data in the new row
        self.table_widget.setItem(row_count, 0, QTableWidgetItem(str(creation_time)))
        self.table_widget.setItem(row_count, 1, QTableWidgetItem(str(file_name)))
        self.table_widget.setItem(row_count, 2, QTableWidgetItem(str(file_path)))
        self.table_widget.setItem(row_count, 3, QTableWidgetItem(str(file_size)))
        self.table_widget.setItem(row_count, 4, QTableWidgetItem(str(image_width)))
        self.table_widget.setItem(row_count, 5, QTableWidgetItem(str(image_height)))
        self.table_widget.setItem(row_count, 6, QTableWidgetItem(str(image_depth)))

        # Resize rows to fit content
        self.table_widget.resizeColumnsToContents()

    def clear_data(self):
        """
        Removes all data from the table except the header.
        """
        self.table_widget.clearContents()
        self.table_widget.setRowCount(0)
