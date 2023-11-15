from PIL import Image

def convert_png_to_ico(input_png_path, output_ico_path):
    try:
        # Open the PNG image
        image = Image.open(input_png_path)

        # # Check if the image has an alpha channel (transparency)
        # if image.mode == 'RGBA':
        #     # If it has an alpha channel, convert it to a format that supports transparency
        #     image = image.convert('RGBA')

        # Save the image as an ICO file
        image.save(output_ico_path, format="ICO", sizes=[(8, 8), (16, 16), (32, 32), (48, 48), (64, 64), (256, 256)])

        print(f"Conversion successful. ICO file saved at {output_ico_path}")

    except Exception as e:
        print(f"Error: {e}")

# Example usage:
source = r"G:/Models/Textures/Icons/Icon1.png"
output = "G:/sprite_sheet_creator/SpriteSheetCreator/sprite_sheet_creator/main_window_widget.ico"
convert_png_to_ico(source, output)
