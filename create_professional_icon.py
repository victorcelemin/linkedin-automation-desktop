"""
Generate a professional, eye-catching icon for LinkedIn Automation
"""

from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
import math


def create_professional_icon():
    """Create a professional, eye-catching icon"""
    size = 512  # Higher resolution for better quality
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # Colors
    LINKEDIN_BLUE = (0, 119, 181)
    LINKEDIN_LIGHT = (0, 150, 200)
    WHITE = (255, 255, 255)
    GOLD = (255, 193, 7)
    DARK_BLUE = (0, 50, 100)
    
    # Draw rounded rectangle background with gradient
    margin = 20
    corner_radius = 40
    
    # Create gradient background
    for y in range(size):
        for x in range(size):
            # Check if point is inside rounded rectangle
            if (margin <= x <= size - margin and margin <= y <= size - margin):
                # Check corners
                in_corner = False
                for cx, cy in [(margin + corner_radius, margin + corner_radius),
                              (size - margin - corner_radius, margin + corner_radius),
                              (margin + corner_radius, size - margin - corner_radius),
                              (size - margin - corner_radius, size - margin - corner_radius)]:
                    if math.sqrt((x - cx)**2 + (y - cy)**2) > corner_radius:
                        if ((x < margin + corner_radius or x > size - margin - corner_radius) and
                            (y < margin + corner_radius or y > size - margin - corner_radius)):
                            in_corner = True
                            break
                
                if not in_corner:
                    # Gradient from top to bottom
                    ratio = (y - margin) / (size - 2 * margin)
                    r = int(LINKEDIN_BLUE[0] * (1 - ratio) + DARK_BLUE[0] * ratio)
                    g = int(LINKEDIN_BLUE[1] * (1 - ratio) + DARK_BLUE[1] * ratio)
                    b = int(LINKEDIN_BLUE[2] * (1 - ratio) + DARK_BLUE[2] * ratio)
                    img.putpixel((x, y), (r, g, b, 255))
    
    # Draw border with glow effect
    draw.rounded_rectangle([margin, margin, size - margin, size - margin],
                          radius=corner_radius, outline=WHITE, width=6)
    
    # Draw inner shadow/glow
    draw.rounded_rectangle([margin + 8, margin + 8, size - margin - 8, size - margin - 8],
                          radius=corner_radius - 8, outline=LINKEDIN_LIGHT, width=2)
    
    # Draw "in" text (LinkedIn style) - large and prominent
    try:
        font_large = ImageFont.truetype("arialbd.ttf", 200)
        font_small = ImageFont.truetype("arial.ttf", 36)
        font_robot = ImageFont.truetype("arialbd.ttf", 28)
    except:
        try:
            font_large = ImageFont.truetype("arial.ttf", 200)
            font_small = ImageFont.truetype("arial.ttf", 36)
            font_robot = ImageFont.truetype("arial.ttf", 28)
        except:
            font_large = ImageFont.load_default()
            font_small = ImageFont.load_default()
            font_robot = ImageFont.load_default()
    
    # Draw "in" text with shadow
    text = "in"
    bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 30
    
    # Shadow
    draw.text((x + 4, y + 4), text, fill=(0, 0, 0, 100), font=font_large)
    # Main text
    draw.text((x, y), text, fill=WHITE, font=font_large)
    
    # Draw robot icon - more professional
    robot_center_x = size - 80
    robot_center_y = 70
    
    # Robot circle background
    robot_bg_size = 70
    draw.ellipse([robot_center_x - robot_bg_size//2, robot_center_y - robot_bg_size//2,
                 robot_center_x + robot_bg_size//2, robot_center_y + robot_bg_size//2],
                fill=GOLD, outline=WHITE, width=3)
    
    # Robot head
    head_size = 35
    head_x = robot_center_x - head_size//2
    head_y = robot_center_y - head_size//2 + 5
    draw.rounded_rectangle([head_x, head_y, head_x + head_size, head_y + head_size],
                          radius=8, fill=WHITE, outline=DARK_BLUE, width=2)
    
    # Robot eyes - glowing
    eye_size = 8
    eye_y = head_y + 12
    draw.ellipse([head_x + 8, eye_y, head_x + 8 + eye_size, eye_y + eye_size],
                fill=LINKEDIN_BLUE)
    draw.ellipse([head_x + head_size - 8 - eye_size, eye_y, 
                 head_x + head_size - 8, eye_y + eye_size],
                fill=LINKEDIN_BLUE)
    
    # Robot smile
    draw.arc([head_x + 8, head_y + 18, head_x + head_size - 8, head_y + head_size - 5],
            0, 180, fill=LINKEDIN_BLUE, width=3)
    
    # Robot antenna
    draw.line([robot_center_x, head_y, robot_center_x, head_y - 12],
             fill=WHITE, width=4)
    draw.ellipse([robot_center_x - 6, head_y - 20, robot_center_x + 6, head_y - 8],
                fill=GOLD, outline=WHITE, width=2)
    
    # Draw automation symbol (gear-like)
    gear_x = 80
    gear_y = size - 80
    gear_size = 50
    
    # Draw gear
    for i in range(8):
        angle = i * 45
        x1 = gear_x + int(gear_size * math.cos(math.radians(angle)))
        y1 = gear_y + int(gear_size * math.sin(math.radians(angle)))
        x2 = gear_x + int((gear_size + 15) * math.cos(math.radians(angle)))
        y2 = gear_y + int((gear_size + 15) * math.sin(math.radians(angle)))
        draw.line([(x1, y1), (x2, y2)], fill=WHITE, width=8)
    
    draw.ellipse([gear_x - gear_size, gear_y - gear_size,
                 gear_x + gear_size, gear_y + gear_size],
                outline=WHITE, width=6)
    draw.ellipse([gear_x - 15, gear_y - 15, gear_x + 15, gear_y + 15],
                fill=GOLD)
    
    # Draw text "AUTOMATION" at bottom
    text_auto = "AUTOMATION"
    bbox_auto = draw.textbbox((0, 0), text_auto, font=font_small)
    text_auto_width = bbox_auto[2] - bbox_auto[0]
    x_auto = (size - text_auto_width) // 2
    y_auto = size - 75
    
    # Text shadow
    draw.text((x_auto + 2, y_auto + 2), text_auto, fill=(0, 0, 0, 100), font=font_small)
    # Text
    draw.text((x_auto, y_auto), text_auto, fill=GOLD, font=font_small)
    
    # Draw sparkle effects
    sparkles = [(100, 120), (400, 150), (150, 400), (380, 380)]
    for sx, sy in sparkles:
        # Draw 4-point star
        for angle in [0, 45, 90, 135]:
            length = 12 if angle % 90 == 0 else 6
            ex = sx + int(length * math.cos(math.radians(angle)))
            ey = sy + int(length * math.sin(math.radians(angle)))
            draw.line([(sx, sy), (ex, ey)], fill=GOLD, width=2)
    
    # Save as ICO with multiple sizes
    img.save('assets/icon.ico', format='ICO', 
             sizes=[(512, 512), (256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
    
    # Also save as PNG
    img.save('assets/icon.png', format='PNG')
    
    # Create smaller versions for different uses
    img_small = img.resize((256, 256), Image.Resampling.LANCZOS)
    img_small.save('assets/icon_256.png', format='PNG')
    
    img_64 = img.resize((64, 64), Image.Resampling.LANCZOS)
    img_64.save('assets/icon_64.png', format='PNG')
    
    print("✅ Professional icons created:")
    print("   - assets/icon.ico (all sizes)")
    print("   - assets/icon.png (512x512)")
    print("   - assets/icon_256.png (256x256)")
    print("   - assets/icon_64.png (64x64)")
    
    return img


if __name__ == "__main__":
    os.makedirs('assets', exist_ok=True)
    create_professional_icon()