import glob
import os
import re
from PIL import Image, ImageDraw, ImageFont

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def draw_watermark(image, watermark_text="https://github.com/blazecodeprakhar"):
    if not watermark_text:
        return image

    overlay = Image.new('RGBA', image.size, (255, 255, 255, 0))
    draw = ImageDraw.Draw(overlay)

    font_size = max(24, int(image.height * 0.015))
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except IOError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    margin = int(image.height * 0.02)
    padding_x = int(font_size * 0.6)
    padding_y = int(font_size * 0.3)

    x2 = image.width - margin
    y2 = image.height - margin
    x1 = x2 - text_w - (padding_x * 2)
    y1 = y2 - text_h - (padding_y * 2)

    # Draw sleek dark translucent rounded background pill
    draw.rounded_rectangle([x1, y1, x2, y2], radius=12, fill=(15, 23, 42, 190), outline=(168, 85, 247, 140), width=3)
    # Draw watermark text
    draw.text((x1 + padding_x, y1 + padding_y - 2), watermark_text, fill=(255, 255, 255, 240), font=font)

    converted_rgb = image.convert('RGBA')
    watermarked = Image.alpha_composite(converted_rgb, overlay)
    return watermarked.convert('RGB')

def create_a4_poster_pdf(image_folder='.', output_pdf='color_posters_A4.pdf', dpi=300, watermark_text="https://github.com/blazecodeprakhar"):
    a4_w = int(8.27 * dpi)
    a4_h = int(11.69 * dpi)
    target_ratio = a4_h / a4_w

    extensions = ('*.jpeg', '*.jpg', '*.png', '*.webp')
    image_files = []
    for ext in extensions:
        image_files.extend(glob.glob(os.path.join(image_folder, ext)))

    image_files = sorted(list(set(image_files)), key=natural_sort_key)

    if not image_files:
        print("No images found!")
        return

    print(f"Processing {len(image_files)} images for A4 Cover Fit ({a4_w}x{a4_h} px at {dpi} DPI)...")
    print(f"Watermark: '{watermark_text}'")

    processed_pages = []
    for idx, filepath in enumerate(image_files, start=1):
        filename = os.path.basename(filepath)
        img = Image.open(filepath).convert('RGB')
        w, h = img.size
        img_ratio = h / w

        if img_ratio > target_ratio:
            new_h = int(w * target_ratio)
            top = (h - new_h) // 2
            crop_box = (0, top, w, top + new_h)
            crop_type = f"cropped top/bottom ({h - new_h}px)"
        else:
            new_w = int(h / target_ratio)
            left = (w - new_w) // 2
            crop_box = (left, 0, left + new_w, h)
            crop_type = f"cropped left/right ({w - new_w}px)"

        cropped = img.crop(crop_box)
        resized = cropped.resize((a4_w, a4_h), Image.Resampling.LANCZOS)
        
        # Apply Watermark
        final_page = draw_watermark(resized, watermark_text)
        processed_pages.append(final_page)
        print(f"Page {idx:02d}: {filename} ({w}x{h}) -> {crop_type} -> Watermarked A4 Page")

    processed_pages[0].save(
        output_pdf,
        save_all=True,
        append_images=processed_pages[1:],
        resolution=float(dpi)
    )
    size_mb = os.path.getsize(output_pdf) / (1024 * 1024)
    print(f"\nSUCCESS: Generated watermarked '{output_pdf}' ({size_mb:.2f} MB) with {len(processed_pages)} pages.")

if __name__ == '__main__':
    create_a4_poster_pdf()
