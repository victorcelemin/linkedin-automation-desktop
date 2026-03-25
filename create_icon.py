"""
Generate application icon for LinkedIn Automation
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    """Create application icon"""
    # Create 256x256 image
    size = 256
    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    # LinkedIn Blue gradient background
    linkedin_blue = (0, 119, 181)
    linkedin_dark = (0, 65, 130)
    
    # Draw rounded rectangle background
    margin = 10
    for i in range(size - 2*margin):
        ratio = i / (size - 2*margin)
        color = tuple(int(linkedin_blue[j] * (1-ratio) + linkedin_dark[j] * ratio) for j in range(3))
        draw.line([(margin, margin + i), (size - margin, margin + i)], fill=color + (255,))
    
    # Draw border
    draw.rectangle([margin, margin, size-margin, size-margin], outline=(255, 255, 255, 200), width=4)
    
    # Draw "in" text (LinkedIn style)
    try:
        font = ImageFont.truetype("arial.ttf", 120)
    except:
        font = ImageFont.load_default()
    
    # Draw "in" text
    text = "in"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (size - text_width) // 2
    y = (size - text_height) // 2 - 10
    
    draw.text((x, y), text, fill=(255, 255, 255, 255), font=font)
    
    # Draw robot icon on top
    robot_size = 60
    robot_x = size - 50
    robot_y = 30
    
    # Robot head
    draw.rectangle([robot_x, robot_y, robot_x + robot_size, robot_y + robot_size], 
                   fill=(255, 255, 255, 255), outline=(0, 0, 0, 255), width=2)
    
    # Robot eyes
    eye_size = 12
    draw.ellipse([robot_x + 12, robot_y + 15, robot_x + 12 + eye_size, robot_y + 15 + eye_size], 
                 fill=(0, 0, 0, 255))
    draw.ellipse([robot_x + 36, robot_y + 15, robot_x + 36 + eye_size, robot_y + 15 + eye_size], 
                 fill=(0, 0, 0, 255))
    
    # Robot mouth
    draw.arc([robot_x + 15, robot_y + 30, robot_x + 45, robot_y + 45], 0, 180, fill=(0, 0, 0, 255), width=3)
    
    # Robot antenna
    draw.line([robot_x + 30, robot_y, robot_x + 30, robot_y - 15], fill=(255, 255, 255, 255), width=3)
    draw.ellipse([robot_x + 25, robot_y - 25, robot_x + 35, robot_y - 15], fill=(255, 255, 0, 255))
    
    # Save as ICO
    img.save('assets/icon.ico', format='ICO', sizes=[(256, 256), (128, 128), (64, 64), (32, 32), (16, 16)])
    print("Icon created: assets/icon.ico")
    
    # Also save as PNG
    img.save('assets/icon.png', format='PNG')
    print("Icon created: assets/icon.png")
    
    return img

if __name__ == "__main__":
    os.makedirs('assets', exist_ok=True)
    create_icon()