import os
import glob
import re
import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageDraw, ImageFont

# Set CustomTkinter theme & appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

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

    # Sleek dark translucent background box with border
    draw.rounded_rectangle([x1, y1, x2, y2], radius=12, fill=(15, 23, 42, 190), outline=(168, 85, 247, 140), width=3)
    draw.text((x1 + padding_x, y1 + padding_y - 2), watermark_text, fill=(255, 255, 255, 240), font=font)

    converted_rgb = image.convert('RGBA')
    watermarked = Image.alpha_composite(converted_rgb, overlay)
    return watermarked.convert('RGB')

class PosterStudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Poster Studio Desktop - A4 Poster Generator")
        self.geometry("1100 x 720")
        self.minsize(950, 620)

        self.image_paths = []
        self.thumbnail_images = []

        self.setup_ui()
        self.auto_load_current_directory()

    def setup_ui(self):
        # Grid layout: 2 columns (Sidebar 320px, Main workspace 1fr)
        self.grid_columnconfigure(0, weight=0, minsize=320)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ================= SIDEBAR =================
        self.sidebar = ctk.CTkFrame(self, corner_radius=15, fg_color=("#1e293b", "#0f172a"))
        self.sidebar.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        # App Logo & Title
        logo_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logo_frame.pack(fill="x", padx=15, pady=(15, 10))

        title_lbl = ctk.CTkLabel(
            logo_frame, 
            text="Poster Studio Desktop", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#c084fc"
        )
        title_lbl.pack(anchor="w")

        author_lbl = ctk.CTkLabel(
            logo_frame, 
            text="by github.com/blazecodeprakhar", 
            font=ctk.CTkFont(size=11),
            text_color="#94a3b8"
        )
        author_lbl.pack(anchor="w")

        # File Selection Buttons
        btn_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        btn_frame.pack(fill="x", padx=15, pady=10)

        self.btn_select = ctk.CTkButton(
            btn_frame, 
            text="📁 Select Poster Images", 
            font=ctk.CTkFont(size=13, weight="bold"),
            height=38,
            command=self.select_images
        )
        self.btn_select.pack(fill="x", pady=(0, 6))

        self.btn_autoload = ctk.CTkButton(
            btn_frame, 
            text="🔄 Reload Current Folder", 
            fg_color="transparent",
            border_width=1,
            border_color="#475569",
            text_color="#cbd5e1",
            height=32,
            command=self.auto_load_current_directory
        )
        self.btn_autoload.pack(fill="x")

        # Settings Section
        settings_frame = ctk.CTkFrame(self.sidebar, fg_color="#1e293b", corner_radius=10)
        settings_frame.pack(fill="x", padx=15, pady=10)

        sec_lbl = ctk.CTkLabel(settings_frame, text="⚙️ Poster & Watermark Settings", font=ctk.CTkFont(size=13, weight="bold"))
        sec_lbl.pack(anchor="w", padx=12, pady=(10, 5))

        # Paper Format
        ctk.CTkLabel(settings_frame, text="Paper Format:", font=ctk.CTkFont(size=11), text_color="#94a3b8").pack(anchor="w", padx=12)
        self.opt_paper = ctk.CTkOptionMenu(settings_frame, values=["A4 (210 x 297 mm)", "A3 (297 x 420 mm)", "US Letter (8.5 x 11 in)"])
        self.opt_paper.pack(fill="x", padx=12, pady=(2, 8))

        # Fit Strategy
        ctk.CTkLabel(settings_frame, text="Fit Strategy:", font=ctk.CTkFont(size=11), text_color="#94a3b8").pack(anchor="w", padx=12)
        self.opt_fit = ctk.CTkOptionMenu(
            settings_frame, 
            values=["Aspect Cover (Edge-to-Edge Fill)", "Contain (Full Image + Padding)"]
        )
        self.opt_fit.pack(fill="x", padx=12, pady=(2, 8))

        # Watermark Text
        ctk.CTkLabel(settings_frame, text="Watermark Text:", font=ctk.CTkFont(size=11), text_color="#94a3b8").pack(anchor="w", padx=12)
        self.entry_watermark = ctk.CTkEntry(settings_frame)
        self.entry_watermark.insert(0, "https://github.com/blazecodeprakhar")
        self.entry_watermark.pack(fill="x", padx=12, pady=(2, 6))

        # Enable Watermark Checkbox
        self.chk_watermark_var = ctk.BooleanVar(value=True)
        self.chk_watermark = ctk.CTkCheckBox(
            settings_frame, 
            text="Enable Page Watermark", 
            variable=self.chk_watermark_var,
            font=ctk.CTkFont(size=12)
        )
        self.chk_watermark.pack(anchor="w", padx=12, pady=(2, 10))

        # Output PDF File Name
        ctk.CTkLabel(settings_frame, text="Output PDF Name:", font=ctk.CTkFont(size=11), text_color="#94a3b8").pack(anchor="w", padx=12)
        self.entry_pdf_name = ctk.CTkEntry(settings_frame)
        self.entry_pdf_name.insert(0, "color_posters_A4.pdf")
        self.entry_pdf_name.pack(fill="x", padx=12, pady=(2, 12))

        # Progress Bar & Export Action Button
        action_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        action_frame.pack(fill="x", padx=15, pady=(auto, 15), side="bottom")

        self.progress_bar = ctk.CTkProgressBar(action_frame, mode="determinate")
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(0, 10))

        self.btn_export = ctk.CTkButton(
            action_frame, 
            text="⚡ CREATE POSTER PDF", 
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#a855f7",
            hover_color="#9333ea",
            height=44,
            command=self.start_pdf_generation
        )
        self.btn_export.pack(fill="x")

        # ================= MAIN WORKSPACE =================
        self.workspace = ctk.CTkFrame(self, corner_radius=15, fg_color="#1e293b")
        self.workspace.grid(row=0, column=1, sticky="nsew", padx=(0, 15), pady=15)
        self.workspace.grid_rowconfigure(1, weight=1)
        self.workspace.grid_columnconfigure(0, weight=1)

        # Header
        ws_header = ctk.CTkFrame(self.workspace, fg_color="transparent")
        ws_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(15, 10))

        self.lbl_workspace_title = ctk.CTkLabel(
            ws_header, 
            text="Selected Poster Pages", 
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.lbl_workspace_title.pack(side="left")

        self.badge_pages = ctk.CTkLabel(
            ws_header, 
            text="0 Pages Loaded", 
            fg_color="#311042",
            text_color="#e9d5ff",
            corner_radius=12,
            padx=12,
            pady=4,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.badge_pages.pack(side="right")

        # Scrollable Thumbnail Grid
        self.scroll_grid = ctk.CTkScrollableFrame(self.workspace, fg_color="transparent")
        self.scroll_grid.grid(row=1, column=0, sticky="nsew", padx=15, pady=(0, 15))

    def auto_load_current_directory(self):
        extensions = ('*.jpeg', '*.jpg', '*.png', '*.webp')
        files = []
        for ext in extensions:
            files.extend(glob.glob(ext))
        
        files = sorted(list(set(files)), key=natural_sort_key)
        if files:
            self.load_images_from_list([os.path.abspath(f) for f in files])

    def select_images(self):
        file_paths = filedialog.askopenfilenames(
            title="Select Poster Images",
            filetypes=[("Image Files", "*.jpg *.jpeg *.png *.webp")]
        )
        if file_paths:
            sorted_paths = sorted(list(file_paths), key=natural_sort_key)
            self.load_images_from_list(sorted_paths)

    def load_images_from_list(self, paths):
        self.image_paths = list(paths)
        self.render_thumbnails()

    def remove_image(self, index):
        if 0 <= index < len(self.image_paths):
            del self.image_paths[index]
            self.render_thumbnails()

    def render_thumbnails(self):
        # Clear existing scrollable frame
        for child in self.scroll_grid.winfo_children():
            child.destroy()

        self.thumbnail_images.clear()
        count = len(self.image_paths)
        self.badge_pages.configure(text=f"{count} Page{'s' if count != 1 else ''} Loaded")

        if count == 0:
            empty_lbl = ctk.CTkLabel(
                self.scroll_grid, 
                text="No poster images loaded yet.\nClick '📁 Select Poster Images' to start.",
                font=ctk.CTkFont(size=14),
                text_color="#64748b"
            )
            empty_lbl.pack(expand=True, pady=100)
            self.btn_export.configure(state="disabled")
            return

        self.btn_export.configure(state="normal")

        # Grid configuration for thumbnails (3 per row)
        cols = 3
        for idx, img_path in enumerate(self.image_paths):
            row = idx // cols
            col = idx % cols

            card = ctk.CTkFrame(self.scroll_grid, fg_color="#0f172a", corner_radius=10)
            card.grid(row=row, column=col, padx=8, pady=8, sticky="nsew")

            filename = os.path.basename(img_path)
            
            try:
                img = Image.open(img_path)
                w, h = img.size
                # Create thumbnail with 1:1.414 aspect ratio container
                thumb_w = 160
                thumb_h = 226
                img_ratio = h / w
                target_ratio = thumb_h / thumb_w

                if img_ratio > target_ratio:
                    new_h = int(w * target_ratio)
                    top = (h - new_h) // 2
                    cropped = img.crop((0, top, w, top + new_h))
                else:
                    new_w = int(h / target_ratio)
                    left = (w - new_w) // 2
                    cropped = img.crop((left, 0, left + new_w, h))

                cropped_thumb = cropped.resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
                ctk_img = ctk.CTkImage(light_image=cropped_thumb, dark_image=cropped_thumb, size=(thumb_w, thumb_h))
                self.thumbnail_images.append(ctk_img)

                img_lbl = ctk.CTkLabel(card, image=ctk_img, text="")
                img_lbl.pack(padx=8, pady=(8, 4))
            except Exception as e:
                err_lbl = ctk.CTkLabel(card, text="[Image Error]", text_color="#ef4444")
                err_lbl.pack(padx=8, pady=20)

            # Card Footer with Title and Delete Button
            info_frame = ctk.CTkFrame(card, fg_color="transparent")
            info_frame.pack(fill="x", padx=8, pady=(0, 6))

            title_str = f"{idx + 1}. {filename[:14]}..." if len(filename) > 17 else f"{idx + 1}. {filename}"
            name_lbl = ctk.CTkLabel(info_frame, text=title_str, font=ctk.CTkFont(size=11), text_color="#cbd5e1")
            name_lbl.pack(side="left")

            btn_del = ctk.CTkButton(
                info_frame, 
                text="❌", 
                width=24, 
                height=24, 
                fg_color="#334155", 
                hover_color="#ef4444",
                command=lambda i=idx: self.remove_image(i)
            )
            btn_del.pack(side="right")

    def start_pdf_generation(self):
        if not self.image_paths:
            messagebox.showwarning("Warning", "Please select poster images first.")
            return

        self.btn_export.configure(state="disabled", text="Processing PDF...")
        self.progress_bar.set(0)

        # Run in separate thread to prevent UI freezing
        thread = threading.Thread(target=self.generate_pdf_worker, daemon=True)
        thread.start()

    def generate_pdf_worker(self):
        try:
            dpi = 300
            a4_w = int(8.27 * dpi)
            a4_h = int(11.69 * dpi)
            target_ratio = a4_h / a4_w

            fit_mode = self.opt_fit.get()
            is_cover = "Aspect Cover" in fit_mode
            enable_watermark = self.chk_watermark_var.get()
            watermark_text = self.entry_watermark.get().strip() if enable_watermark else ""

            output_filename = self.entry_pdf_name.get().strip()
            if not output_filename.endswith(".pdf"):
                output_filename += ".pdf"

            total = len(self.image_paths)
            processed_pages = []

            for idx, filepath in enumerate(self.image_paths, start=1):
                img = Image.open(filepath).convert('RGB')
                w, h = img.size
                img_ratio = h / w

                if is_cover:
                    if img_ratio > target_ratio:
                        new_h = int(w * target_ratio)
                        top = (h - new_h) // 2
                        cropped = img.crop((0, top, w, top + new_h))
                    else:
                        new_w = int(h / target_ratio)
                        left = (w - new_w) // 2
                        cropped = img.crop((left, 0, left + new_w, h))

                    resized = cropped.resize((a4_w, a4_h), Image.Resampling.LANCZOS)
                else:
                    # Contain mode
                    background = Image.new('RGB', (a4_w, a4_h), (255, 255, 255))
                    if img_ratio > target_ratio:
                        dh = a4_h
                        dw = int(a4_h / img_ratio)
                        dx = (a4_w - dw) // 2
                        dy = 0
                    else:
                        dw = a4_w
                        dh = int(a4_w * img_ratio)
                        dx = 0
                        dy = (a4_h - dh) // 2

                    img_resized = img.resize((dw, dh), Image.Resampling.LANCZOS)
                    background.paste(img_resized, (dx, dy))
                    resized = background

                if enable_watermark and watermark_text:
                    final_page = draw_watermark(resized, watermark_text)
                else:
                    final_page = resized

                processed_pages.append(final_page)
                
                # Update GUI progress bar safely
                progress = idx / total
                self.after(0, self.progress_bar.set, progress)

            # Save PDF
            processed_pages[0].save(
                output_filename,
                save_all=True,
                append_images=processed_pages[1:],
                resolution=float(dpi)
            )

            self.after(0, self.on_pdf_success, output_filename, total)

        except Exception as e:
            self.after(0, self.on_pdf_error, str(e))

    def on_pdf_success(self, filename, page_count):
        self.btn_export.configure(state="normal", text="⚡ CREATE POSTER PDF")
        self.progress_bar.set(1.0)

        size_mb = os.path.getsize(filename) / (1024 * 1024)
        msg = f"SUCCESS!\n\nPDF '{filename}' created successfully.\nPages: {page_count}\nSize: {size_mb:.2f} MB\nWatermark: {'Yes' if self.chk_watermark_var.get() else 'No'}"
        messagebox.showinfo("Poster Studio Desktop", msg)

    def on_pdf_error(self, err_msg):
        self.btn_export.configure(state="normal", text="⚡ CREATE POSTER PDF")
        messagebox.showerror("Error Creating PDF", f"An error occurred:\n{err_msg}")

if __name__ == "__main__":
    app = PosterStudioApp()
    app.mainloop()
