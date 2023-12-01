from PIL import Image, ImageDraw

def generate_gradient(width, height):
    # Create a new image with an alpha channel
    gradient = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(gradient)

    # Create a horizontal gradient from alpha to white
    for x in range(width):
        alpha_value = int((x / width) * 255)
        color = (255, 255, 255, alpha_value)
        draw.line([(x, 0), (x, height)], fill=color)

    return gradient

def save_image(image, filename):
    image.save(filename)
    print(f"Image saved as {filename}")

if __name__ == "__main__":
    width, height = 1024, 512
    gradient_image = generate_gradient(width, height)
    save_image(gradient_image, "G:/Models/Refrences/vertical_gradient_with_checker_pattern.png")



























# G:/Models/Refrences/vertical_gradient_with_checker_pattern.png