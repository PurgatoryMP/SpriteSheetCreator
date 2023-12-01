from PyQt5.QtWidgets import QFileDialog


class DirectConverter:
    """
    Provide options for the user to directly convert from one media type to another.
    """

    # TODO: When the user selects one of the options from the main menu a prompt will appear with options for converting
    #  that type of content, the idea being that the user can convert a sequence to a video directly or a gif or a webm
    #  and vise versa.

    def __init__(self, main_console_widget):
        super().__init__()

        # Add the console widget.
        self.console = main_console_widget
        self.console.append_text("INFO: Converter Loaded.")

    def convert_image(self):
        """
        Prompts the user with options to convert a selected image to another type of image format.
        """
        try:
            print("convert_image working")

            p = self.get_file_path()
            print("path: {}".format(p))

        except Exception as err:
            print(err.args)
            self.console.append_text("ERROR: convert_image: {}".format(err.args))

    def convert_sequence(self):
        """
        prompts the user with options to convert the directory of images to another format.
        """
        try:
            print("convert_sequence working")

        except Exception as err:
            print(err.args)
            self.console.append_text("ERROR: convert_sequence: {}".format(err.args))

    def convert_video(self):
        """
        Prompts the user with options to convert a selected video to another type of video format.
        """
        try:
            print("convert_video working")

        except Exception as err:
            print(err.args)
            self.console.append_text("ERROR: convert_video: {}".format(err.args))

    def convert_gif(self):
        """
        Prompts the user with options to convert a selected gif to another type of video or animated image format.
        """
        try:
            print("convert_gif working")

        except Exception as err:
            print(err.args)
            self.console.append_text("ERROR: convert_gif: {}".format(err.args))

    def convert_web(self):
        """
        Prompts the user with options to convert a selected webm image to another type of web image format.
        """
        try:
            print("convert_web working")

        except Exception as err:
            print(err.args)
            self.console.append_text("ERROR: convert_web: {}".format(err.args))

    def convert_icon(self):
        """
        Prompts the user with options to convert a selected image to an icon image format.
        """
        try:
            print("convert_icon working")

        except Exception as err:
            print(err.args)
            self.console.append_text("ERROR: convert_icon: {}".format(err.args))

    def get_file_path(self) -> str:
        """
        Open a file dialog for selecting a file.

        Returns: (str): The file path of the selected file.

        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(None, "Select File", "", "All Files (*);;Text Files (*.txt)",
                                                   options=options)
        return file_path

    def get_directory_path(self) -> str:
        """
        Open a directory dialog for selecting a directory.

        Returns: (str): The directory path of the selected directory.
        """
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_dialog = QFileDialog()
        directory_path = file_dialog.getExistingDirectory(None, "Select Directory", "", options=options)
        return directory_path
