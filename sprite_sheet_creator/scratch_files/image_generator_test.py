from PIL import Image
import os


def create_sprite_sheet(directory_path):
    # Create a new blank image with transparency
    sprite_sheet = Image.new("RGBA", (2048, 2048), (0, 0, 0, 0))

    # Get a list of image file names in the directory
    image_files = [file for file in os.listdir(directory_path) if
                   file.lower().endswith((".png", ".jpg", ".jpeg", ".gif"))]

    # Sort the image files alphabetically
    image_files.sort()

    # Initialize variables for sprite sheet position
    x, y = 0, 0

    for file_name in image_files:
        # Open the image
        image_path = os.path.join(directory_path, file_name)
        image = Image.open(image_path).convert("RGBA")

        # Calculate the remaining width on the current row
        remaining_width = 2048 - x

        # Check if the image fits on the current row
        if image.width > remaining_width:
            x = 0  # Move to the next row
            y += image.height

        # Check if the sprite sheet is full
        if y + image.height > 2048:
            break

        # Paste the image onto the sprite sheet
        sprite_sheet.paste(image, (x, y), image)

        # Move the position for the next image
        x += image.width

    return sprite_sheet


directory_path = r"G:\Models\2023\Unicorn Dance\a_sequence"
sprite_sheet = create_sprite_sheet(directory_path)
sprite_sheet.save(r"G:\Models\2023\Unicorn Dance\a_sequence\sprite_sheet.png")
