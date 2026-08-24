import sys
import os
import glob
import re
import threading
import webbrowser
import tkinter as tk
from tkinter import filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk

# Set CustomTkinter theme & appearance
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

def get_asset_path(filename):
    if getattr(sys, 'frozen', False):
        base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(base_dir, "assets", filename)

def natural_sort_key(s):
    return [int(text) if text.isdigit() else text.lower() for text in re.split(r'(\d+)', s)]

class PosterStudioApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Poster Studio Desktop - A4 Poster Generator")
        self.geometry("1100x720")
        self.minsize(950, 620)

        # Set Window & Taskbar Icon
        self.set_app_icon()

        self.image_paths = []
        self.thumbnail_images = []

        self.setup_ui()
        self.auto_load_current_directory()

    def set_app_icon(self):
        icon_ico = get_asset_path("icon.ico")
        icon_png = get_asset_path("icon.png")

        if os.path.exists(icon_ico):
            try:
                self.iconbitmap(icon_ico)
            except Exception as e:
                print(f"Could not set .ico window icon: {e}")
        
        if os.path.exists(icon_png):
            try:
                img = Image.open(icon_png)
                self._icon_photo = ImageTk.PhotoImage(img)
                self.iconphoto(False, self._icon_photo)
            except Exception as e:
                print(f"Could not set .png iconphoto: {e}")

    def open_github(self):
        webbrowser.open("https://github.com/blazecodeprakhar")

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

        header_top = ctk.CTkFrame(logo_frame, fg_color="transparent")
        header_top.pack(anchor="w", fill="x")

        icon_png_path = get_asset_path("icon.png")
        if os.path.exists(icon_png_path):
            try:
                logo_img_pil = Image.open(icon_png_path)
                self.logo_ctk_img = ctk.CTkImage(light_image=logo_img_pil, dark_image=logo_img_pil, size=(38, 38))
                logo_icon_lbl = ctk.CTkLabel(header_top, image=self.logo_ctk_img, text="")
                logo_icon_lbl.pack(side="left", padx=(0, 10))
            except Exception as e:
                print(f"Could not load sidebar logo icon: {e}")

        title_lbl = ctk.CTkLabel(
            header_top, 
            text="Poster Studio", 
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color="#c084fc"
        )
        title_lbl.pack(side="left", anchor="w")

        # Software Branding Link (Clickable Author Watermark)
        author_btn = ctk.CTkButton(
            logo_frame,
            text="🔗 by github.com/blazecodeprakhar",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="transparent",
            text_color="#a855f7",
            hover_color="#334155",
            anchor="w",
            height=22,
            command=self.open_github
        )
        author_btn.pack(anchor="w", pady=(2, 0))

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

        sec_lbl = ctk.CTkLabel(settings_frame, text="⚙️ Poster Settings", font=ctk.CTkFont(size=13, weight="bold"))
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

        # Output PDF File Name
        ctk.CTkLabel(settings_frame, text="Output PDF Name:", font=ctk.CTkFont(size=11), text_color="#94a3b8").pack(anchor="w", padx=12)
        self.entry_pdf_name = ctk.CTkEntry(settings_frame)
        self.entry_pdf_name.insert(0, "color_posters_A4.pdf")
        self.entry_pdf_name.pack(fill="x", padx=12, pady=(2, 12))

        # Software Attribution Box (Software UI Watermark)
        branding_box = ctk.CTkFrame(self.sidebar, fg_color="#0f172a", corner_radius=10, border_width=1, border_color="#334155")
        branding_box.pack(fill="x", padx=15, pady=(5, 10))

        brand_title = ctk.CTkLabel(branding_box, text="⚡ Developer Attribution", font=ctk.CTkFont(size=11, weight="bold"), text_color="#e2e8f0")
        brand_title.pack(anchor="w", padx=10, pady=(8, 2))

        brand_btn = ctk.CTkButton(
            branding_box,
            text="🌐 github.com/blazecodeprakhar",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#311042",
            hover_color="#581c87",
            text_color="#e9d5ff",
            height=28,
            command=self.open_github
        )
        brand_btn.pack(fill="x", padx=8, pady=(0, 8))

        # Progress Bar & Export Action Button
        action_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        action_frame.pack(fill="x", padx=15, pady=(10, 15), side="bottom")

        self.progress_bar = ctk.CTkProgressBar(action_frame, mode="determinate")
        self.progress_bar.set(0)
        self.progress_bar.pack(fill="x", pady=(0, 10))

        self.btn_export = ctk.CTkButton(
            action_frame, 
            text="⚡ CREATE CLEAN POSTER PDF", 
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

        header_actions = ctk.CTkFrame(ws_header, fg_color="transparent")
        header_actions.pack(side="right")

        self.btn_author_link = ctk.CTkButton(
            header_actions,
            text="⭐ GitHub Profile",
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#1e1b4b",
            hover_color="#311042",
            text_color="#c084fc",
            width=110,
            height=28,
            command=self.open_github
        )
        self.btn_author_link.pack(side="left", padx=(0, 10))

        self.badge_pages = ctk.CTkLabel(
            header_actions, 
            text="0 Pages Loaded", 
            fg_color="#311042",
            text_color="#e9d5ff",
            corner_radius=12,
            padx=12,
            pady=4,
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.badge_pages.pack(side="left")

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

        self.btn_export.configure(state="disabled", text="Processing Clean PDF...")
        self.progress_bar.set(0)

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

                # Append clean page without any PDF watermark
                processed_pages.append(resized)

                progress = idx / total
                self.after(0, self.progress_bar.set, progress)

            # Save clean PDF
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
        self.btn_export.configure(state="normal", text="⚡ CREATE CLEAN POSTER PDF")
        self.progress_bar.set(1.0)

        size_mb = os.path.getsize(filename) / (1024 * 1024)
        msg = f"SUCCESS!\n\nClean PDF '{filename}' created successfully.\nPages: {page_count}\nSize: {size_mb:.2f} MB\nPDF Watermark: None (Clean)"
        messagebox.showinfo("Poster Studio Desktop", msg)

    def on_pdf_error(self, err_msg):
        self.btn_export.configure(state="normal", text="⚡ CREATE CLEAN POSTER PDF")
        messagebox.showerror("Error Creating PDF", f"An error occurred:\n{err_msg}")

if __name__ == "__main__":
    app = PosterStudioApp()
    app.mainloop()
