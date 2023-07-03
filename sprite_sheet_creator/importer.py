import os
import tempfile
from pathlib import Path

from PIL.Image import Image
from PyQt5.QtGui import QImage
from PyQt5.QtWidgets import QFileDialog
from moviepy.video.io.VideoFileClip import VideoFileClip


class ImportExporter():
    def __init__(self, main_console_widget, control_widget):
        self.path = None
        self.console = main_console_widget
        self.console.append_text("INFO: Loading Import/Exporter functions.----------------")

        self.control = control_widget

        self.image_sequence = []

        self.console.append_text("INFO: Finished Loading Import/Exporter functions.")


    def import_image_sequence(self) -> list:
        """
        Imports an image sequence from a selected directory.
        """
        try:
            # Open file dialog to select directory
            directory = QFileDialog.getExistingDirectory()
            if directory:
                # Retrieve image files from the selected directory and sort them by creation time.
                # This keeps the frames in the correct order regardless of name.
                self.image_sequence = sorted([str(os.path.join(directory, filename)).replace("\\", "/") for filename in os.listdir(directory)], key=os.path.getctime)
                return self.image_sequence
        except Exception as err:
            self.console.append_text(str(err.args))

    def export_sprite_sheet(self, pixmap_image) -> None:
        """
        Save the sprite sheet image as a PNG file.

        The image is saved based on the provided parameters and user input.

        Returns:
            None
        """
        try:
            if pixmap_image:
                # Convert the pixmap of the sprite sheet widget to a QImage
                # sprite_sheet_image = QImage(pixmap_image.pixmap().toImage())

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
    #
    # def import_as_gif(self) -> None:
    #     """
    #     Imports a gif file and converts it to an image sequence.
    #     """
    #     gif_path, _ = QFileDialog.getOpenFileName(self, "Graphics Interchange Files", "", "Gif Files (*.gif)")
    #
    #     temp_dir = tempfile.mkdtemp(prefix='SSC_temp_', dir=tempfile.gettempdir())
    #     print(temp_dir)
    #
    #     if gif_path:
    #         # Convert gif to an image sequence
    #         gif = Image.open(gif_path)
    #         frames = []
    #         try:
    #             while True:
    #                 frames.append(gif.copy())
    #                 gif.seek(len(frames))  # Move to the next frame
    #         except EOFError:
    #             pass
    #
    #         for i, frame in enumerate(frames):
    #             output_path = f"{temp_dir}/{i}.png"
    #             frame.save(output_path, "PNG")
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
    # def export_as_gif(self) -> None:
    #     """
    #     exports a gif file which is the image sequence.
    #     """
    #     try:
    #         if self.image_sequence:
    #             images = []
    #             file_names = self.image_sequence[
    #                          int(self.start_frame_input.text()):int(self.end_frame_input.text()) + 1]
    #
    #             # print("\n".join(file_names))
    #
    #             for file_path in file_names:
    #                 print(file_path)
    #                 if os.path.exists(file_path):
    #                     try:
    #                         with Image.open(file_path) as image:
    #                             if image.mode != 'RGBA':
    #                                 image = image.convert('RGBA')
    #                             images.append(image.copy())
    #                     except IOError:
    #                         pass
    #
    #             if images:
    #                 save_path, _ = QFileDialog.getSaveFileName(self, "Save As",
    #                                                            f"Gif_{str(int(self.start_frame_input.text()) + int(self.end_frame_input.text()) + 1)}_{self.fps_input.text()}",
    #                                                            filter="GIF Files (*.gif)")
    #                 if save_path:
    #                     frame_duration = 1000 / int(self.fps_input.text())
    #                     print(frame_duration)
    #                     images[0].save(save_path,
    #                                    format='GIF',
    #                                    save_all=True,
    #                                    append_images=images[1:],
    #                                    duration=10,
    #                                    loop=0,
    #                                    disposal=2,
    #                                    background=255)
    #                     self.path = os.path.dirname(save_path)
    #                     self.open_dialog(self.path)
    #         else:
    #             print("Image sequence not provided.")
    #     except Exception as err:
    #         self.debug(str(err.args))
    #
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