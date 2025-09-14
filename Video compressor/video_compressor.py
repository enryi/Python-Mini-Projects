import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import subprocess
import threading
import os
import re
from pathlib import Path
import glob

class VideoCompressor:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Compressor Pro")
        self.root.geometry("950x750")
        self.root.resizable(True, True)
        
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
        
        # Single mode variables
        self.input_file = tk.StringVar()
        self.output_file = tk.StringVar()
        
        # Batch mode variables
        self.input_folder = tk.StringVar()
        self.output_folder = tk.StringVar()
        
        # Common variables
        self.compression_mode = tk.StringVar(value="single")
        self.preset = tk.StringVar(value="balanced")
        self.quality = tk.IntVar(value=23)
        self.progress = tk.DoubleVar()
        self.is_processing = False
        
        # Batch processing
        self.current_file_progress = tk.DoubleVar()
        self.batch_files = []
        self.current_batch_index = 0
        
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
        
        # Custom scrollbar style
        style.configure("Custom.Vertical.TScrollbar",
                       background=self.bg_tertiary,
                       troughcolor=self.bg_primary,
                       bordercolor=self.bg_primary,
                       arrowcolor=self.text_secondary,
                       darkcolor=self.bg_tertiary,
                       lightcolor=self.bg_tertiary,
                       gripcount=0,
                       relief="flat",
                       borderwidth=0)
        
        style.map("Custom.Vertical.TScrollbar",
                  background=[('active', self.accent), ('pressed', self.accent_hover)])
        
    def create_widgets(self):
        # Create main canvas and scrollbar
        self.canvas = tk.Canvas(self.root, bg=self.bg_primary, highlightthickness=0)
        
        # Custom thin scrollbar
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview, 
                                      style="Custom.Vertical.TScrollbar")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas and scrollbar
        self.scrollbar.pack(side="right", fill="y", padx=(0, 5))
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Create scrollable frame
        self.scrollable_frame = tk.Frame(self.canvas, bg=self.bg_primary)
        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Bind events for scrolling
        self.scrollable_frame.bind("<Configure>", self.on_frame_configure)
        self.canvas.bind("<Configure>", self.on_canvas_configure)
        self.bind_mousewheel()
        
        # Header
        header_frame = tk.Frame(self.scrollable_frame, bg=self.bg_primary, height=100)
        header_frame.pack(fill="x", padx=30, pady=(20, 0))
        
        title = ttk.Label(header_frame, text="Video Compressor Pro", style="Title.TLabel")
        title.pack(anchor="w")
        
        subtitle = ttk.Label(header_frame, text="Compress videos with FFmpeg • Single & Batch Mode", style="Subtitle.TLabel")
        subtitle.pack(anchor="w", pady=(5, 0))
        
        self.main_frame = tk.Frame(self.scrollable_frame, bg=self.bg_primary)
        self.main_frame.pack(fill="both", expand=True, padx=30, pady=20)
        
        # FFmpeg Path Card
        ffmpeg_card = ttk.Frame(self.main_frame, style="Card.TFrame")
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
        
        # Mode Selection Card
        mode_card = ttk.Frame(self.main_frame, style="Card.TFrame")
        mode_card.pack(fill="x", pady=(0, 15))
        
        mode_inner = tk.Frame(mode_card, bg=self.bg_secondary)
        mode_inner.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(mode_inner, text="COMPRESSION MODE", style="Small.TLabel").pack(anchor="w")
        
        mode_frame = tk.Frame(mode_inner, bg=self.bg_secondary)
        mode_frame.pack(fill="x", pady=(10, 0))
        
        single_btn = tk.Radiobutton(mode_frame,
                                   text="Single File",
                                   variable=self.compression_mode,
                                   value="single",
                                   bg=self.bg_tertiary,
                                   fg=self.text_primary,
                                   selectcolor=self.bg_tertiary,
                                   activebackground=self.bg_tertiary,
                                   font=("Segoe UI", 11, "bold"),
                                   relief="flat",
                                   padx=20,
                                   pady=10,
                                   cursor="hand2",
                                   command=self.toggle_mode)
        single_btn.pack(side="left", padx=(0, 15))
        
        batch_btn = tk.Radiobutton(mode_frame,
                                  text="Batch Processing",
                                  variable=self.compression_mode,
                                  value="batch",
                                  bg=self.bg_secondary,
                                  fg=self.text_primary,
                                  selectcolor=self.bg_tertiary,
                                  activebackground=self.bg_tertiary,
                                  font=("Segoe UI", 11, "bold"),
                                  relief="flat",
                                  padx=20,
                                  pady=10,
                                  cursor="hand2",
                                  command=self.toggle_mode)
        batch_btn.pack(side="left")
        
        # Input/Output Cards Container
        self.io_container = tk.Frame(self.main_frame, bg=self.bg_primary)
        self.io_container.pack(fill="x", pady=(0, 15))
        
        # Create both single and batch input/output sections
        self.create_single_mode_widgets()
        self.create_batch_mode_widgets()
        
        # Preset Card
        preset_card = ttk.Frame(self.main_frame, style="Card.TFrame")
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
        
        for i in range(4):
            presets_frame.grid_columnconfigure(i, weight=1)
        
        # Quality Card
        quality_card = ttk.Frame(self.main_frame, style="Card.TFrame")
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
        
        tk.Label(quality_hints, text="Better Quality", bg=self.bg_secondary, fg=self.text_secondary, font=("Segoe UI", 8)).pack(side="left")
        tk.Label(quality_hints, text="Smaller Size", bg=self.bg_secondary, fg=self.text_secondary, font=("Segoe UI", 8)).pack(side="right")
        
        # Format Conversion Card
        self.create_convert_section()
        
        # Progress Card
        progress_card = ttk.Frame(self.main_frame, style="Card.TFrame")
        progress_card.pack(fill="x", pady=(0, 15))
        
        progress_inner = tk.Frame(progress_card, bg=self.bg_secondary)
        progress_inner.pack(fill="x", padx=20, pady=20)
        
        self.status_label = ttk.Label(progress_inner, text="Ready to compress", style="Dark.TLabel")
        self.status_label.pack(anchor="w")
        
        # Overall progress (for batch mode)
        self.progress_bar = ttk.Progressbar(progress_inner,
                                           style="Dark.Horizontal.TProgressbar",
                                           variable=self.progress,
                                           maximum=100)
        self.progress_bar.pack(fill="x", pady=(10, 0))
        
        self.progress_text = ttk.Label(progress_inner, text="", style="Small.TLabel")
        self.progress_text.pack(anchor="w", pady=(5, 0))
        
        # Current file progress (for batch mode)
        self.current_file_label = ttk.Label(progress_inner, text="", style="Small.TLabel")
        self.current_file_progress_bar = ttk.Progressbar(progress_inner,
                                                        style="Dark.Horizontal.TProgressbar",
                                                        variable=self.current_file_progress,
                                                        maximum=100)
        
        # Compress Button Container
        button_container = tk.Frame(self.main_frame, bg=self.bg_primary)
        button_container.pack(fill="x", pady=(10, 30))
        
        self.compress_btn = tk.Button(button_container,
                                     text="COMPRESS VIDEO",
                                     bg=self.accent,
                                     fg=self.bg_primary,
                                     relief="flat",
                                     font=("Segoe UI", 12, "bold"),
                                     padx=30,
                                     pady=15,
                                     cursor="hand2",
                                     command=self.start_compression)
        self.compress_btn.pack(pady=10)
        self.compress_btn.bind("<Enter>", lambda e: self.compress_btn.config(bg=self.accent_hover) if not self.is_processing else None)
        self.compress_btn.bind("<Leave>", lambda e: self.compress_btn.config(bg=self.accent) if not self.is_processing else None)
        
        # Initialize with single mode
        self.toggle_mode()
        
        # Update scroll region after everything is packed
        self.root.after(100, self.update_scroll_region)
    
    def on_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_canvas_configure(self, event):
        canvas_width = event.width
        self.canvas.itemconfig(self.canvas_window, width=canvas_width)
        
    def bind_mousewheel(self):
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
        def _bind_to_mousewheel(event):
            self.canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
        def _unbind_from_mousewheel(event):
            self.canvas.unbind_all("<MouseWheel>")
            
        self.canvas.bind('<Enter>', _bind_to_mousewheel)
        self.canvas.bind('<Leave>', _unbind_from_mousewheel)
    
    def update_scroll_region(self):
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        
    def create_single_mode_widgets(self):
        # Single Mode Input Card
        self.single_input_card = ttk.Frame(self.io_container, style="Card.TFrame")
        
        single_input_inner = tk.Frame(self.single_input_card, bg=self.bg_secondary)
        single_input_inner.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(single_input_inner, text="INPUT VIDEO", style="Small.TLabel").pack(anchor="w")
        
        input_frame = tk.Frame(single_input_inner, bg=self.bg_secondary)
        input_frame.pack(fill="x", pady=(10, 0))
        
        self.input_entry = tk.Entry(input_frame, 
                                   textvariable=self.input_file,
                                   bg=self.bg_tertiary,
                                   fg=self.text_primary,
                                   insertbackground=self.text_primary,
                                   relief="flat",
                                   font=("Segoe UI", 10))
        self.input_entry.pack(side="left", fill="x", expand=True, ipady=8)
        
        browse_input_btn = tk.Button(input_frame,
                              text="Browse",
                              bg=self.accent,
                              fg=self.bg_primary,
                              relief="flat",
                              font=("Segoe UI", 10, "bold"),
                              padx=20,
                              cursor="hand2",
                              command=self.browse_input)
        browse_input_btn.pack(side="right", padx=(10, 0))
        browse_input_btn.bind("<Enter>", lambda e: browse_input_btn.config(bg=self.accent_hover))
        browse_input_btn.bind("<Leave>", lambda e: browse_input_btn.config(bg=self.accent))
        
        # Single Mode Output Card
        self.single_output_card = ttk.Frame(self.io_container, style="Card.TFrame")
        
        single_output_inner = tk.Frame(self.single_output_card, bg=self.bg_secondary)
        single_output_inner.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(single_output_inner, text="OUTPUT VIDEO", style="Small.TLabel").pack(anchor="w")
        
        output_frame = tk.Frame(single_output_inner, bg=self.bg_secondary)
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
        
    def create_batch_mode_widgets(self):
        # Batch Mode Input Folder Card
        self.batch_input_card = ttk.Frame(self.io_container, style="Card.TFrame")
        
        batch_input_inner = tk.Frame(self.batch_input_card, bg=self.bg_secondary)
        batch_input_inner.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(batch_input_inner, text="INPUT FOLDER", style="Small.TLabel").pack(anchor="w")
        
        input_folder_frame = tk.Frame(batch_input_inner, bg=self.bg_secondary)
        input_folder_frame.pack(fill="x", pady=(10, 0))
        
        self.input_folder_entry = tk.Entry(input_folder_frame,
                                          textvariable=self.input_folder,
                                          bg=self.bg_tertiary,
                                          fg=self.text_primary,
                                          insertbackground=self.text_primary,
                                          relief="flat",
                                          font=("Segoe UI", 10))
        self.input_folder_entry.pack(side="left", fill="x", expand=True, ipady=8)
        
        browse_input_folder_btn = tk.Button(input_folder_frame,
                                           text="Browse",
                                           bg=self.accent,
                                           fg=self.bg_primary,
                                           relief="flat",
                                           font=("Segoe UI", 10, "bold"),
                                           padx=20,
                                           cursor="hand2",
                                           command=self.browse_input_folder)
        browse_input_folder_btn.pack(side="right", padx=(10, 0))
        browse_input_folder_btn.bind("<Enter>", lambda e: browse_input_folder_btn.config(bg=self.accent_hover))
        browse_input_folder_btn.bind("<Leave>", lambda e: browse_input_folder_btn.config(bg=self.accent))
        
        # Batch Mode Output Folder Card
        self.batch_output_card = ttk.Frame(self.io_container, style="Card.TFrame")
        
        batch_output_inner = tk.Frame(self.batch_output_card, bg=self.bg_secondary)
        batch_output_inner.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(batch_output_inner, text="OUTPUT FOLDER", style="Small.TLabel").pack(anchor="w")
        
        output_folder_frame = tk.Frame(batch_output_inner, bg=self.bg_secondary)
        output_folder_frame.pack(fill="x", pady=(10, 0))
        
        self.output_folder_entry = tk.Entry(output_folder_frame,
                                           textvariable=self.output_folder,
                                           bg=self.bg_tertiary,
                                           fg=self.text_primary,
                                           insertbackground=self.text_primary,
                                           relief="flat",
                                           font=("Segoe UI", 10))
        self.output_folder_entry.pack(side="left", fill="x", expand=True, ipady=8)
        
        browse_output_folder_btn = tk.Button(output_folder_frame,
                                            text="Browse",
                                            bg=self.accent,
                                            fg=self.bg_primary,
                                            relief="flat",
                                            font=("Segoe UI", 10, "bold"),
                                            padx=20,
                                            cursor="hand2",
                                            command=self.browse_output_folder)
        browse_output_folder_btn.pack(side="right", padx=(10, 0))
        browse_output_folder_btn.bind("<Enter>", lambda e: browse_output_folder_btn.config(bg=self.accent_hover))
        browse_output_folder_btn.bind("<Leave>", lambda e: browse_output_folder_btn.config(bg=self.accent))
        
        # Files count label
        self.files_count_label = ttk.Label(batch_output_inner, text="", style="Small.TLabel")
        self.files_count_label.pack(anchor="w", pady=(10, 0))
    
    def create_convert_section(self):
        convert_frame = ttk.Frame(self.main_frame, style="Card.TFrame")
        convert_frame.pack(fill="x", pady=(0, 15))
        
        convert_inner = tk.Frame(convert_frame, bg=self.bg_secondary)
        convert_inner.pack(fill="x", padx=20, pady=20)
        
        ttk.Label(convert_inner, text="FORMAT CONVERSION", style="Small.TLabel").pack(anchor="w")
        
        formats_frame = tk.Frame(convert_inner, bg=self.bg_secondary)
        formats_frame.pack(fill="x", pady=(10, 0))
        
        formats = ["MP4", "AVI", "MOV", "MKV", "WMV", "FLV", "WEBM", "M4V"]
        
        # Create format selectors in a grid
        ttk.Label(formats_frame, text="From:", style="Dark.TLabel").grid(row=0, column=0, padx=(0, 10), pady=5, sticky="w")
        
        self.from_format_combo = ttk.Combobox(formats_frame, values=formats, state="readonly", width=10)
        self.from_format_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.from_format_combo.set("MP4")
        
        ttk.Label(formats_frame, text="To:", style="Dark.TLabel").grid(row=0, column=2, padx=(20, 10), pady=5, sticky="w")
        
        self.to_format_combo = ttk.Combobox(formats_frame, values=formats, state="readonly", width=10)
        self.to_format_combo.grid(row=0, column=3, padx=5, pady=5, sticky="ew")
        self.to_format_combo.set("MP4")
        
        formats_frame.grid_columnconfigure(1, weight=1)
        formats_frame.grid_columnconfigure(3, weight=1)
        
        # Convert button
        convert_btn = tk.Button(convert_inner,
                               text="CONVERT FORMAT",
                               bg=self.accent,
                               fg=self.bg_primary,
                               relief="flat",
                               font=("Segoe UI", 10, "bold"),
                               padx=20,
                               pady=8,
                               cursor="hand2",
                               command=self.convert_video)
        convert_btn.pack(fill="x", pady=(15, 0))
        convert_btn.bind("<Enter>", lambda e: convert_btn.config(bg=self.accent_hover))
        convert_btn.bind("<Leave>", lambda e: convert_btn.config(bg=self.accent))
    
    def toggle_mode(self):
        mode = self.compression_mode.get()
        
        # Hide all cards first
        self.single_input_card.pack_forget()
        self.single_output_card.pack_forget()
        self.batch_input_card.pack_forget()
        self.batch_output_card.pack_forget()
        self.current_file_label.pack_forget()
        self.current_file_progress_bar.pack_forget()
        
        if mode == "single":
            self.single_input_card.pack(fill="x", pady=(0, 15))
            self.single_output_card.pack(fill="x", pady=(0, 15))
            self.compress_btn.config(text="COMPRESS VIDEO")
        else:  # batch
            self.batch_input_card.pack(fill="x", pady=(0, 15))
            self.batch_output_card.pack(fill="x", pady=(0, 15))
            self.current_file_label.pack(anchor="w", pady=(10, 5))
            self.current_file_progress_bar.pack(fill="x", pady=(0, 5))
            self.compress_btn.config(text="COMPRESS BATCH")
            self.update_files_count()
        
        # Update scroll region after mode change
        self.root.after(10, self.update_scroll_region)
    
    def update_quality_label(self, value):
        self.quality_label.config(text=str(int(float(value))))
        
    def browse_input(self):
        filename = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv *.flv *.webm *.m4v"), ("All files", "*.*")]
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
    
    def browse_input_folder(self):
        folder = filedialog.askdirectory(title="Select Input Folder with Videos")
        if folder:
            self.input_folder.set(folder)
            if not self.output_folder.get():
                self.output_folder.set(os.path.join(folder, "compressed"))
            self.update_files_count()
    
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
    
    def browse_ffmpeg(self):
        filename = filedialog.askopenfilename(
            title="Select FFmpeg Executable",
            filetypes=[("FFmpeg executable", "ffmpeg.exe"), ("All files", "*.*")]
        )
        if filename:
            self.ffmpeg_path.set(filename)
    
    def update_files_count(self):
        if not self.input_folder.get():
            self.files_count_label.config(text="")
            return
        
        video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv', '*.flv', '*.webm', '*.m4v']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(glob.glob(os.path.join(self.input_folder.get(), ext)))
            video_files.extend(glob.glob(os.path.join(self.input_folder.get(), ext.upper())))
        
        count = len(video_files)
        self.files_count_label.config(text=f"Found {count} video files")
    
    def get_video_duration(self, filepath):
        try:
            cmd = [self.ffmpeg_path.get(), "-i", filepath]
            result = subprocess.run(cmd, stderr=subprocess.PIPE, text=True, timeout=30)
            duration_match = re.search(r'Duration: (\d{2}):(\d{2}):(\d{2})', result.stderr)
            if duration_match:
                hours, minutes, seconds = map(int, duration_match.groups())
                return hours * 3600 + minutes * 60 + seconds
        except:
            pass
        return None
    
    def get_batch_files(self):
        if not self.input_folder.get():
            return []
        
        video_extensions = ['*.mp4', '*.avi', '*.mov', '*.mkv', '*.wmv', '*.flv', '*.webm', '*.m4v']
        video_files = []
        
        for ext in video_extensions:
            video_files.extend(glob.glob(os.path.join(self.input_folder.get(), ext)))
            video_files.extend(glob.glob(os.path.join(self.input_folder.get(), ext.upper())))
        
        return sorted(video_files)
    
    def start_compression(self):
        if not os.path.exists(self.ffmpeg_path.get()):
            messagebox.showerror("Error", f"FFmpeg not found at {self.ffmpeg_path.get()}")
            return
        
        mode = self.compression_mode.get()
        
        if mode == "single":
            if not self.input_file.get():
                messagebox.showerror("Error", "Please select an input video file")
                return
            if not self.output_file.get():
                messagebox.showerror("Error", "Please specify an output file")
                return
        else:  # batch
            if not self.input_folder.get():
                messagebox.showerror("Error", "Please select an input folder")
                return
            if not self.output_folder.get():
                messagebox.showerror("Error", "Please specify an output folder")
                return
            
            self.batch_files = self.get_batch_files()
            if not self.batch_files:
                messagebox.showerror("Error", "No video files found in the input folder")
                return
            
            # Create output folder if it doesn't exist
            os.makedirs(self.output_folder.get(), exist_ok=True)
        
        self.is_processing = True
        self.compress_btn.config(state="disabled", bg=self.bg_tertiary, 
                               text="PROCESSING..." if mode == "single" else "PROCESSING BATCH...")
        self.progress.set(0)
        self.current_file_progress.set(0)
        
        if mode == "single":
            self.status_label.config(text="Processing video...")
            thread = threading.Thread(target=self.run_single_compression)
        else:
            self.current_batch_index = 0
            self.status_label.config(text=f"Processing batch: 0/{len(self.batch_files)} files")
            thread = threading.Thread(target=self.run_batch_compression)
        
        thread.daemon = True
        thread.start()
    
    def run_single_compression(self):
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
                    progress = min((current_time / duration) * 100, 100)
                    
                    self.root.after(0, self.update_single_progress, progress, f"Processing: {progress:.1f}%")
            
            process.wait()
            
            if process.returncode == 0:
                self.root.after(0, self.single_compression_complete)
            else:
                self.root.after(0, self.compression_failed, "Compression failed")
                
        except Exception as e:
            self.root.after(0, self.compression_failed, str(e))
    
    def run_batch_compression(self):
        try:
            total_files = len(self.batch_files)
            successful = 0
            failed = 0
            
            preset_settings = {
                "ultra": {"crf": 28, "preset": "faster"},
                "high": {"crf": 25, "preset": "fast"},
                "balanced": {"crf": self.quality.get(), "preset": "medium"},
                "quality": {"crf": 20, "preset": "slow"}
            }
            
            settings = preset_settings[self.preset.get()]
            
            for i, input_file in enumerate(self.batch_files):
                if not self.is_processing:  # Check if cancelled
                    break
                
                self.current_batch_index = i
                filename = os.path.basename(input_file)
                
                # Update UI
                self.root.after(0, self.update_batch_progress, 
                               (i / total_files) * 100, 
                               f"Processing: {i}/{total_files} files completed",
                               f"Current file: {filename}")
                
                # Generate output path
                input_path = Path(input_file)
                output_file = os.path.join(self.output_folder.get(), 
                                         f"{input_path.stem}_compressed{input_path.suffix}")
                
                # Skip if output file already exists
                if os.path.exists(output_file):
                    self.root.after(0, self.update_current_file_progress, 100, f"Skipped (already exists): {filename}")
                    continue
                
                cmd = [
                    self.ffmpeg_path.get(),
                    "-i", input_file,
                    "-c:v", "libx264",
                    "-crf", str(settings["crf"]),
                    "-preset", settings["preset"],
                    "-c:a", "aac",
                    "-b:a", "128k",
                    "-movflags", "+faststart",
                    "-y",
                    output_file
                ]
                
                duration = self.get_video_duration(input_file)
                
                try:
                    process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True, bufsize=1)
                    
                    for line in process.stderr:
                        if not self.is_processing:  # Check if cancelled
                            process.terminate()
                            break
                            
                        time_match = re.search(r'time=(\d{2}):(\d{2}):(\d{2})', line)
                        if time_match and duration:
                            hours, minutes, seconds = map(int, time_match.groups())
                            current_time = hours * 3600 + minutes * 60 + seconds
                            file_progress = min((current_time / duration) * 100, 100)
                            
                            self.root.after(0, self.update_current_file_progress, 
                                           file_progress, f"Compressing: {filename} ({file_progress:.1f}%)")
                    
                    process.wait()
                    
                    if process.returncode == 0:
                        successful += 1
                        self.root.after(0, self.update_current_file_progress, 100, f"Completed: {filename}")
                    else:
                        failed += 1
                        self.root.after(0, self.update_current_file_progress, 0, f"Failed: {filename}")
                        
                except Exception as e:
                    failed += 1
                    self.root.after(0, self.update_current_file_progress, 0, f"Error: {filename} - {str(e)}")
            
            # Final update
            if self.is_processing:  # Only if not cancelled
                self.root.after(0, self.batch_compression_complete, successful, failed, total_files)
            else:
                self.root.after(0, self.compression_cancelled)
                
        except Exception as e:
            self.root.after(0, self.compression_failed, str(e))
    
    def update_single_progress(self, value, text):
        self.progress.set(value)
        self.progress_text.config(text=text)
    
    def update_batch_progress(self, overall_progress, overall_text, current_file_text):
        self.progress.set(overall_progress)
        self.progress_text.config(text=overall_text)
        self.current_file_label.config(text=current_file_text)
    
    def update_current_file_progress(self, value, text):
        self.current_file_progress.set(value)
        self.current_file_label.config(text=text)
    
    def single_compression_complete(self):
        self.is_processing = False
        self.compress_btn.config(state="normal", bg=self.accent, text="COMPRESS VIDEO")
        self.progress.set(100)
        self.status_label.config(text="✓ Compression complete!", foreground=self.success)
        self.progress_text.config(text="Video saved successfully")
        
        try:
            input_size = os.path.getsize(self.input_file.get()) / (1024 * 1024)
            output_size = os.path.getsize(self.output_file.get()) / (1024 * 1024)
            reduction = ((input_size - output_size) / input_size) * 100
            
            messagebox.showinfo("Success", 
                              f"Video compressed successfully!\n\n"
                              f"Original: {input_size:.1f} MB\n"
                              f"Compressed: {output_size:.1f} MB\n"
                              f"Size reduction: {reduction:.1f}%")
        except:
            messagebox.showinfo("Success", "Video compressed successfully!")
    
    def batch_compression_complete(self, successful, failed, total):
        self.is_processing = False
        self.compress_btn.config(state="normal", bg=self.accent, text="COMPRESS BATCH")
        self.progress.set(100)
        self.current_file_progress.set(100)
        
        if failed == 0:
            self.status_label.config(text="✓ Batch compression complete!", foreground=self.success)
            self.progress_text.config(text=f"All {successful} files processed successfully")
            self.current_file_label.config(text="Batch processing completed")
        else:
            self.status_label.config(text="⚠ Batch compression completed with errors", foreground="#ffaa00")
            self.progress_text.config(text=f"{successful} successful, {failed} failed out of {total} files")
            self.current_file_label.config(text="Check individual file results")
        
        # Calculate total size reduction if possible
        try:
            total_input_size = 0
            total_output_size = 0
            
            for input_file in self.batch_files:
                if os.path.exists(input_file):
                    total_input_size += os.path.getsize(input_file)
                    
                    input_path = Path(input_file)
                    output_file = os.path.join(self.output_folder.get(), 
                                             f"{input_path.stem}_compressed{input_path.suffix}")
                    if os.path.exists(output_file):
                        total_output_size += os.path.getsize(output_file)
            
            if total_input_size > 0 and total_output_size > 0:
                total_input_mb = total_input_size / (1024 * 1024)
                total_output_mb = total_output_size / (1024 * 1024)
                total_reduction = ((total_input_size - total_output_size) / total_input_size) * 100
                
                messagebox.showinfo("Batch Compression Complete", 
                                  f"Batch processing finished!\n\n"
                                  f"Files processed: {successful}/{total}\n"
                                  f"Failed: {failed}\n\n"
                                  f"Total original size: {total_input_mb:.1f} MB\n"
                                  f"Total compressed size: {total_output_mb:.1f} MB\n"
                                  f"Total size reduction: {total_reduction:.1f}%\n\n"
                                  f"Output folder: {self.output_folder.get()}")
            else:
                messagebox.showinfo("Batch Compression Complete", 
                                  f"Batch processing finished!\n\n"
                                  f"Files processed: {successful}/{total}\n"
                                  f"Failed: {failed}\n\n"
                                  f"Output folder: {self.output_folder.get()}")
        except:
            messagebox.showinfo("Batch Compression Complete", 
                              f"Batch processing finished!\n\n"
                              f"Files processed: {successful}/{total}\n"
                              f"Failed: {failed}\n\n"
                              f"Output folder: {self.output_folder.get()}")
    
    def compression_failed(self, error):
        self.is_processing = False
        mode = self.compression_mode.get()
        self.compress_btn.config(state="normal", bg=self.accent, 
                               text="COMPRESS VIDEO" if mode == "single" else "COMPRESS BATCH")
        self.status_label.config(text="✗ Compression failed", foreground=self.error)
        self.progress_text.config(text=error)
        messagebox.showerror("Error", f"Compression failed:\n{error}")
    
    def compression_cancelled(self):
        self.is_processing = False
        mode = self.compression_mode.get()
        self.compress_btn.config(state="normal", bg=self.accent, 
                               text="COMPRESS VIDEO" if mode == "single" else "COMPRESS BATCH")
        self.status_label.config(text="Compression cancelled", foreground="#ffaa00")
        self.progress_text.config(text="Operation was cancelled by user")
    
    def convert_video(self):
        mode = self.compression_mode.get()
        
        if mode == "single":
            if not self.input_file.get():
                messagebox.showerror("Error", "Please select a video file first")
                return
            selected_file = self.input_file.get()
        else:
            messagebox.showerror("Error", "Format conversion only works in Single File mode")
            return
            
        try:
            self.progress.set(20)
            self.status_label.config(text="Starting format conversion...")
            
            from_fmt = self.from_format_combo.get().lower()
            to_fmt = self.to_format_combo.get().lower()
            
            # Generate output path
            input_path = Path(selected_file)
            output_path = input_path.parent / f"{input_path.stem}_converted.{to_fmt.lower()}"
            
            cmd = [
                self.ffmpeg_path.get(),
                "-i", selected_file,
                "-c:v", "copy" if from_fmt == to_fmt else "libx264",
                "-c:a", "copy" if from_fmt == to_fmt else "aac",
                "-y",
                str(output_path)
            ]
            
            process = subprocess.run(cmd, capture_output=True, text=True)
            
            if process.returncode == 0:
                self.progress.set(100)
                self.status_label.config(text="✓ Format conversion complete!", foreground=self.success)
                self.progress_text.config(text=f"Video converted and saved to: {output_path}")
                messagebox.showinfo("Success", f"Video converted successfully!\n\nSaved to:\n{output_path}")
            else:
                raise Exception(process.stderr)
                
        except Exception as e:
            self.status_label.config(text="✗ Conversion failed", foreground=self.error)
            self.progress_text.config(text=f"Conversion error: {str(e)}")
            messagebox.showerror("Error", f"Failed to convert video:\n{str(e)}")
        finally:
            self.progress.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoCompressor(root)
    root.mainloop()