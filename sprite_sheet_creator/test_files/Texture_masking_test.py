import os
from tkinter import Tk, Button, filedialog
from PIL import Image, ImageTk


class ImageProcessor:
    """
    Applies a mask to every image in a directory.
    """
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        self.image_directory = None
        self.mask_image_path = None

        self.import_button = Button(root, text="Import", command=self.select_image_directory)
        self.import_button.pack(pady=10)

        self.mask_button = Button(root, text="Mask", command=self.select_mask_image)
        self.mask_button.pack(pady=10)

        self.run_button = Button(root, text="Run", command=self.apply_masks_and_save)
        self.run_button.pack(pady=10)

    def select_image_directory(self):
        """
        selects the main image.
        """
        self.image_directory = filedialog.askdirectory(title="Select Image Directory")

    def select_mask_image(self):
        """
        select the mask image.
        """
        self.mask_image_path = filedialog.askopenfilename(title="Select Mask Image", filetypes=[("PNG files", "*.png")])

    def apply_masks_and_save(self):
        """
        set the mask as the transparent value for the alpha channel on the main image.
        """
        if self.image_directory is None or self.mask_image_path is None:
            print("Please select an image directory and a mask image.")
            return

        mask_image = Image.open(self.mask_image_path).convert("L")  # Convert to grayscale

        for filename in os.listdir(self.image_directory):
            if filename.endswith(".png"):
                image_path = os.path.join(self.image_directory, filename)
                image = Image.open(image_path)

                # Ensure both images have the same size
                mask_image = mask_image.resize(image.size)

                # Create alpha channel based on the mask
                alpha = mask_image.point(lambda p: p > 128 and 255)

                # Apply alpha channel to the image
                image.putalpha(alpha)

                # Save the result
                output_path = os.path.join(self.image_directory, f"masked_{filename}")
                image.save(output_path, "PNG")

        print("Masking process completed.")


if __name__ == "__main__":
    root = Tk()
    app = ImageProcessor(root)
    root.mainloop()
