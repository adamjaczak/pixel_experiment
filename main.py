from PIL import Image, ImageOps, ImageFilter

def apply_error(r, g, b, error, weight):
    new_r = (max(0, min(255, int(r + (error * weight)))))
    new_g = (max(0, min(255, int( g + (error * weight)))))
    new_b = (max(0, min(255, int(b + (error * weight)))))

    return (new_r, new_g, new_b)

def recalculate_pixel_data(r, g, b):
    brightness = (0.299 * r) + (0.587 * g) + (0.114 * b)

    if brightness < 128:
        return (0,0,0, brightness - 0)

    return (255,255,255, brightness - 255)

image_path = "portrait-beautiful-blond-woman-with-trendy-hairstyle.jpg"

image = Image.open(image_path).convert("RGB")

def posterize(image):
    img = image.filter(ImageFilter.GaussianBlur(radius=1))
    posterized = ImageOps.posterize(img, bits=2)
    posterized.save("posterized.jpg")


def one_bit_dither(image):

    pixels = image.load()

    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            output = recalculate_pixel_data(r, g, b)
            updated_pixel = output[:3]
            error = output[3]
            pixels[x, y] = updated_pixel
            if x + 1 < width:
                new_r, new_g, new_b = pixels[x + 1, y][:3]
                new_pixels = apply_error(new_r, new_g, new_b, error, (7/16))
                pixels[x + 1, y] = new_pixels
            if x + 1 < width and y + 1 < height:
                new_r, new_g, new_b = pixels[x + 1, y + 1][:3]
                new_pixels = apply_error(new_r, new_g, new_b, error, (1/16))
                pixels[x + 1, y + 1] = new_pixels
            if y + 1 < height:
                new_r, new_g, new_b = pixels[x, y + 1][:3]
                new_pixels = apply_error(new_r, new_g, new_b, error, (5/16))
                pixels[x, y + 1] = new_pixels
            if x > 0 and y + 1 < height:
                new_r, new_g, new_b = pixels[x - 1, y + 1][:3]
                new_pixels = apply_error(new_r, new_g, new_b, error, (3/16))
                pixels[x - 1, y + 1] = new_pixels

    image.save("dither.jpg")

def duotone(image, gradient_bottom: tuple, gradient_top : tuple):
    image = ImageOps.autocontrast(image)
    pixels = image.load()
    width, height = image.size

    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y][:3]
            brightness = (0.299 * r) + (0.587 * g) + (0.114 * b)
            t = brightness / 255.0
            new_r = int(gradient_bottom[0] + (gradient_top[0] - gradient_bottom[0]) * t)
            new_g = int(gradient_bottom[1] + (gradient_top[1] - gradient_bottom[1]) * t)
            new_b = int(gradient_bottom[2] + (gradient_top[2] - gradient_bottom[2]) * t)

            pixels[x, y] = (new_r, new_g, new_b)

    image.save("duotone.jpg")

#one_bit_dither(image)
#posterize(image)
duotone(image, (10, 10, 30), (150, 255, 184))
