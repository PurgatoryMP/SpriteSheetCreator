from PIL import Image

def create_checker_texture(size, output_path):
    image = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    step = 1

    while step <= size:
        for i in range(0, size, step * 2):
            for j in range(0, size, step * 2):
                for x in range(i, min(i + step, size)):
                    for y in range(j, min(j + step, size)):
                        alpha = int((x + y) % (step * 2) / (step * 2) * 255)
                        image.putpixel((x, y), (0, 0, 0, alpha))

        step *= 2

    image.save(output_path)

if __name__ == "__main__":
    output_path = "G:/Models/2023/Unicorn Dance/checker_texture.png"
    size = 2048
    create_checker_texture(size, output_path)
    print(f"Checker texture saved to {output_path}")
