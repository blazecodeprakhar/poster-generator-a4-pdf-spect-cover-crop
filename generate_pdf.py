import glob
import os
import re
from PIL import Image

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

def create_a4_poster_pdf(image_folder='.', output_pdf='color_posters_A4.pdf', dpi=300):
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

    print(f"Processing {len(image_files)} images for clean A4 Cover Fit ({a4_w}x{a4_h} px at {dpi} DPI)...")

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
        processed_pages.append(resized)
        print(f"Page {idx:02d}: {filename} ({w}x{h}) -> {crop_type} -> Clean A4 Page")

    processed_pages[0].save(
        output_pdf,
        save_all=True,
        append_images=processed_pages[1:],
        resolution=float(dpi)
    )
    size_mb = os.path.getsize(output_pdf) / (1024 * 1024)
    print(f"\nSUCCESS: Generated clean '{output_pdf}' ({size_mb:.2f} MB) with {len(processed_pages)} pages.")

if __name__ == '__main__':
    create_a4_poster_pdf()
