from PIL import Image, ImageChops
import os

def trim(image, color):
    """Trim an image to remove transparent or solid background color.
    
    Args:
        image (PIL.Image): The image to trim.
        color (tuple): The background color to remove (RGB or RGBA).
        
    Returns:
        PIL.Image: The trimmed image.
    """
    background = Image.new(image.mode, image.size, color)
    difference = ImageChops.difference(image, background)
    difference = ImageChops.add(difference, difference, 2.0, -100)
    bounding_box = difference.getbbox()
    if bounding_box:
        return image.crop(bounding_box)

def process_image(input_path, output_path, background_color):
    """Trim an image and save it to a specified output path.
    
    Args:
        input_path (str): The path to the input image file.
        output_path (str): The path to the output image file.
        background_color (tuple): The background color to remove (RGB or RGBA).
    """
    # Open the image file
    image = Image.open(input_path)
    
    # Trim the image
    trimmed_image = trim(image, background_color)
    
    # Save the trimmed image to the output path
    trimmed_image.save(output_path)

def process_images_in_dir(input_dir, output_dir):
    """Trim all images in a directory and save them to another directory.
    
    Args:
        input_dir (str): The path to the input directory.
        output_dir (str): The path to the output directory.
    """
    # Set the default background color to white (RGB)
    background_color = (255, 255, 255)

    # Iterate over all files in the input directory
    for filename in os.listdir(input_dir):
        # Only process .png and .jpg/.jpeg files
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        
        # Set the background color to transparent if the file is a .png file
        background_color = (255, 255, 255, 0) if filename.lower().endswith('.png') else (255, 255, 255)

        # Generate the input and output file paths
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)

        # Trim the image and save it to the output path
        process_image(input_path, output_path, background_color)
        print(f'Processed image: {input_path} -> {output_path}')

# Trim all images in the src directory and save them to the dist directory
process_images_in_dir('src', 'dist')