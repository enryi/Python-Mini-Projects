import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import customtkinter as ctk
from PIL import Image, ImageTk
import subprocess
import os
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ModernImageProcessor:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Image Processor")
        self.root.geometry("800x700")
        self.root.minsize(600, 500)
        
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        
        self.ffmpeg_path = tk.StringVar(value="E:\\HDD\\ffmpeg\\bin\\ffmpeg.exe")
        self.selected_file = None
        self.output_dir = None
        
        self.setup_ui()
        
    def setup_ui(self):
        title_frame = ctk.CTkFrame(self.root, corner_radius=10)
        title_frame.grid(row=0, column=0, sticky="ew", padx=20, pady=(20, 10))
        title_frame.grid_columnconfigure(0, weight=1)
        
        title_label = ctk.CTkLabel(
            title_frame,
            text="🖼️ Image Processor",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.grid(row=0, column=0, pady=20)
        
        self.main_frame = ctk.CTkScrollableFrame(self.root, corner_radius=10)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=10)
        self.main_frame.grid_columnconfigure((0, 1), weight=1)
        
        self.create_file_section()
        
        self.create_ffmpeg_section()
        
        self.create_resize_section()
        self.create_compress_section()
        self.create_convert_section()
        
        self.create_output_section()
        
        self.create_progress_section()
        
    def create_file_section(self):
        file_frame = ctk.CTkFrame(self.main_frame)
        file_frame.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        file_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(file_frame, text="📁 File Selection", font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, columnspan=3, pady=(15, 10), sticky="w", padx=15
        )
        
        ctk.CTkButton(
            file_frame,
            text="Select Image",
            command=self.select_file,
            width=120
        ).grid(row=1, column=0, padx=15, pady=(0, 15), sticky="w")
        
        self.file_label = ctk.CTkLabel(file_frame, text="No file selected", text_color="gray")
        self.file_label.grid(row=1, column=1, padx=10, pady=(0, 15), sticky="ew")
        
        ctk.CTkButton(
            file_frame,
            text="Output Folder",
            command=self.select_output_dir,
            width=120
        ).grid(row=2, column=0, padx=15, pady=(0, 15), sticky="w")
        
        self.output_label = ctk.CTkLabel(file_frame, text="Same as input", text_color="gray")
        self.output_label.grid(row=2, column=1, padx=10, pady=(0, 15), sticky="ew")
        
    def create_ffmpeg_section(self):
        ffmpeg_frame = ctk.CTkFrame(self.main_frame)
        ffmpeg_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        ffmpeg_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(ffmpeg_frame, text="⚙️ FFmpeg Settings", font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, columnspan=3, pady=(15, 10), sticky="w", padx=15
        )
        
        ctk.CTkLabel(ffmpeg_frame, text="FFmpeg Path:").grid(
            row=1, column=0, padx=15, pady=5, sticky="w"
        )
        
        self.ffmpeg_entry = ctk.CTkEntry(ffmpeg_frame, textvariable=self.ffmpeg_path)
        self.ffmpeg_entry.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkButton(
            ffmpeg_frame,
            text="Browse",
            command=self.browse_ffmpeg,
            width=80
        ).grid(row=1, column=2, padx=(10, 15), pady=5)
        
        ctk.CTkButton(
            ffmpeg_frame,
            text="Test FFmpeg",
            command=self.test_ffmpeg,
            width=120
        ).grid(row=2, column=0, padx=15, pady=(5, 15), sticky="w")
        
        self.ffmpeg_status = ctk.CTkLabel(ffmpeg_frame, text="Not tested", text_color="gray")
        self.ffmpeg_status.grid(row=2, column=1, padx=10, pady=(5, 15), sticky="w")
        
    def create_resize_section(self):
        resize_frame = ctk.CTkFrame(self.main_frame)
        resize_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 10), pady=(0, 20))
        resize_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(resize_frame, text="📏 Resize Image", font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=(15, 10), sticky="w", padx=15
        )
        
        ctk.CTkLabel(resize_frame, text="Width:").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        self.width_entry = ctk.CTkEntry(resize_frame, placeholder_text="1920")
        self.width_entry.grid(row=1, column=1, padx=(10, 15), pady=5, sticky="ew")
        
        ctk.CTkLabel(resize_frame, text="Height:").grid(row=2, column=0, padx=15, pady=5, sticky="w")
        self.height_entry = ctk.CTkEntry(resize_frame, placeholder_text="1080")
        self.height_entry.grid(row=2, column=1, padx=(10, 15), pady=5, sticky="ew")
        
        self.maintain_aspect = ctk.CTkCheckBox(resize_frame, text="Maintain aspect ratio")
        self.maintain_aspect.grid(row=3, column=0, columnspan=2, padx=15, pady=5, sticky="w")
        
        ctk.CTkButton(
            resize_frame,
            text="Resize Image",
            command=self.resize_image,
            fg_color="#2B7A2B",
            hover_color="#1E5F1E"
        ).grid(row=4, column=0, columnspan=2, padx=15, pady=(10, 15), sticky="ew")
        
    def create_compress_section(self):
        compress_frame = ctk.CTkFrame(self.main_frame)
        compress_frame.grid(row=2, column=1, sticky="nsew", padx=(10, 0), pady=(0, 20))
        compress_frame.grid_columnconfigure(1, weight=1)
        
        ctk.CTkLabel(compress_frame, text="🗜️ Compress with FFmpeg", font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, columnspan=2, pady=(15, 10), sticky="w", padx=15
        )
        
        ctk.CTkLabel(compress_frame, text="Quality (1-31):").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        self.quality_slider = ctk.CTkSlider(compress_frame, from_=1, to=31, number_of_steps=30)
        self.quality_slider.set(23)
        self.quality_slider.grid(row=1, column=1, padx=(10, 15), pady=5, sticky="ew")
        
        self.quality_label = ctk.CTkLabel(compress_frame, text="23")
        self.quality_label.grid(row=2, column=1, padx=(10, 15), pady=0, sticky="w")
        self.quality_slider.configure(command=self.update_quality_label)
        
        ctk.CTkButton(
            compress_frame,
            text="Compress Image",
            command=self.compress_image,
            fg_color="#B8860B",
            hover_color="#8B6914"
        ).grid(row=3, column=0, columnspan=2, padx=15, pady=(15, 15), sticky="ew")
        
    def create_convert_section(self):
        convert_frame = ctk.CTkFrame(self.main_frame)
        convert_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        convert_frame.grid_columnconfigure((1, 3), weight=1)
        
        ctk.CTkLabel(convert_frame, text="🔄 Convert Format", font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, columnspan=4, pady=(15, 10), sticky="w", padx=15
        )
        
        formats = [
            "JPEG", "JPG", "PNG", "BMP", "TIFF", "WEBP", "ICO", "GIF", 
            "EPS", "PCX", "PPM", "SGI", "TGA", "PSD", "PDF", "HEIC",
            "DIB", "EXR", "IM", "MSP", "Palm", "PCX", "XV"
        ]
        formats.sort()
        
        ctk.CTkLabel(convert_frame, text="From:").grid(row=1, column=0, padx=15, pady=5, sticky="w")
        self.from_format = ctk.CTkOptionMenu(convert_frame, values=formats, state="disabled")  # Set initially disabled
        self.from_format.grid(row=1, column=1, padx=10, pady=5, sticky="ew")
        
        ctk.CTkLabel(convert_frame, text="To:").grid(row=1, column=2, padx=15, pady=5, sticky="w")
        self.to_format = ctk.CTkOptionMenu(convert_frame, values=formats)
        self.to_format.grid(row=1, column=3, padx=(10, 15), pady=5, sticky="ew")
        
        ctk.CTkButton(
            convert_frame,
            text="Convert Image",
            command=self.convert_image,
            fg_color="#7B2D7B",
            hover_color="#5A1F5A"
        ).grid(row=2, column=0, columnspan=4, padx=15, pady=(10, 15), sticky="ew")
        
    def create_output_section(self):
        log_frame = ctk.CTkFrame(self.main_frame)
        log_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        log_frame.grid_columnconfigure(0, weight=1)
        log_frame.grid_rowconfigure(1, weight=1)
        
        ctk.CTkLabel(log_frame, text="📋 Output Log", font=ctk.CTkFont(size=16, weight="bold")).grid(
            row=0, column=0, pady=(15, 10), sticky="w", padx=15
        )
        
        self.log_text = ctk.CTkTextbox(log_frame, height=120, font=ctk.CTkFont(family="Consolas", size=12))
        self.log_text.grid(row=1, column=0, padx=15, pady=(0, 15), sticky="ew")
        
    def create_progress_section(self):
        progress_frame = ctk.CTkFrame(self.main_frame)
        progress_frame.grid(row=5, column=0, columnspan=2, sticky="ew")
        progress_frame.grid_columnconfigure(0, weight=1)
        
        self.progress_bar = ctk.CTkProgressBar(progress_frame)
        self.progress_bar.grid(row=0, column=0, padx=15, pady=15, sticky="ew")
        self.progress_bar.set(0)
        
    def log_message(self, message):
        """Add message to log"""
        self.log_text.insert("end", f"{message}\n")
        self.log_text.see("end")
        
    def update_quality_label(self, value):
        """Update quality label"""
        self.quality_label.configure(text=str(int(value)))
        
    def select_file(self):
        """Select input image file"""
        file_path = filedialog.askopenfilename(
            title="Select Image File",
            filetypes=[
                ("All Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp *.ico *.gif *.eps"
                 " *.pcx *.ppm *.sgi *.tga *.psd *.pdf *.heic *.dib *.exr *.im *.msp *.palm *.pcx *.xv"),
                ("JPEG files", "*.jpg *.jpeg"),
                ("PNG files", "*.png"),
                ("BMP files", "*.bmp"),
                ("TIFF files", "*.tiff"),
                ("WebP files", "*.webp"),
                ("ICO files", "*.ico"),
                ("GIF files", "*.gif"),
                ("EPS files", "*.eps"),
                ("PSD files", "*.psd"),
                ("PDF files", "*.pdf"),
                ("HEIC files", "*.heic"),
                ("Other formats", "*.pcx *.ppm *.sgi *.tga *.dib *.exr *.im *.msp *.palm *.xv"),
                ("All files", "*.*")
            ]
        )
        
        if file_path:
            self.selected_file = file_path
            self.file_label.configure(text=os.path.basename(file_path), text_color="white")
            self.log_message(f"Selected file: {file_path}")
            
            # Detect and set input format
            extension = os.path.splitext(file_path)[1].upper().lstrip('.')
            if extension == 'JPG':
                extension = 'JPEG'
            self.from_format.configure(state="disabled")  # Disable the dropdown
            self.from_format.set(extension)  # Set the detected format
            
    def select_output_dir(self):
        """Select output directory"""
        dir_path = filedialog.askdirectory(title="Select Output Directory")
        if dir_path:
            self.output_dir = dir_path
            self.output_label.configure(text=os.path.basename(dir_path), text_color="white")
            self.log_message(f"Output directory: {dir_path}")
            
    def browse_ffmpeg(self):
        """Browse for FFmpeg executable"""
        file_path = filedialog.askopenfilename(
            title="Select FFmpeg Executable",
            filetypes=[("Executable files", "*.exe"), ("All files", "*.*")]
        )
        
        if file_path:
            self.ffmpeg_path.set(file_path)
            self.log_message(f"FFmpeg path updated: {file_path}")
            
    def test_ffmpeg(self):
        """Test FFmpeg installation"""
        def test_in_thread():
            try:
                result = subprocess.run(
                    [self.ffmpeg_path.get(), "-version"],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                if result.returncode == 0:
                    self.ffmpeg_status.configure(text="✅ Working", text_color="green")
                    self.log_message("FFmpeg test: Success")
                else:
                    self.ffmpeg_status.configure(text="❌ Error", text_color="red")
                    self.log_message("FFmpeg test: Failed")
                    
            except Exception as e:
                self.ffmpeg_status.configure(text="❌ Not found", text_color="red")
                self.log_message(f"FFmpeg test error: {str(e)}")
                
        threading.Thread(target=test_in_thread, daemon=True).start()
        
    def get_output_path(self, original_path, suffix="", extension=None):
        """Generate output file path"""
        if self.output_dir:
            base_dir = self.output_dir
        else:
            base_dir = os.path.dirname(original_path)
            
        filename = os.path.splitext(os.path.basename(original_path))[0]
        
        if extension:
            ext = f".{extension.lower()}"
        else:
            ext = os.path.splitext(original_path)[1]
            
        return os.path.join(base_dir, f"{filename}{suffix}{ext}")
        
    def resize_image(self):
        """Resize image using PIL"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select an image file first")
            return
            
        try:
            width = self.width_entry.get()
            height = self.height_entry.get()
            
            if not width or not height:
                messagebox.showerror("Error", "Please enter both width and height")
                return
                
            width, height = int(width), int(height)
            
            self.progress_bar.set(0.2)
            self.log_message("Starting image resize...")
            
            with Image.open(self.selected_file) as img:
                if self.maintain_aspect.get():
                    img.thumbnail((width, height), Image.Resampling.LANCZOS)
                    resized_img = img
                else:
                    resized_img = img.resize((width, height), Image.Resampling.LANCZOS)
                
                self.progress_bar.set(0.8)
                
                output_path = self.get_output_path(self.selected_file, "_resized")
                resized_img.save(output_path, quality=95)
                
                self.progress_bar.set(1.0)
                self.log_message(f"Image resized successfully: {output_path}")
                messagebox.showinfo("Success", f"Image resized and saved to:\n{output_path}")
                
        except Exception as e:
            self.log_message(f"Resize error: {str(e)}")
            messagebox.showerror("Error", f"Failed to resize image: {str(e)}")
        finally:
            self.progress_bar.set(0)
            
    def compress_image(self):
        """Compress image using FFmpeg"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select an image file first")
            return
            
        def compress_in_thread():
            try:
                self.progress_bar.set(0.2)
                self.log_message("Starting FFmpeg compression...")
                
                quality = int(self.quality_slider.get())
                output_path = self.get_output_path(self.selected_file, "_compressed")
                
                cmd = [
                    self.ffmpeg_path.get(),
                    "-i", self.selected_file,
                    "-q:v", str(quality),
                    "-y",
                    output_path
                ]
                
                self.progress_bar.set(0.5)
                
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.returncode == 0:
                    self.progress_bar.set(1.0)
                    self.log_message(f"Image compressed successfully: {output_path}")
                    messagebox.showinfo("Success", f"Image compressed and saved to:\n{output_path}")
                else:
                    self.log_message(f"FFmpeg error: {result.stderr}")
                    messagebox.showerror("Error", f"FFmpeg compression failed:\n{result.stderr}")
                    
            except Exception as e:
                self.log_message(f"Compression error: {str(e)}")
                messagebox.showerror("Error", f"Failed to compress image: {str(e)}")
            finally:
                self.progress_bar.set(0)
                
        threading.Thread(target=compress_in_thread, daemon=True).start()
        
    def convert_image(self):
        """Convert image format"""
        if not self.selected_file:
            messagebox.showerror("Error", "Please select an image file first")
            return
            
        try:
            self.progress_bar.set(0.2)
            self.log_message("Starting format conversion...")
            
            format_mapping = {
                'JPG': ('JPEG', 'jpg'),
                'JPEG': ('JPEG', 'jpeg'),
                'PNG': ('PNG', 'png'),
                'BMP': ('BMP', 'bmp'),
                'TIFF': ('TIFF', 'tiff'),
                'WEBP': ('WEBP', 'webp'),
                'ICO': ('ICO', 'ico'),
                'GIF': ('GIF', 'gif'),
                'EPS': ('EPS', 'eps'),
                'PCX': ('PCX', 'pcx'),
                'PPM': ('PPM', 'ppm'),
                'SGI': ('SGI', 'sgi'),
                'TGA': ('TGA', 'tga'),
                'PSD': ('PSD', 'psd'),
                'PDF': ('PDF', 'pdf'),
                'HEIC': ('HEIC', 'heic')
            }
            
            selected_from = self.from_format.get().upper()
            selected_to = self.to_format.get().upper()
            
            from_fmt = format_mapping.get(selected_from, (selected_from, selected_from.lower()))[0]
            to_fmt, to_ext = format_mapping.get(selected_to, (selected_to, selected_to.lower()))
            
            with Image.open(self.selected_file) as img:
                if to_fmt == 'JPEG' and img.mode in ('RGBA', 'LA', 'P'):
                    background = Image.new('RGB', img.size, (255, 255, 255))
                    if img.mode == 'P':
                        img = img.convert('RGBA')
                    background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                    img = background
                    
                self.progress_bar.set(0.8)
                
                output_path = self.get_output_path(self.selected_file, "_converted", to_ext)
                
                save_kwargs = {}
                if to_fmt == 'JPEG':
                    save_kwargs['quality'] = 95
                    
                img.save(output_path, format=to_fmt, **save_kwargs)
                
                self.progress_bar.set(1.0)
                self.log_message(f"Image converted successfully: {output_path}")
                messagebox.showinfo("Success", f"Image converted and saved to:\n{output_path}")
                
        except Exception as e:
            self.log_message(f"Conversion error: {str(e)}")
            messagebox.showerror("Error", f"Failed to convert image: {str(e)}")
        finally:
            self.progress_bar.set(0)
            
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernImageProcessor()
    app.run()