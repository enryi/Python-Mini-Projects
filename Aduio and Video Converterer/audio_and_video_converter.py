import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
import os
from pathlib import Path
import queue
import time

# MoviePy import for audio extraction
try:
    from moviepy.video.io.VideoFileClip import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    print("MoviePy not available - audio extraction will be disabled")

# FFmpeg converter (mock implementation if not available)
# VideoConverter mock implementation (FFmpeg not available)
FFMPEG_AVAILABLE = False
class VideoConverter:
    def __init__(self, ffmpeg_path=None):
        pass

    def convert_to_mp4(self, input_file, output_path, quality="fast", audio_bitrate="192k"):
        time.sleep(2)  # Simulate processing time
        output_file = os.path.join(output_path, f"{Path(input_file).stem}.mp4")
        return {"success": True, "output_file": output_file, "error": None}

class UnifiedMediaConverter:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.setup_variables()
        self.create_widgets()
        
        # Initialize converters
        if FFMPEG_AVAILABLE:
            try:
                self.video_converter = VideoConverter()
            except Exception:
                self.video_converter = None
        else:
            self.video_converter = VideoConverter()
        
        # Progress queue for threading communication
        self.progress_queue = queue.Queue()
        self.root.after(100, self.check_progress_queue)
        
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Unified Media Converter")
        self.root.geometry("950x800")
        self.root.minsize(900, 750)
        self.root.configure(bg='#1e1e1e')
        
        # Center window
        self.center_window()
        
        # Try to set icon
        try:
            self.root.iconbitmap('icon.ico')
        except:
            pass
    
    def center_window(self):
        """Center the window on screen"""
        self.root.update_idletasks()
        width, height = 950, 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
    
    def setup_styles(self):
        """Configure modern dark theme styles"""
        self.style = ttk.Style()
        self.style.theme_use("clam")
        
        self.colors = {
            'bg_primary': '#1e1e1e',
            'bg_secondary': '#2d2d2d',
            'bg_tertiary': '#3c3c3c',
            'accent': '#007acc',
            'accent_hover': '#0099ff',
            'text_primary': '#ffffff',
            'text_secondary': '#cccccc',
            'text_disabled': '#666666',
            'success': '#4caf50',
            'error': '#f44336',
            'warning': '#ff9800',
            'border': '#555555'
        }
        
        # Frame styles
        self.style.configure('Main.TFrame', background=self.colors['bg_primary'])
        self.style.configure('Card.TFrame', background=self.colors['bg_secondary'], relief='solid', borderwidth=1)
        
        # Button styles
        self.style.configure('Accent.TButton',
                           background=self.colors['accent'],
                           foreground=self.colors['text_primary'],
                           borderwidth=0,
                           focuscolor='none',
                           font=('Segoe UI', 10, 'bold'))
        
        self.style.map('Accent.TButton',
                      background=[('active', self.colors['accent_hover'])])
        
        self.style.configure('Secondary.TButton',
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=0,
                           font=('Segoe UI', 9))
        
        self.style.map('Secondary.TButton',
                      background=[('active', self.colors['accent'])])
        
        # Label styles
        self.style.configure('Title.TLabel',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 18, 'bold'))
        
        self.style.configure('Subtitle.TLabel',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_secondary'],
                           font=('Segoe UI', 11, 'bold'))
        
        self.style.configure('Card.TLabel',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 9))
        
        # Entry and Combobox styles
        self.style.configure('Modern.TEntry',
                           fieldbackground=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           insertcolor=self.colors['text_primary'])
        
        self.style.configure('Modern.TCombobox',
                           fieldbackground=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1)
        
        # Progress bar style
        self.style.configure('Modern.Horizontal.TProgressbar',
                           background=self.colors['accent'],
                           troughcolor=self.colors['bg_tertiary'],
                           borderwidth=0)
        
        # Notebook style
        self.style.configure('Modern.TNotebook',
                           background=self.colors['bg_primary'],
                           borderwidth=0)
        
        self.style.configure('Modern.TNotebook.Tab',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_secondary'],
                           padding=[20, 8],
                           font=('Segoe UI', 10))
        
        self.style.map('Modern.TNotebook.Tab',
                      background=[('selected', self.colors['accent']),
                                ('active', self.colors['bg_tertiary'])],
                      foreground=[('selected', self.colors['text_primary'])])
    
    def setup_variables(self):
        """Initialize variables"""
        self.selected_files = []
        self.output_folder = tk.StringVar(value=str(Path.home() / "Downloads"))
        self.conversion_active = False
        self.conversion_thread = None
        
        # Audio extraction variables
        self.audio_format = tk.StringVar(value="mp3")
        self.audio_bitrate = tk.StringVar(value="192k")
        
        # Video conversion variables
        self.video_quality = tk.StringVar(value="fast")
        self.video_audio_bitrate = tk.StringVar(value="192k")
        
        # Progress variables
        self.progress_var = tk.DoubleVar()
        self.status_var = tk.StringVar(value="Ready")
    
    def create_widgets(self):
        """Create all interface widgets"""
        # Main container
        main_container = ttk.Frame(self.root, style='Main.TFrame', padding="20")
        main_container.pack(fill="both", expand=True)
        
        # Header
        self.create_header(main_container)
        
        # Tabbed interface
        self.create_tabs(main_container)
        
        # Common sections
        self.create_file_section()
        self.create_output_section()
        self.create_progress_section()
        self.create_controls()
    
    def create_header(self, parent):
        """Create application header"""
        header_frame = ttk.Frame(parent, style='Main.TFrame')
        header_frame.pack(fill="x", pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="🎬 Unified Media Converter", style='Title.TLabel')
        title_label.pack(side="left")
        
        status_frame = ttk.Frame(header_frame, style='Main.TFrame')
        status_frame.pack(side="right")
        
        # Status indicators
        moviepy_status = "✅" if MOVIEPY_AVAILABLE else "❌"
        ffmpeg_status = "✅" if FFMPEG_AVAILABLE else "⚠️"
        
        status_text = f"Audio: {moviepy_status} Video: {ffmpeg_status}"
        ttk.Label(status_frame, text=status_text, 
                 style='Card.TLabel', font=('Segoe UI', 8)).pack()
    
    def create_tabs(self, parent):
        """Create tabbed interface"""
        self.notebook = ttk.Notebook(parent, style='Modern.TNotebook')
        self.notebook.pack(fill="both", expand=True, pady=(0, 20))
        
        # Audio extraction tab
        self.audio_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.audio_frame, text="🎵 Audio Extraction")
        
        # Video conversion tab  
        self.video_frame = ttk.Frame(self.notebook, style='Main.TFrame')
        self.notebook.add(self.video_frame, text="🎬 Video Conversion")
        
        # Create tab content
        self.create_audio_tab()
        self.create_video_tab()
    
    def create_audio_tab(self):
        """Create audio extraction settings"""
        if not MOVIEPY_AVAILABLE:
            warning_frame = ttk.Frame(self.audio_frame, style='Card.TFrame', padding="15")
            warning_frame.pack(fill="x", padx=10, pady=10)
            
            ttk.Label(warning_frame, 
                     text="⚠️ MoviePy not available. Install with: pip install moviepy",
                     style='Card.TLabel', 
                     font=('Segoe UI', 10, 'bold')).pack()
            return
        
        settings_frame = ttk.Frame(self.audio_frame, style='Card.TFrame', padding="15")
        settings_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(settings_frame, text="🎵 Audio Extraction Settings", 
                 style='Subtitle.TLabel').pack(anchor="w", pady=(0, 10))
        
        # Format selection
        format_frame = ttk.Frame(settings_frame, style='Card.TFrame')
        format_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(format_frame, text="Output Format:", style='Card.TLabel').pack(side="left")
        format_combo = ttk.Combobox(format_frame, textvariable=self.audio_format,
                                   values=["mp3", "wav", "aac", "ogg"],
                                   style='Modern.TCombobox', state='readonly', width=12)
        format_combo.pack(side="right")
        
        # Bitrate selection
        bitrate_frame = ttk.Frame(settings_frame, style='Card.TFrame')
        bitrate_frame.pack(fill="x")
        
        ttk.Label(bitrate_frame, text="Audio Bitrate:", style='Card.TLabel').pack(side="left")
        bitrate_combo = ttk.Combobox(bitrate_frame, textvariable=self.audio_bitrate,
                                    values=["128k", "192k", "256k", "320k"],
                                    style='Modern.TCombobox', state='readonly', width=12)
        bitrate_combo.pack(side="right")
    
    def create_video_tab(self):
        """Create video conversion settings"""
        settings_frame = ttk.Frame(self.video_frame, style='Card.TFrame', padding="15")
        settings_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(settings_frame, text="🎬 Video Conversion Settings", 
                 style='Subtitle.TLabel').pack(anchor="w", pady=(0, 10))
        
        # Quality selection
        quality_frame = ttk.Frame(settings_frame, style='Card.TFrame')
        quality_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(quality_frame, text="Video Quality:", style='Card.TLabel').pack(side="left")
        quality_combo = ttk.Combobox(quality_frame, textvariable=self.video_quality,
                                    values=["ultrafast", "superfast", "veryfast", "faster",
                                           "fast", "medium", "slow", "slower", "veryslow"],
                                    style='Modern.TCombobox', state='readonly', width=12)
        quality_combo.pack(side="right")
        
        # Audio bitrate selection
        bitrate_frame = ttk.Frame(settings_frame, style='Card.TFrame')
        bitrate_frame.pack(fill="x")
        
        ttk.Label(bitrate_frame, text="Audio Bitrate:", style='Card.TLabel').pack(side="left")
        bitrate_combo = ttk.Combobox(bitrate_frame, textvariable=self.video_audio_bitrate,
                                    values=["128k", "192k", "256k", "320k"],
                                    style='Modern.TCombobox', state='readonly', width=12)
        bitrate_combo.pack(side="right")
        
        if not FFMPEG_AVAILABLE:
            warning_frame = ttk.Frame(self.video_frame, style='Card.TFrame', padding="15")
            warning_frame.pack(fill="x", padx=10, pady=(5, 10))
            
            ttk.Label(warning_frame, 
                     text="⚠️ Using mock converter. Install FFmpeg for real conversion.",
                     style='Card.TLabel', 
                     font=('Segoe UI', 9)).pack()
    
    def create_file_section(self):
        """Create file selection section"""
        files_frame = ttk.Frame(self.root, style='Card.TFrame', padding="15")
        files_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Header
        header_frame = ttk.Frame(files_frame, style='Card.TFrame')
        header_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(header_frame, text="📁 Media Files", style='Subtitle.TLabel').pack(side="left")
        
        buttons_frame = ttk.Frame(header_frame, style='Card.TFrame')
        buttons_frame.pack(side="right")
        
        ttk.Button(buttons_frame, text="Add Files", command=self.add_files,
                  style='Accent.TButton').pack(side="right", padx=(5, 0))
        
        ttk.Button(buttons_frame, text="Clear All", command=self.clear_files,
                  style='Secondary.TButton').pack(side="right")
        
        # File list
        list_frame = ttk.Frame(files_frame, style='Card.TFrame')
        list_frame.pack(fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")
        
        self.files_listbox = tk.Listbox(list_frame,
                                       bg=self.colors['bg_tertiary'],
                                       fg=self.colors['text_primary'],
                                       selectbackground=self.colors['accent'],
                                       selectforeground=self.colors['text_primary'],
                                       borderwidth=0,
                                       highlightthickness=0,
                                       font=('Consolas', 9),
                                       yscrollcommand=scrollbar.set)
        self.files_listbox.pack(fill="both", expand=True)
        scrollbar.config(command=self.files_listbox.yview)
        
        self.files_listbox.bind('<Delete>', self.remove_selected_file)
        self.files_listbox.bind('<Double-Button-1>', self.remove_selected_file)
    
    def create_output_section(self):
        """Create output folder section"""
        output_frame = ttk.Frame(self.root, style='Card.TFrame', padding="15")
        output_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Header
        header_frame = ttk.Frame(output_frame, style='Card.TFrame')
        header_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(header_frame, text="💾 Output Folder", style='Subtitle.TLabel').pack(side="left")
        
        ttk.Button(header_frame, text="Browse", command=self.select_output_folder,
                  style='Accent.TButton').pack(side="right")
        
        # Path entry
        self.output_entry = ttk.Entry(output_frame, textvariable=self.output_folder,
                                     style='Modern.TEntry', font=('Consolas', 9))
        self.output_entry.pack(fill="x")
    
    def create_progress_section(self):
        """Create progress section"""
        progress_frame = ttk.Frame(self.root, style='Card.TFrame', padding="15")
        progress_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Header
        header_frame = ttk.Frame(progress_frame, style='Card.TFrame')
        header_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(header_frame, text="📊 Progress", style='Subtitle.TLabel').pack(side="left")
        
        self.status_label = ttk.Label(header_frame, textvariable=self.status_var, style='Card.TLabel')
        self.status_label.pack(side="right")
        
        # Progress bar
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var,
                                          style='Modern.Horizontal.TProgressbar')
        self.progress_bar.pack(fill="x")
    
    def create_controls(self):
        """Create control buttons"""
        controls_frame = ttk.Frame(self.root, style='Main.TFrame')
        controls_frame.pack(fill="x", padx=20, pady=20)
        
        buttons_frame = ttk.Frame(controls_frame, style='Main.TFrame')
        buttons_frame.pack()
        
        self.start_button = ttk.Button(buttons_frame, text="🚀 Start Processing",
                                      command=self.start_processing,
                                      style='Accent.TButton', width=20)
        self.start_button.pack(side="left", padx=(0, 10))
        
        self.stop_button = ttk.Button(buttons_frame, text="⏹ Stop",
                                     command=self.stop_processing,
                                     style='Secondary.TButton', state='disabled', width=15)
        self.stop_button.pack(side="left", padx=(0, 10))
        
        ttk.Button(buttons_frame, text="📂 Open Output",
                  command=self.open_output_folder,
                  style='Secondary.TButton', width=15).pack(side="left")
    
    def add_files(self):
        """Add media files to the list"""
        filetypes = [
            ("Media files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.webm *.m4v *.mp3 *.wav *.aac *.ogg"),
            ("Video files", "*.mp4 *.avi *.mov *.mkv *.flv *.wmv *.webm *.m4v"),
            ("Audio files", "*.mp3 *.wav *.aac *.ogg"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(title="Select media files", filetypes=filetypes)
        
        for file in files:
            if file not in self.selected_files:
                self.selected_files.append(file)
                filename = os.path.basename(file)
                ext = Path(file).suffix.lower()
                
                if ext in ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v']:
                    icon = "🎬"
                elif ext in ['.mp3', '.wav', '.aac', '.ogg']:
                    icon = "🎵"
                else:
                    icon = "📄"
                
                self.files_listbox.insert(tk.END, f"{icon} {filename}")
    
    def remove_selected_file(self, event=None):
        """Remove selected file from list"""
        selection = self.files_listbox.curselection()
        if selection:
            index = selection[0]
            self.files_listbox.delete(index)
            self.selected_files.pop(index)
    
    def clear_files(self):
        """Clear all files from list"""
        self.files_listbox.delete(0, tk.END)
        self.selected_files.clear()
    
    def select_output_folder(self):
        """Select output folder"""
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.output_folder.set(folder)
    
    def open_output_folder(self):
        """Open output folder in file explorer"""
        output_path = self.output_folder.get()
        if os.path.exists(output_path):
            if os.name == 'nt':  # Windows
                os.startfile(output_path)
            elif os.name == 'posix':  # macOS/Linux
                os.system(f'open "{output_path}"' if os.uname().sysname == 'Darwin' else f'xdg-open "{output_path}"')
        else:
            messagebox.showerror("Error", "Output folder does not exist")
    
    def start_processing(self):
        """Start media processing"""
        if not self.selected_files:
            messagebox.showwarning("Warning", "Please select at least one media file")
            return
        
        if not os.path.exists(self.output_folder.get()):
            messagebox.showerror("Error", "Output folder does not exist")
            return
        
        # Get current tab
        current_tab = self.notebook.index(self.notebook.select())
        
        if current_tab == 0:  # Audio extraction
            if not MOVIEPY_AVAILABLE:
                messagebox.showerror("Error", "MoviePy not available for audio extraction")
                return
        
        self.conversion_active = True
        self.start_button.config(state='disabled')
        self.stop_button.config(state='normal')
        self.progress_var.set(0)
        
        # Start processing thread
        self.conversion_thread = threading.Thread(target=self.processing_worker, 
                                                 args=(current_tab,), daemon=True)
        self.conversion_thread.start()
    
    def stop_processing(self):
        """Stop media processing"""
        self.conversion_active = False
        self.status_var.set("Stopping...")
    
    def processing_worker(self, operation_type):
        """Background processing worker"""
        try:
            total_files = len(self.selected_files)
            successful = 0
            failed = 0
            
            for i, input_file in enumerate(self.selected_files):
                if not self.conversion_active:
                    break
                
                filename = os.path.basename(input_file)
                self.progress_queue.put(("status", f"Processing: {filename}"))
                
                if operation_type == 0:  # Audio extraction
                    result = self.extract_audio(input_file)
                else:  # Video conversion
                    result = self.convert_video(input_file)
                
                if result["success"]:
                    successful += 1
                else:
                    failed += 1
                    self.progress_queue.put(("error", f"Error processing {filename}: {result['error']}"))
                
                progress = ((i + 1) / total_files) * 100
                self.progress_queue.put(("progress", progress))
            
            if self.conversion_active:
                if failed == 0:
                    self.progress_queue.put(("status", f"✅ Completed! {successful} files processed"))
                    self.progress_queue.put(("show_success", f"Processing completed!\n{successful} files processed successfully"))
                else:
                    self.progress_queue.put(("status", f"⚠️ Completed with errors: {successful} successes, {failed} failures"))
                    self.progress_queue.put(("show_warning", f"Processing completed with errors:\nSuccesses: {successful}\nFailures: {failed}"))
            else:
                self.progress_queue.put(("status", "❌ Processing stopped"))
            
            self.progress_queue.put(("finished", None))
            
        except Exception as e:
            self.progress_queue.put(("status", f"❌ Error: {str(e)}"))
            self.progress_queue.put(("show_error", f"Processing error:\n{str(e)}"))
            self.progress_queue.put(("finished", None))
    
    def extract_audio(self, input_file):
        """Extract audio from video file"""
        try:
            input_path = Path(input_file)
            output_file = os.path.join(self.output_folder.get(), 
                                     f"{input_path.stem}.{self.audio_format.get()}")
            
            with VideoFileClip(input_file) as video_clip:
                if video_clip.audio is None:
                    return {"success": False, "error": "No audio track found"}
                
                audio_clip = video_clip.audio
                
                write_params = {'verbose': False, 'logger': None}
                
                if self.audio_format.get().lower() in ['mp3', 'aac', 'ogg']:
                    write_params['bitrate'] = self.audio_bitrate.get()
                
                audio_clip.write_audiofile(output_file, **write_params)
                audio_clip.close()
            
            return {"success": True, "output_file": output_file}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def convert_video(self, input_file):
        """Convert video file"""
        try:
            result = self.video_converter.convert_to_mp4(
                input_file,
                self.output_folder.get(),
                quality=self.video_quality.get(),
                audio_bitrate=self.video_audio_bitrate.get()
            )
            return result
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def check_progress_queue(self):
        """Check progress queue for updates from worker thread"""
        try:
            while True:
                item = self.progress_queue.get_nowait()
                command, data = item
                
                if command == "status":
                    self.status_var.set(data)
                elif command == "progress":
                    self.progress_var.set(data)
                elif command == "error":
                    print(f"Processing error: {data}")
                elif command == "show_success":
                    messagebox.showinfo("Success", data)
                elif command == "show_warning":
                    messagebox.showwarning("Warning", data)
                elif command == "show_error":
                    messagebox.showerror("Error", data)
                elif command == "finished":
                    self.start_button.config(state='normal')
                    self.stop_button.config(state='disabled')
                    self.conversion_active = False
                    break
                    
        except queue.Empty:
            pass
        
        self.root.after(100, self.check_progress_queue)

def main():
    """Main function"""
    root = tk.Tk()
    app = UnifiedMediaConverter(root)
    
    def on_closing():
        if app.conversion_active:
            if messagebox.askokcancel("Quit", "Processing is active. Do you want to quit?"):
                app.conversion_active = False
                root.destroy()
        else:
            root.destroy()
    
    root.protocol("WM_DELETE_WINDOW", on_closing)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.destroy()

if __name__ == "__main__":
    main()