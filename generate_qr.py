import qrcode
from PIL import Image, ImageDraw, ImageFont
import os

# Base URL of your Streamlit app
BASE_URL = "https://mwanaisha222-edic-attendence-main-ndibxo.streamlit.app/"

# Mapping of blocks to query parameter values
blocks = [
    {"key": "block_civil", "discipline": "civil"},
    {"key": "block_electrical", "discipline": "electrical"},
    {"key": "block_mechanical", "discipline": "mechanical"},
    {"key": "block_automotive", "discipline": "automotive"}
]

def create_qr_with_text(url, text, filename):
    """Create QR code with centered text overlay"""
    
    # Create QR code with higher error correction to allow for overlay
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,  # High error correction
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    
    # Create QR code image
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Convert to RGB if needed
    if qr_img.mode != 'RGB':
        qr_img = qr_img.convert('RGB')
    
    # Create a drawing context
    draw = ImageDraw.Draw(qr_img)
    
    # Get image dimensions
    width, height = qr_img.size
    
    # Try to use a default font, fallback to PIL's default if not available
    try:
        # Try different font sizes to fit the text nicely
        font_size = max(12, width // 20)  # Adaptive font size based on QR code size
        font = ImageFont.truetype("arial.ttf", font_size)
    except (OSError, IOError):
        try:
            font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", font_size)
        except (OSError, IOError):
            try:
                font = ImageFont.truetype("/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf", font_size)
            except (OSError, IOError):
                font = ImageFont.load_default()
    
    # Calculate text size and position for centering
    text_bbox = draw.textbbox((0, 0), text.upper(), font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    # Calculate center position
    text_x = (width - text_width) // 2
    text_y = (height - text_height) // 2
    
    # Create a white background rectangle for the text
    padding = 8
    rect_x1 = text_x - padding
    rect_y1 = text_y - padding
    rect_x2 = text_x + text_width + padding
    rect_y2 = text_y + text_height + padding
    
    # Draw white background rectangle
    draw.rectangle([rect_x1, rect_y1, rect_x2, rect_y2], fill="white", outline="black", width=2)
    
    # Draw the text
    draw.text((text_x, text_y), text.upper(), fill="black", font=font)
    
    # Save the image
    qr_img.save(filename)
    return qr_img

# Generate QR codes for each block
for block in blocks:
    # Construct the full URL with query parameter
    url = f"{BASE_URL}?block={block['discipline']}"
    
    # Create and save the QR code with discipline name in center
    filename = f"{block['key']}_qr.png"
    create_qr_with_text(url, block['discipline'], filename)
    print(f"Generated QR code for {block['discipline'].capitalize()} block: {url}")
    print(f"Saved as: {filename}")

print("✅ QR codes generated for Civil, Electrical, and Mechanical blocks with centered discipline names.")