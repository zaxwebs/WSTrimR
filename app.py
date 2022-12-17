from PIL import Image, ImageChops
import os


def process_image(input_path, output_path, width, height):
    """Trim an image to remove transparent or solid background color, add padding to it, and resize it to fit within specified dimensions. Save it to a specified output path.

    Args:
        input_path (str): The path to the input image file.
        output_path (str): The path to the output image file.
        width (int): The width of the output image.
        height (int): The height of the output image.
    """
    # Open the image file
    image = Image.open(input_path)

    # Set the default background color to white (RGB)
    background_color = (255, 255, 255)

    # Set the background color to transparent if the file is a .png file
    if input_path.lower().endswith('.png'):
        background_color = (255, 255, 255, 0)

    background = Image.new(image.mode, image.size, background_color)
    difference = ImageChops.difference(image, background)
    difference = ImageChops.add(difference, difference, 2.0, -100)
    bounding_box = difference.getbbox()
    if bounding_box:
        trimmed_image = image.crop(bounding_box)

        # Maintain the aspect ratio of the trimmed image
        ratio = min(width/trimmed_image.width, height/trimmed_image.height)
        new_width = int(trimmed_image.width*ratio)
        new_height = int(trimmed_image.height*ratio)

        # Create a new image with the desired dimensions and the same mode as the trimmed image
        resized_image = Image.new(
            trimmed_image.mode, (width, height), background_color)

        # Calculate the position to paste the trimmed image in the center of the new image
        x_pos = (width - new_width) // 2
        y_pos = (height - new_height) // 2

        # Paste the trimmed image onto the new image
        resized_image.paste(trimmed_image.resize(
            (new_width, new_height), resample=Image.LANCZOS), (x_pos, y_pos))

        # Save the processed image to the output path
        resized_image.save(output_path)


def process_images_in_dir(input_dir, output_dir, width, height):
    """Trim all images in a directory, add padding to them, and save them to another directory.

    Args:
        input_dir (str): The path to the input directory.
        output_dir (str): The path to the output directory.
        width (int): The width of the output image.
        height (int): The height of the output image.
    """
    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        # Only process .png and .jpg/.jpeg files
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue

        # Generate the input and output file paths
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Trim, pad, and resize the image and save it to the output path
        process_image(input_path, output_path, width, height)
        print(f'Processed image: {input_path} -> {output_path}')


# Trim, pad, and resize all images in the src directory and save them to the dist directory
process_images_in_dir('src', 'dist', width=400, height=300)
