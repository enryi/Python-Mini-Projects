import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
import re
from pathlib import Path

class VideoCompressor:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Compressor Pro")
        self.root.geometry("900x650")
        self.root.resizable(False, False)
        
        self.bg_primary = "#0f0f0f"
        self.bg_secondary = "#1a1a1a"
        self.bg_tertiary = "#252525"
        self.accent = "#00d4ff"
        self.accent_hover = "#00a8cc"
        self.text_primary = "#ffffff"
        self.text_secondary = "#b0b0b0"
        self.success = "#00ff88"
        self.error = "#ff3366"
        
        self.ffmpeg_path = tk.StringVar(value=r"E:\HDD\ffmpeg\bin\ffmpeg.exe")
        
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        self.preset = tk.StringVar(value="balanced")
        self.quality = tk.IntVar(value=23)
        self.progress = tk.DoubleVar()
        self.is_processing = False
        
        self.setup_styles()
        self.create_widgets()
        
    def setup_styles(self):
        self.root.configure(bg=self.bg_primary)
        
        style = ttk.Style()
        style.theme_use('clam')
        
        style.configure("Title.TLabel", 
                       background=self.bg_primary,
                       foreground=self.text_primary,
                       font=("Segoe UI", 24, "bold"))
        
        style.configure("Subtitle.TLabel",
                       background=self.bg_primary,
                       foreground=self.text_secondary,
                       font=("Segoe UI", 10))
        
        style.configure("Card.TFrame",
                       background=self.bg_secondary,
                       relief="flat",
                       borderwidth=0)
        
        style.configure("Dark.TLabel",
                       background=self.bg_secondary,
                       foreground=self.text_primary,
                       font=("Segoe UI", 10))
        
        style.configure("Small.TLabel",
                       background=self.bg_secondary,
                       foreground=self.text_secondary,
                       font=("Segoe UI", 9))
        
        style.configure("Dark.Horizontal.TProgressbar",
                       background=self.bg_tertiary,
                       troughcolor=self.bg_tertiary,
                       bordercolor=self.bg_tertiary,
                       darkcolor=self.accent,
                       lightcolor=self.accent)
        
    def create_widgets(self):
        header_frame = tk.Frame(self.root, bg=self.bg_primary, height=100)
        header_frame.pack(fill="x", padx=30, pady=(20, 0))
        
        title = ttk.Label(header_frame, text="Video Compressor", style="Title.TLabel")
        title.pack(anchor="w")
        
        subtitle = ttk.Label(header_frame, text="Compress videos with FFmpeg • Simple & Fast", style="Subtitle.TLabel")
        subtitle.pack(anchor="w", pady=(5, 0))
        
        main_container = tk.Frame(self.root, bg=self.bg_primary)
        main_container.pack(fill="both", expand=True, padx=30, pady=20)
        
        ffmpeg_card = ttk.Frame(main_container, style="Card.TFrame")
        ffmpeg_card.pack(fill="x", pady=(0, 15))
        
        ffmpeg_inner = tk.Frame(ffmpeg_card, bg=self.bg_secondary)
        ffmpeg_inner.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(ffmpeg_inner, text="FFMPEG PATH", style="Small.TLabel").pack(anchor="w")
        
        ffmpeg_frame = tk.Frame(ffmpeg_inner, bg=self.bg_secondary)
        ffmpeg_frame.pack(fill="x", pady=(10, 0))
        
        self.ffmpeg_entry = tk.Entry(ffmpeg_frame,
                                    textvariable=self.ffmpeg_path,
                                    bg=self.bg_tertiary,
                                    fg=self.text_primary,
                                    insertbackground=self.text_primary,
                                    relief="flat",
                                    font=("Segoe UI", 10))
        self.ffmpeg_entry.pack(side="left", fill="x", expand=True, ipady=8)
        
        ffmpeg_btn = tk.Button(ffmpeg_frame,
                              text="Browse",
                              bg=self.accent,
                              fg=self.bg_primary,
                              relief="flat",
                              font=("Segoe UI", 10, "bold"),
                              padx=20,
                              cursor="hand2",
                              command=self.browse_ffmpeg)
        ffmpeg_btn.pack(side="right", padx=(10, 0))
        ffmpeg_btn.bind("<Enter>", lambda e: ffmpeg_btn.config(bg=self.accent_hover))
        ffmpeg_btn.bind("<Leave>", lambda e: ffmpeg_btn.config(bg=self.accent))
        
        input_card = ttk.Frame(main_container, style="Card.TFrame")
        input_card.pack(fill="x", pady=(0, 15))
        
        input_inner = tk.Frame(input_card, bg=self.bg_secondary)
        input_inner.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(input_inner, text="INPUT VIDEO", style="Small.TLabel").pack(anchor="w")
        
        input_frame = tk.Frame(input_inner, bg=self.bg_secondary)
        input_frame.pack(fill="x", pady=(10, 0))
        
        self.input_entry = tk.Entry(input_frame, 
                                   textvariable=self.input_file,
                                   bg=self.bg_tertiary,
                                   fg=self.text_primary,
                                   insertbackground=self.text_primary,
                                   relief="flat",
                                   font=("Segoe UI", 10))
        self.input_entry.pack(side="left", fill="x", expand=True, ipady=8)
        
        browse_btn = tk.Button(input_frame,
                              text="Browse",
                              bg=self.accent,
                              fg=self.bg_primary,
                              relief="flat",
                              font=("Segoe UI", 10, "bold"),
                              padx=20,
                              cursor="hand2",
                              command=self.browse_input)
        browse_btn.pack(side="right", padx=(10, 0))
        browse_btn.bind("<Enter>", lambda e: browse_btn.config(bg=self.accent_hover))
        browse_btn.bind("<Leave>", lambda e: browse_btn.config(bg=self.accent))
        
        preset_card = ttk.Frame(main_container, style="Card.TFrame")
        preset_card.pack(fill="x", pady=(0, 15))
        
        preset_inner = tk.Frame(preset_card, bg=self.bg_secondary)
        preset_inner.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(preset_inner, text="COMPRESSION PRESET", style="Small.TLabel").pack(anchor="w")
        
        presets_frame = tk.Frame(preset_inner, bg=self.bg_secondary)
        presets_frame.pack(fill="x", pady=(10, 0))
        
        presets = [
            ("Ultra", "ultra", "Smallest file, lower quality"),
            ("High", "high", "Small file, good quality"),
            ("Balanced", "balanced", "Recommended"),
            ("Quality", "quality", "Larger file, best quality")
        ]
        
        for i, (name, value, desc) in enumerate(presets):
            preset_btn = tk.Radiobutton(presets_frame,
                                       text=name,
                                       variable=self.preset,
                                       value=value,
                                       bg=self.bg_tertiary if value == "balanced" else self.bg_secondary,
                                       fg=self.text_primary,
                                       selectcolor=self.bg_tertiary,
                                       activebackground=self.bg_tertiary,
                                       font=("Segoe UI", 10),
                                       relief="flat",
                                       padx=15,
                                       pady=8,
                                       cursor="hand2")
            preset_btn.grid(row=0, column=i, padx=(0, 10), sticky="ew")
            
            desc_label = tk.Label(presets_frame,
                                text=desc,
                                bg=self.bg_secondary,
                                fg=self.text_secondary,
                                font=("Segoe UI", 8))
            desc_label.grid(row=1, column=i, padx=(0, 10), pady=(5, 0))
        
        presets_frame.grid_columnconfigure(0, weight=1)
        presets_frame.grid_columnconfigure(1, weight=1)
        presets_frame.grid_columnconfigure(2, weight=1)
        presets_frame.grid_columnconfigure(3, weight=1)
        
        quality_card = ttk.Frame(main_container, style="Card.TFrame")
        quality_card.pack(fill="x", pady=(0, 15))
        
        quality_inner = tk.Frame(quality_card, bg=self.bg_secondary)
        quality_inner.pack(fill="x", padx=20, pady=20)
        
        quality_header = tk.Frame(quality_inner, bg=self.bg_secondary)
        quality_header.pack(fill="x")
        
        ttk.Label(quality_header, text="QUALITY (CRF)", style="Small.TLabel").pack(side="left")
        self.quality_label = ttk.Label(quality_header, text="23", style="Dark.TLabel")
        self.quality_label.pack(side="right")
        
        self.quality_slider = tk.Scale(quality_inner,
                                      from_=18, to=30,
                                      orient="horizontal",
                                      variable=self.quality,
                                      bg=self.bg_secondary,
                                      fg=self.text_primary,
                                      troughcolor=self.bg_tertiary,
                                      activebackground=self.accent,
                                      highlightthickness=0,
                                      showvalue=0,
                                      command=self.update_quality_label)
        self.quality_slider.pack(fill="x", pady=(10, 0))
        
        quality_hints = tk.Frame(quality_inner, bg=self.bg_secondary)
        quality_hints.pack(fill="x", pady=(5, 0))
        
        tk.Label(quality_hints, text="Better", bg=self.bg_secondary, fg=self.text_secondary, font=("Segoe UI", 8)).pack(side="left")
        tk.Label(quality_hints, text="Smaller", bg=self.bg_secondary, fg=self.text_secondary, font=("Segoe UI", 8)).pack(side="right")
        
        output_card = ttk.Frame(main_container, style="Card.TFrame")
        output_card.pack(fill="x", pady=(0, 15))
        
        output_inner = tk.Frame(output_card, bg=self.bg_secondary)
        output_inner.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(output_inner, text="OUTPUT VIDEO", style="Small.TLabel").pack(anchor="w")
        
        output_frame = tk.Frame(output_inner, bg=self.bg_secondary)
        output_frame.pack(fill="x", pady=(10, 0))
        
        self.output_entry = tk.Entry(output_frame,
                                    textvariable=self.output_file,
                                    bg=self.bg_tertiary,
                                    fg=self.text_primary,
                                    insertbackground=self.text_primary,
                                    relief="flat",
                                    font=("Segoe UI", 10))
        self.output_entry.pack(side="left", fill="x", expand=True, ipady=8)
        
        save_btn = tk.Button(output_frame,
                           text="Save As",
                           bg=self.accent,
                           fg=self.bg_primary,
                           relief="flat",
                           font=("Segoe UI", 10, "bold"),
                           padx=20,
                           cursor="hand2",
                           command=self.browse_output)
        save_btn.pack(side="right", padx=(10, 0))
        save_btn.bind("<Enter>", lambda e: save_btn.config(bg=self.accent_hover))
        save_btn.bind("<Leave>", lambda e: save_btn.config(bg=self.accent))
        
        progress_card = ttk.Frame(main_container, style="Card.TFrame")
        progress_card.pack(fill="x", pady=(0, 15))
        
        progress_inner = tk.Frame(progress_card, bg=self.bg_secondary)
        progress_inner.pack(fill="x", padx=20, pady=20)
        
        self.status_label = ttk.Label(progress_inner, text="Ready to compress", style="Dark.TLabel")
        self.status_label.pack(anchor="w")
        
        self.progress_bar = ttk.Progressbar(progress_inner,
                                           style="Dark.Horizontal.TProgressbar",
                                           variable=self.progress,
                                           maximum=100)
        self.progress_bar.pack(fill="x", pady=(10, 0))
        
        self.progress_text = ttk.Label(progress_inner, text="", style="Small.TLabel")
        self.progress_text.pack(anchor="w", pady=(5, 0))
        
        self.compress_btn = tk.Button(main_container,
                                     text="COMPRESS VIDEO",
                                     bg=self.accent,
                                     fg=self.bg_primary,
                                     relief="flat",
                                     font=("Segoe UI", 12, "bold"),
                                     padx=30,
                                     pady=15,
                                     cursor="hand2",
                                     command=self.compress_video)
        self.compress_btn.pack(pady=(0, 10))
        self.compress_btn.bind("<Enter>", lambda e: self.compress_btn.config(bg=self.accent_hover) if not self.is_processing else None)
        self.compress_btn.bind("<Leave>", lambda e: self.compress_btn.config(bg=self.accent) if not self.is_processing else None)
        
    def update_quality_label(self, value):
        self.quality_label.config(text=str(int(float(value))))
        
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm"), ("All files", "*.*")]
        )
        if filename:
            self.input_file.set(filename)
            path = Path(filename)
            output = path.parent / f"{path.stem}_compressed{path.suffix}"
            self.output_file.set(str(output))
            
    def browse_output(self):
        filename = filedialog.asksaveasfilename(
            title="Save Compressed Video As",
            defaultextension=".mp4",
            filetypes=[("MP4 files", "*.mp4"), ("All files", "*.*")]
        )
        if filename:
            self.output_file.set(filename)
            
    def browse_ffmpeg(self):
        filename = filedialog.askopenfilename(
            title="Select FFmpeg Executable",
            filetypes=[("FFmpeg executable", "ffmpeg.exe"), ("All files", "*.*")]
        )
        if filename:
            self.ffmpeg_path.set(filename)

    def get_video_duration(self, filepath):
        cmd = [self.ffmpeg_path.get(), "-i", filepath]
        result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True)
        duration_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})', result.stderr)
        if duration_match:
            hours, minutes, seconds = map(int, duration_match.groups())
            return hours * 3600 + minutes * 60 + seconds
        return None
        
    def compress_video(self):
        if not self.input_file.get():
            messagebox.showerror("Error", "Please select an input video file")
            return
            
        if not self.output_file.get():
            messagebox.showerror("Error", "Please specify an output file")
            return
            
        if not os.path.exists(self.ffmpeg_path.get()):
            messagebox.showerror("Error", f"FFmpeg not found at {self.ffmpeg_path.get()}")
            return
            
        self.is_processing = True
        self.compress_btn.config(state="disabled", bg=self.bg_tertiary, text="COMPRESSING...")
        self.progress.set(0)
        self.status_label.config(text="Processing video...")
        
        thread = threading.Thread(target=self.run_compression)
        thread.daemon = True
        thread.start()
        
    def run_compression(self):
        try:
            preset_settings = {
                "ultra": {"crf": 28, "preset": "faster"},
                "high": {"crf": 25, "preset": "fast"},
                "balanced": {"crf": self.quality.get(), "preset": "medium"},
                "quality": {"crf": 20, "preset": "slow"}
            }
            
            settings = preset_settings[self.preset.get()]
            
            cmd = [
                self.ffmpeg_path.get(),
                "-i", self.input_file.get(),
                "-c:v", "libx264",
                "-crf", str(settings["crf"]),
                "-preset", settings["preset"],
                "-c:a", "aac",
                "-b:a", "128k",
                "-movflags", "+faststart",
                "-y",
                self.output_file.get()
            ]
            
            duration = self.get_video_duration(self.input_file.get())
            
            process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True, bufsize=1)
            
            for line in process.stderr:
                time_match = re.search(r'time=(\d{2}):(\d{2}):(\d{2})', line)
                if time_match and duration:
                    hours, minutes, seconds = map(int, time_match.groups())
                    current_time = hours * 3600 + minutes * 60 + seconds
                    progress = (current_time / duration) * 100
                    
                    self.root.after(0, self.update_progress, progress, f"Processing: {progress:.1f}%")
            
            process.wait()
            
            if process.returncode == 0:
                self.root.after(0, self.compression_complete)
            else:
                self.root.after(0, self.compression_failed, "Compression failed")
                
        except Exception as e:
            self.root.after(0, self.compression_failed, str(e))
            
    def update_progress(self, value, text):
        self.progress.set(value)
        self.progress_text.config(text=text)
        
    def compression_complete(self):
        self.is_processing = False
        self.compress_btn.config(state="normal", bg=self.accent, text="COMPRESS VIDEO")
        self.progress.set(100)
        self.status_label.config(text="✓ Compression complete!", foreground=self.success)
        self.progress_text.config(text="Video saved successfully")
        
        input_size = os.path.getsize(self.input_file.get()) / (1024 * 1024)
        output_size = os.path.getsize(self.output_file.get()) / (1024 * 1024)
        reduction = ((input_size - output_size) / input_size) * 100
        
        messagebox.showinfo("Success", 
                          f"Video compressed successfully!\n\n"
                          f"Original: {input_size:.1f} MB\n"
                          f"Compressed: {output_size:.1f} MB\n"
                          f"Size reduction: {reduction:.1f}%")
        
    def compression_failed(self, error):
        self.is_processing = False
        self.compress_btn.config(state="normal", bg=self.accent, text="COMPRESS VIDEO")
        self.status_label.config(text="✗ Compression failed", foreground=self.error)
        self.progress_text.config(text=error)
        messagebox.showerror("Error", f"Compression failed:\n{error}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCompressor(root)
    root.mainloop()