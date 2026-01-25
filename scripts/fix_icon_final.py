from PIL import Image, ImageOps

def fix_icon_final(input_path, output_path):
    print(f"Opening {input_path}...")
    img = Image.open(input_path).convert("RGB")
    
    # Target Brand Color for the Final Icon: #2B2A28 (Deep Graphite) -> (43, 42, 40)
    target_color = (43, 42, 40)
    
    # Background color of the source image is NOT white.
    # It is --warm-off-white: #F7F3EF -> (247, 243, 239) approx.
    # We'll use the Green channel as a proxy for brightness because it's usually cleanest.
    
    # 1. Create a grayscale version for the mask
    gray = img.convert("L")
    
    # 2. Level adjustment to remove JPEG noise and handle the off-white background
    # Background is around 247. Let's say anything above 230 is pure transparency.
    # Foreground is around 43. Anything below 60 is pure opaque.
    
    WHITE_POINT = 230
    BLACK_POINT = 80
    
    def normalize_alpha(p):
        if p >= WHITE_POINT:
            return 0  # Transparent
        if p <= BLACK_POINT:
            return 255 # Opaque
        # Linear interpolation between
        # p=230 -> 0
        # p=80 -> 255
        # Slope = (255 - 0) / (80 - 230) = 255 / -150 = -1.7
        val = (p - WHITE_POINT) * (255 / (BLACK_POINT - WHITE_POINT))
        return int(val)

    # Apply the mapping
    alpha = gray.point(normalize_alpha)
    
    # 3. Create the final image
    # Solid Fill of the target color
    final_img = Image.new("RGBA", img.size, target_color + (0,))
    # Apply our calculated alpha
    final_img.putalpha(alpha)
    
    final_img.save(output_path, "PNG")
    print(f"Saved to {output_path}")

if __name__ == "__main__":
    fix_icon_final("icon-light.png", "icon-transparent.png")
