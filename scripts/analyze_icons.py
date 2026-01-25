from PIL import Image
import os

def analyze_image(path):
    if not os.path.exists(path):
        print(f"{path}: Not found")
        return
        
    img = Image.open(path)
    print(f"--- Analysis of {path} ---")
    print(f"Format: {img.format}")
    print(f"Mode: {img.mode}")
    print(f"Size: {img.size}")
    
    if img.mode == 'RGBA':
        extrema = img.getextrema()
        alpha_extrema = extrema[3]
        print(f"Alpha range: {alpha_extrema}")
        if alpha_extrema[0] < 255:
            print("Contains transparency.")
        else:
            print("Full opaque alpha channel.")
    else:
        print("No alpha channel.")
        
    # sample corner
    img = img.convert('RGBA')
    print(f"Top-Left Pixel: {img.getpixel((0,0))}")
    print(f"Center Pixel: {img.getpixel((img.width//2, img.height//2))}")

if __name__ == "__main__":
    analyze_image("icon-light.png")
    analyze_image("icon-dark.png")
