import os
import shutil
import tempfile


import cv2
from PIL import Image
from PyQt5.QtGui import QImageReader
from PyQt5.QtWidgets import QFileDialog
from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.video.io.VideoFileClip import VideoFileClip


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

    def export_image_sequence(self, image_sequence: list) -> None:
        """
        Exports the image sequence to the defined directory.
        """
        try:
            if image_sequence:
                sequence_directory = QFileDialog.getExistingDirectory(caption="Select Sequence Directory.")
                if sequence_directory:

                    start = self.control.get_start_frame_value() - 1
                    if start <= 0:
                        start = 0
                    end = self.control.get_end_frame_value()

                    for index, image_filepath in enumerate(image_sequence[start:end]):
                        destination_filepath = os.path.join(sequence_directory, os.path.basename(image_filepath))

                        try:
                            shutil.copy(image_filepath, destination_filepath)
                        except FileNotFoundError:
                            self.console.append_text(f"ERROR: File not found: {image_filepath}")
                            continue

                self.console.append_text("INFO: Image Sequence Exported: {}".format(sequence_directory))
            else:
                self.console.append_text("Warning: Nothing to export.")

        except Exception as err:
            self.console.append_text("ERROR: export_image_sequence: {}".format(err.args))

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

    def export_as_gif(self, image_sequence: list) -> None:
        """
        Exports a gif of the image sequence.

        Args:
            image_sequence: (list): A collection of file paths to the frames of the image sequence.
        """
        try:
            start_frame = self.control.get_start_frame_value()
            end_frame = self.control.get_end_frame_value()
            filename = f"GifName_000.gif"

            # The image sequence
            sequence = image_sequence[start_frame:end_frame]

            # Open a file dialog to get the save file path
            save_path, _ = QFileDialog.getSaveFileName(
                caption="Save Gif file",
                directory=filename,
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
                                   #duration=10,  # Set the duration between frames (in milliseconds)
                                   fps=self.control.get_fps_value(),
                                   loop=0,
                                   disposal=2,
                                   background=255)
            else:
                print("WARNING: export_as_gif: Image sequence not provided.")
        except Exception as err:
            self.console.append_text("ERROR: export_as_gif: {}".format(err.args))


    def import_as_mp4(self) -> list:
        """
        Imports a .MP4 file and converts it to an image sequence.
        This MP4 may contain audio information. Maybe this can be re-used?
        """
        try:
            video_path, _ = QFileDialog.getOpenFileName(caption="Select Video File", filter="MP4 (*.mp4)")

            # Create the output directory if it doesn't exist
            output_dir = "{}/{}".format(self.temp_directory, "converted")

            if not os.path.exists(output_dir):
                os.makedirs(output_dir)

            if os.path.exists(output_dir) and os.path.isdir(output_dir):
                shutil.rmtree(output_dir)
                os.makedirs(output_dir)

            if video_path:
                video = VideoFileClip(video_path)
                frames = video.iter_frames()

                for i, frame in enumerate(frames):
                    image = Image.fromarray(frame)
                    file_name = f"{output_dir}/{i}.png"
                    image.save(file_name)
                    print(f"Saved: {file_name}")

            self.image_sequence = sorted([str(os.path.join(output_dir, filename)).replace("\\", "/") for filename in os.listdir(output_dir)], key=os.path.getctime)

            return self.image_sequence
        except Exception as err:
            self.console.append_text("ERROR: export_as_gif: {}".format(err.args))

    def export_as_mp4(self, image_sequence: list) -> None:
        """
        Exports the image sequence as an .mp4 file.
        """
        try:
            if image_sequence:
                fps = self.control.get_fps_value()
                codec = "mp4v"
                filename = "Movie_000.mp4"
                save_path, _ = QFileDialog.getSaveFileName(
                    caption="Save MP4 file",
                    directory=filename,
                    filter="MP4 Files (*.mp4)")

                if save_path:
                    # Get the image dimensions from the first image in the sequence
                    first_image = cv2.imread(image_sequence[0])
                    height, width, _ = first_image.shape

                    video_writer = cv2.VideoWriter(save_path, cv2.VideoWriter_fourcc(*codec), fps, (width, height))

                    for image_path in image_sequence:
                        frame = cv2.imread(image_path)
                        video_writer.write(frame)

                    video_writer.release()
            else:
                self.console.append_text("WARNING: No images to export.")
        except Exception as err:
            self.console.append_text("ERROR: export_as_mp4: {}".format(err.args))

    def export_as_webm(self, image_sequence: list) -> None:
        """
        exports the image sequence as a .webm file.
        """
        try:
            if image_sequence:
                fps = self.control.get_fps_value()
                codec = "libvpx-vp9"
                filename = "Webm_000.webm"  # Change the filename extension to .webm
                save_path, _ = QFileDialog.getSaveFileName(
                    caption="Save Webm file",
                    directory=filename,
                    filter="Webm Files (*.webm)")

                if save_path:
                    # Create a temporary directory to store the images
                    temp_dir = tempfile.mkdtemp()

                    # Copy the image_sequence to the temporary directory
                    for i, image_path in enumerate(image_sequence):
                        shutil.copy(image_path, os.path.join(temp_dir, f"frame_{i:04d}.png"))

                    # Create an ImageSequenceClip from the images in the temporary directory
                    image_sequence_clip = ImageSequenceClip(temp_dir, fps=fps)

                    # Save the clip as .webm using the specified codec
                    image_sequence_clip.write_videofile(save_path, codec=codec)

                    # Remove the temporary directory and its contents
                    shutil.rmtree(temp_dir)

        except Exception as err:
            self.console.append_text("ERROR: export_as_webm: {}".format(err.args))

    def save_script(self, name: str, script: str) -> None:
        """
        Saves the script to the specified directory.
        """
        try:
            if script:
                filename = "{}_Animation_Script.txt".format(name)
                save_path, _ = QFileDialog.getSaveFileName(
                    caption="Save text file",
                    directory=filename,
                    filter="Text Files (*.txt)")
                if save_path:
                    with open(save_path, "w") as file:
                        file.write(script)

        except Exception as err:
            self.console.append_text("ERROR: save_lsl_script_1_file: {}".format(err.args))
