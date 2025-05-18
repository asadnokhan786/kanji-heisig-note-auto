import cairosvg
from PIL import Image


def svg_to_png(input_svg_path, output_png_path, size=(500, 500), dpi=600):
    """
    Convert an SVG file to a high-resolution PNG, with optional resizing.
    
    Parameters:
    input_svg_path (str): Path to the input SVG file.
    output_png_path (str): Path to save the resulting PNG file.
    size (tuple): Desired size of the PNG image.
    dpi (int): DPI for rendering the SVG at higher resolution.
    """
    # Step 1: Convert the SVG to PNG with a high dpi (larger resolution)
    cairosvg.svg2png(url=input_svg_path, write_to=output_png_path, scale=50)


    # Step 2: Open the PNG image and resize if necessary
    with Image.open(output_png_path) as img:
        # Resize the image while keeping the high resolution
        img = img.resize(size, Image.Resampling.LANCZOS)
        img.save(output_png_path)
    
    print(f"High-quality PNG image saved as: {output_png_path}")
