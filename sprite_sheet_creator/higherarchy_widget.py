from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem
import style_sheet

class FileTableWidget(QWidget):
    def __init__(self, main_console_widget):
        """
        Initializes the user interface of the widget.
        """
        super().__init__()

        self.console = main_console_widget

        # Set up the layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        # Create the table view
        self.table_widget = QTableWidget(self)
        self.table_widget.setStyleSheet(style_sheet.table_widget_style())
        layout.addWidget(self.table_widget)

        # Set the header
        self.set_header()

        self.console.append_text("INFO: Table Widget Loaded.")

    def set_header(self):
        """
        Sets the header at the top of the table.
        """
        try:
            header_labels = ["Created At:", "File Name:", "File Path:", "File Size:", "Width", "Height", "Bit Depth"]
            self.table_widget.setColumnCount(len(header_labels))
            self.table_widget.setHorizontalHeaderLabels(header_labels)
        except Exception as err:
            self.console.append_text("ERROR: set_header: {}".format(err.args))

    def append_data(self, creation_time, file_name, file_path, file_size, image_width, image_height, image_depth) -> None:
        """
        Adds an entry to the table.

        Args:
            creation_time (str): The creation time of the file.
            file_name (str): The name of the file.
            file_path (str): The path of the file.
            file_size (int): The size of the file in bytes.
            image_width (int): The width of the image in pixels.
            image_height (int): The height of the image in pixels.
            image_depth (int): The bit depth of the image.

        Returns:
            None
        """
        try:
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
        except Exception as err:
            self.console.append_text("ERROR: append_data: {}".format(err.args))

    def clear_data(self) -> None:
        """
        Removes all data from the table except the header.

        Returns:
            None
        """
        try:
            self.table_widget.clearContents()
            self.table_widget.setRowCount(0)
        except Exception as err:
            self.console.append_text("ERROR: clear_data: {}".format(err.args))
