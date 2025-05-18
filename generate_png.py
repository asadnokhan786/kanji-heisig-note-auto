import cairosvg
from PIL import Image

def svg_to_png(input_svg_path, output_png_path, size=(500, 500)):
    """
    Convert an SVG file to PNG and resize it to the specified size.
    
    Parameters:
    input_svg_path (str): The path to the input SVG file.
    output_png_path (str): The path to save the resulting PNG file.
    size (tuple): The desired size of the output PNG image (default is (500, 500)).
    """
    # Step 1: Convert SVG to PNG using cairosvg
    cairosvg.svg2png(url=input_svg_path, write_to=output_png_path)
    
    # Step 2: Open the generated PNG using Pillow
    with Image.open(output_png_path) as img:
        # Step 3: Resize the PNG to the specified size
        img = img.resize(size, Image.ANTIALIAS)
        
        # Step 4: Save the resized PNG
        img.save(output_png_path)
    
    print(f"PNG image saved as: {output_png_path}")

