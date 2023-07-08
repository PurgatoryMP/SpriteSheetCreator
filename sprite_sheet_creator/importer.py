import os
import shutil
import tempfile
from pathlib import Path

from PyQt5.QtCore import Qt, QByteArray, QSize
from PyQt5.QtGui import QImage, QImageReader, QMovie, QPixmap, QImageWriter
from PyQt5.QtWidgets import QFileDialog
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image


class ImportExporter():
    def __init__(self, main_console_widget, control_widget):
        self.path = None
        self.console = main_console_widget
        self.console.append_text("INFO: Loading Import/Exporter functions.----------------")

        self.control = control_widget

        self.image_sequence = []

        self.temp_directory = "{}/{}".format(tempfile.gettempdir(), "SuperSprite_Temp")
        if not os.path.exists(self.temp_directory):
            os.mkdir(self.temp_directory)

        self.console.append_text("INFO: Finished Loading Import/Exporter functions.")

    def clean_up_temp_directory(self) -> None:
        """
        Deletes the temp directory for this tool.
        """
        try:
            if os.path.exists(self.temp_directory) and os.path.isdir(self.temp_directory):
                shutil.rmtree(self.temp_directory)
        except Exception as err:
            print(err.args)
            self.console.append_text("ERROR: clean_up_temp_directory: {}".format(err.args))

    def import_image_sequence(self) -> list:
        """
        Imports an image sequence from a selected directory.
        """
        try:
            # Open file dialog to select directory
            directory = QFileDialog.getExistingDirectory(caption="Select Sequence Directory.")
            if directory:
                # Retrieve image files from the selected directory and sort them by creation time.
                # This keeps the frames in the correct order regardless of name.
                self.image_sequence = sorted([str(os.path.join(directory, filename)).replace("\\", "/") for filename in os.listdir(directory)], key=os.path.getctime)
                return self.image_sequence
        except Exception as err:
            self.console.append_text("ERROR: import_image_sequence: {}".format(err.args))

    def export_sprite_sheet(self, pixmap_image) -> None:
        """
        Save the sprite sheet image as a PNG file.

        The image is saved based on the provided parameters and user input.

        Returns:
            None
        """
        try:
            if pixmap_image:
                # Calculate the number of rows and columns in the sprite sheet
                num_rows = self.control.get_grid_rows_value()
                num_columns = self.control.get_grid_columns_value()

                # Calculate the frame range and frames per second (fps)
                frame_range = self.control.get_end_frame_value() - self.control.get_start_frame_value()

                fps = self.control.get_fps_value()

                # Generate the filename based on the parameters
                filename = f"SheetName_000_{num_rows}_{num_columns}_{frame_range}_{fps}.png"

                # Open a file dialog to get the save file path
                file_path, _ = QFileDialog.getSaveFileName(caption=filename, directory=filename, filter="PNG Image (*.png)")
                if file_path:
                    # Save the sprite sheet image to the specified file path
                    pixmap_image.save(file_path)

                    # open a popup dialog with a button the user can click to open the output directory in the file explorer.
                    self.path = os.path.dirname(file_path)
                    os.startfile(self.path)

        except Exception as err:
            self.console.append_text("ERROR: export_sprite_sheet: {}".format(err.args))

    def import_as_gif(self) -> list:
        """
        Imports a gif file and converts it to an image sequence.
        """
        try:
            converted_path = []
            gif_path, _ = QFileDialog.getOpenFileName(caption="Graphics Interchange Files", filter="Gif Files (*.gif)")

            # Load the GIF file using QImageReader
            gif_reader = QImageReader(gif_path)
            gif_reader.setDecideFormatFromContent(True)
            frame_count = gif_reader.imageCount()

            # Create the output directory if it doesn't exist
            output_dir = "{}/{}".format(self.temp_directory, "converted")

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            if os.path.exists(output_dir) and os.path.isdir(output_dir):
                shutil.rmtree(output_dir)
                os.makedirs(output_dir)

            # Iterate over each frame of the GIF and save as separate images
            for frame_index in range(frame_count):
                gif_reader.jumpToImage(frame_index)
                image = gif_reader.read()

                # Generate the output file path for the current frame
                output_path = os.path.join(output_dir, f"{frame_index}.png")

                # Save the image as PNG
                image.save(output_path)
                converted_path.append(output_path.replace("\\", "/"))

                print(f"Frame {frame_index} saved as {output_path}")

            self.image_sequence = converted_path
            return self.image_sequence
        except Exception as err:
            self.console.append_text("ERROR: import_as_gif: {}".format(err.args))

    from PyQt5.QtWidgets import QFileDialog
    from PyQt5.QtGui import QMovie, QImage, QPainter
    from PyQt5.QtCore import Qt
    import os

    from PyQt5.QtWidgets import QFileDialog
    from PyQt5.QtGui import QMovie, QPixmap
    from PyQt5.QtCore import Qt
    import os

    from PyQt5.QtWidgets import QFileDialog
    from PyQt5.QtGui import QImageWriter
    import os

    def export_as_gif(self, image_sequence) -> None:
        """
        Exports a gif of the image sequence.

        Args:
            image_sequence: (list): A collection of file paths to the frames of the image sequence.
        """
        try:
            start_frame = self.control.get_start_frame_value()
            end_frame = self.control.get_end_frame_value()

            # Calculate the number of rows and columns in the sprite sheet
            # num_rows = self.control.get_grid_rows_value()
            # num_columns = self.control.get_grid_columns_value()

            # Calculate the frame range and frames per second (fps)
            # frame_range = end_frame - start_frame

            # fps = self.control.get_fps_value()
            filename = f"GifName_000.gif"

            # The image sequence
            sequence = image_sequence[start_frame:end_frame]

            # Open a file dialog to get the save file path
            save_path, _ = QFileDialog.getSaveFileName(caption="Save Gif file", directory=filename,
                                                       filter="GIF Files (*.gif)")

            if save_path and sequence:
                images = []
                for file_path in sequence:
                    if os.path.exists(file_path):
                        image = Image.open(file_path)
                        images.append(image)

                if images:
                    images[0].save(save_path,
                                   format='GIF',
                                   save_all=True,
                                   append_images=images[1:],
                                   duration=100,  # Set the duration between frames (in milliseconds)
                                   loop=0,
                                   disposal=2,
                                   background=255)
            else:
                print("WARNING: export_as_gif: Image sequence not provided.")
        except Exception as err:
            self.console.append_text("ERROR: export_as_gif: {}".format(err.args))


    # def import_as_mp4(self) -> None:
    #     """
    #     Imports a .MP4 file and converts it to an image sequence.
    #     This MP4 may contain audio information. Maybe this can be re-used?
    #     """
    #     video_path, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4)")
    #
    #     temp_dir = tempfile.mkdtemp(prefix='SSC_temp_', dir=tempfile.gettempdir())
    #     print(temp_dir)
    #
    #     if video_path:
    #         video = VideoFileClip(video_path)
    #         frames = video.iter_frames()
    #
    #         for i, frame in enumerate(frames):
    #             image = Image.fromarray(frame)
    #             file_name = f"{temp_dir}/{i}.png"
    #             image.save(file_name)
    #             print(f"Saved: {file_name}")
    #
    #         image_files = list(Path(temp_dir).glob("*.png")) + list(Path(temp_dir).glob("*.jpg"))
    #         self.image_sequence = [os.path.join(temp_dir, file) for file in image_files]
    #
    #         self.image_sequence.sort()
    #         print("\n".join(self.image_sequence))
    #
    #         self.populate_widgets(self.image_sequence)
    #         print("import_as_gif")
    #
    # def export_as_mp4(self) -> None:
    #     """
    #     exports the image sequence as a .mp4 file.
    #     """
    #     try:
    #         if self.image_sequence:
    #             save_path, _ = QFileDialog.getSaveFileName(self, "Save As",
    #                                                        f"Movie_{str(int(self.start_frame_input.text()) + int(self.end_frame_input.text()) + 1)}_{self.fps_input.text()}",
    #                                                        filter="MP4 Image (*.mp4)")
    #
    #             if save_path:
    #                 clip = mp.ImageSequenceClip(self.image_sequence, fps=int(self.fps_input.text()))
    #                 clip.write_videofile(save_path, codec="libx264")
    #
    #                 # open a popup dialog with a button the user can click to open the output directory in the file explorer.
    #                 self.path = os.path.dirname(save_path)
    #                 self.open_dialog(self.path)
    #     except Exception as err:
    #         self.debug(str(err.args))
    #
    # def export_as_webm(self):
    #     """
    #             exports the image sequence as a .mp4 file.
    #             """
    #     try:
    #         if self.image_sequence:
    #             save_path, _ = QFileDialog.getSaveFileName(self, "Save As",
    #                                                        f"Webm_{str(int(self.start_frame_input.text()) + int(self.end_frame_input.text()) + 1)}_{self.fps_input.text()}",
    #                                                        filter="WEBM Image (*.webm)")
    #
    #             if save_path:
    #                 clip = mp.ImageSequenceClip(self.image_sequence, fps=int(self.fps_input.text()))
    #                 clip.write_videofile(save_path, codec="libvpx-vp9")
    #
    #                 # open a popup dialog with a button the user can click to open the output directory in the file explorer.
    #                 self.path = os.path.dirname(save_path)
    #                 self.open_dialog(self.path)
    #     except Exception as err:
    #         self.debug(str(err.args))
    #
    # def convert_gif_to_Sequence(self) -> None:
    #     """
    #     imports a gif file and then converts it to an image sequence saving it out to a user defined directory.
    #     """
    #     video_path, _ = QFileDialog.getOpenFileName(self, "Graphics Interchange Files", "", "Gif Files (*.gif)")
    #
    #     if video_path:
    #         # Convert gif to an image sequence
    #         gif = Image.open(video_path)
    #         frames = []
    #         try:
    #             while True:
    #                 frames.append(gif.copy())
    #                 gif.seek(len(frames))  # Move to the next frame
    #         except EOFError:
    #             pass
    #
    #         # Select output directory
    #         output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
    #
    #         # Save the image sequence to the selected directory
    #         for i, frame in enumerate(frames):
    #             output_path = f"{output_dir}/image_sequence_{i}.png"
    #             frame.save(output_path, "PNG")
    #
    #     # open a popup dialog with a button the user can click to open the output directory in the file explorer.
    #     self.path = output_dir
    #     self.open_dialog(self.path)
    #
    #
    #
    #
    # def convert_mp4_to_Sequence(self) -> None:
    #     """
    #     imports a .MP4 file and then converts it to an image sequence saving it out to a user defined directory.
    #     """
    #     video_path, _ = QFileDialog.getOpenFileName(self, "Select Video", "", "Video Files (*.mp4)")
    #
    #     if video_path:
    #         video = VideoFileClip(video_path)
    #         frames = video.iter_frames()
    #
    #         output_dir = QFileDialog.getExistingDirectory(self, "Select Output Directory")
    #
    #         if output_dir:
    #             for i, frame in enumerate(frames):
    #                 image = Image.fromarray(frame)
    #                 file_name = f"{output_dir}/image_sequence_{i}.png"
    #                 image.save(file_name)
    #                 self.console(f"Saved: {file_name}")
    #
    #     # open a popup dialog with a button the user can click to open the output directory in the file explorer.
    #     self.path = output_dir
    #     self.open_dialog(self.path)