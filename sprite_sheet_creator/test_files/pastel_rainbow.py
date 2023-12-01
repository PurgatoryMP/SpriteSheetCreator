from PIL import Image, ImageDraw

def lerp_color(color1, color2, t):
    """Linear interpolation between two RGB colors."""
    return tuple(int(c1 + (c2 - c1) * t) for c1, c2 in zip(color1, color2))

def create_smooth_pastel_rainbow(width, height):
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    num_colors = 7
    color_width = width // num_colors

    pastel_colors = [
        (255, 185, 185),  # Light Red
        (255, 218, 185),  # Light Orange
        (255, 255, 185),  # Light Yellow
        (185, 255, 185),  # Light Green
        (185, 218, 255),  # Light Blue
        (218, 185, 255),  # Light Purple
        (255, 185, 255),  # Light Pink
    ]

    for i in range(num_colors - 1):
        color1 = pastel_colors[i]
        color2 = pastel_colors[i + 1]

        x_start = i * color_width
        x_end = (i + 1) * color_width

        for x in range(x_start, x_end):
            t = (x - x_start) / color_width
            blended_color = lerp_color(color1, color2, t)
            draw.line([(x, 0), (x, height)], fill=blended_color)

    # Draw the last color
    for x in range((num_colors - 1) * color_width, width):
        draw.line([(x, 0), (x, height)], fill=pastel_colors[-1])

    image.save("G:/Models/Refrences/A_pastel_rainbow.png")

if __name__ == "__main__":
    width, height = 1024, 512
    create_smooth_pastel_rainbow(width, height)










# G:/Models/Refrences/A_pastel_rainbow.png