import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import re
from pathlib import Path
import yt_dlp as youtube_dl
import math
import time

class VideoDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.setup_variables()
        
        self.urls_list = []
        
    def setup_window(self):
        """Configures the main window"""
        self.root.title("Video Downloader")
        self.root.geometry("1000x800")
        self.root.minsize(900, 700)
        
        self.colors = {
            'bg_primary': '#1a1a1a',
            'bg_secondary': '#2b2b2b',
            'bg_tertiary': '#353535',
            'bg_hover': '#404040',
            'accent': '#0078d4',
            'accent_hover': '#106ebe',
            'accent_secondary': '#ff6b35',
            'accent_secondary_hover': '#e85a2b',
            'text_primary': '#ffffff',
            'text_secondary': '#b3b3b3',
            'text_disabled': '#666666',
            'success': '#00d4aa',
            'error': '#ff5757',
            'warning': '#ffab00',
            'border': '#404040',
            'border_focus': '#0078d4'
        }
        
        self.root.configure(bg=self.colors['bg_primary'])
        
    def setup_styles(self):
        """Configures styles for the widgets"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        self.style.configure('Dark.TFrame', 
                           background=self.colors['bg_primary'],
                           relief='flat')
        
        self.style.configure('Card.TFrame', 
                           background=self.colors['bg_secondary'],
                           relief='flat',
                           borderwidth=0)
        
        self.style.configure('Dark.TButton',
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           focuscolor='none',
                           relief='flat',
                           padding=(12, 8))
        
        self.style.map('Dark.TButton',
                      background=[('active', self.colors['bg_hover']),
                                ('pressed', self.colors['bg_tertiary'])],
                      bordercolor=[('focus', self.colors['border_focus'])])
        
        self.style.configure('Accent.TButton',
                           background=self.colors['accent'],
                           foreground=self.colors['text_primary'],
                           borderwidth=0,
                           focuscolor='none',
                           relief='flat',
                           padding=(12, 8))
        
        self.style.map('Accent.TButton',
                      background=[('active', self.colors['accent_hover']),
                                ('pressed', self.colors['accent'])])
        
        self.style.configure('Secondary.TButton',
                           background=self.colors['accent_secondary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=0,
                           focuscolor='none',
                           relief='flat',
                           padding=(12, 8))
        
        self.style.map('Secondary.TButton',
                      background=[('active', self.colors['accent_secondary_hover']),
                                ('pressed', self.colors['accent_secondary'])])
        
        self.style.configure('Title.TLabel',
                           background=self.colors['bg_primary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 18, 'bold'))
        
        self.style.configure('Subtitle.TLabel',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_primary'],
                           font=('Segoe UI', 11, 'bold'))
        
        self.style.configure('Dark.TLabel',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_secondary'])
        
        self.style.configure('Status.TLabel',
                           background=self.colors['bg_secondary'],
                           foreground=self.colors['text_secondary'],
                           font=('Segoe UI', 9))
        
        self.style.configure('Dark.TEntry',
                           fieldbackground=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           insertcolor=self.colors['text_primary'],
                           relief='flat',
                           padding=8)
        
        self.style.map('Dark.TEntry',
                      focuscolor=[('focus', self.colors['border_focus'])],
                      bordercolor=[('focus', self.colors['border_focus'])])
        
        self.style.configure('Dark.TCombobox',
                           fieldbackground=self.colors['bg_tertiary'],
                           foreground=self.colors['text_primary'],
                           borderwidth=1,
                           relief='flat',
                           padding=8)
        
        self.style.map('Dark.TCombobox',
                      focuscolor=[('focus', self.colors['border_focus'])],
                      bordercolor=[('focus', self.colors['border_focus'])])
        
        self.style.configure('Dark.Horizontal.TProgressbar',
                           background=self.colors['accent'],
                           troughcolor=self.colors['bg_tertiary'],
                           borderwidth=0,
                           lightcolor=self.colors['accent'],
                           darkcolor=self.colors['accent'])
        
        self.style.configure('Dark.TNotebook',
                           background=self.colors['bg_primary'],
                           borderwidth=0,
                           tabmargins=[0, 0, 0, 0])
        
        self.style.configure('Dark.TNotebook.Tab',
                           background=self.colors['bg_tertiary'],
                           foreground=self.colors['text_secondary'],
                           padding=[16, 12],
                           borderwidth=0,
                           focuscolor='none')
        
        self.style.map('Dark.TNotebook.Tab',
                      background=[('selected', self.colors['accent']),
                                ('active', self.colors['bg_hover'])],
                      foreground=[('selected', self.colors['text_primary']),
                                ('active', self.colors['text_primary'])])
        
    def create_widgets(self):
        """Creates all interface widgets"""
        main_frame = ttk.Frame(self.root, style='Dark.TFrame', padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        title_label = ttk.Label(main_frame, text="Video Downloader", style='Title.TLabel')
        title_label.grid(row=0, column=0, pady=(0, 20), sticky=tk.W)
        
        self.notebook = ttk.Notebook(main_frame, style='Dark.TNotebook')
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        self.create_download_tab()
        self.create_audio_tab()
        self.create_batch_tab()
        self.create_info_tab()
        
    def create_download_tab(self):
        """Creates the video download tab"""
        tab_frame = ttk.Frame(self.notebook, style='Dark.TFrame', padding="20")
        self.notebook.add(tab_frame, text="Video")
        
        tab_frame.columnconfigure(0, weight=1)
        
        self.create_url_input_card(tab_frame, row=0)
        self.create_video_settings_card(tab_frame, row=1)
        self.create_output_card(tab_frame, row=2, card_id="video")
        self.create_progress_card(tab_frame, row=3, card_id="video")
        self.create_video_control_buttons(tab_frame, row=4)
        
    def create_audio_tab(self):
        """Creates the audio download tab"""
        tab_frame = ttk.Frame(self.notebook, style='Dark.TFrame', padding="20")
        self.notebook.add(tab_frame, text="Audio")
        
        tab_frame.columnconfigure(0, weight=1)
        
        self.create_url_input_card(tab_frame, row=0, tab_type="audio")
        self.create_audio_settings_card(tab_frame, row=1)
        self.create_output_card(tab_frame, row=2, card_id="audio")
        self.create_progress_card(tab_frame, row=3, card_id="audio")
        self.create_audio_control_buttons(tab_frame, row=4)
        
    def create_batch_tab(self):
        """Creates the batch download tab"""
        tab_frame = ttk.Frame(self.notebook, style='Dark.TFrame', padding="20")
        self.notebook.add(tab_frame, text="Batch")
        
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure(0, weight=1)
        
        self.create_url_list_card(tab_frame, row=0)
        self.create_batch_settings_card(tab_frame, row=1)
        self.create_output_card(tab_frame, row=2, card_id="batch")
        self.create_progress_card(tab_frame, row=3, card_id="batch")
        self.create_batch_control_buttons(tab_frame, row=4)
        
    def create_info_tab(self):
        """Creates the video info tab"""
        tab_frame = ttk.Frame(self.notebook, style='Dark.TFrame', padding="20")
        self.notebook.add(tab_frame, text="Info")
        
        tab_frame.columnconfigure(0, weight=1)
        tab_frame.rowconfigure(1, weight=1)
        
        self.create_url_input_card(tab_frame, row=0, tab_type="info")
        self.create_info_display_card(tab_frame, row=1)
        self.create_info_control_buttons(tab_frame, row=2)
        
    def create_url_input_card(self, parent, row, tab_type="video"):
        """Creates the URL input section"""
        card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        card.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        card.columnconfigure(1, weight=1)
        
        titles = {
            "video": "Video URL",
            "audio": "Audio URL", 
            "info": "URL for Information"
        }
        title = ttk.Label(card, text=titles.get(tab_type, "URL"), style='Subtitle.TLabel')
        title.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))
        
        ttk.Label(card, text="URL:", style='Dark.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 15))
        
        url_var_name = f"url_var_{tab_type}"
        setattr(self, url_var_name, tk.StringVar())
        url_var = getattr(self, url_var_name)
        
        url_entry = ttk.Entry(card, textvariable=url_var, style='Dark.TEntry', font=('Segoe UI', 10))
        url_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 15))
        
        ttk.Button(card, text="Paste", 
                  command=lambda: self.paste_url(url_var),
                  style='Dark.TButton').grid(row=1, column=2)
        
        validation_var_name = f"url_validation_var_{tab_type}"
        setattr(self, validation_var_name, tk.StringVar())
        validation_var = getattr(self, validation_var_name)
        
        validation_label = ttk.Label(card, textvariable=validation_var, style='Status.TLabel')
        validation_label.grid(row=2, column=1, sticky=tk.W, pady=(10, 0))
        
        url_var.trace('w', lambda *args: self.validate_url(url_var, validation_var))
        
    def create_video_settings_card(self, parent, row):
        """Creates the video settings section"""
        card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        card.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        card.columnconfigure(1, weight=1)
        card.columnconfigure(3, weight=1)
        
        title = ttk.Label(card, text="Video Settings", style='Subtitle.TLabel')
        title.grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 15))
        
        ttk.Label(card, text="Quality:", style='Dark.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 15))
        self.video_quality_var = tk.StringVar(value="1080p")
        quality_combo = ttk.Combobox(card, textvariable=self.video_quality_var, 
                                   values=["best", "2160p", "1440p", "1080p", "720p", "480p", "360p", "240p", "144p"], 
                                   style='Dark.TCombobox', state='readonly', width=15, font=('Segoe UI', 10))
        quality_combo.grid(row=1, column=1, sticky=tk.W, padx=(0, 30))
        
        ttk.Label(card, text="Format:", style='Dark.TLabel').grid(row=1, column=2, sticky=tk.W, padx=(0, 15))
        self.video_format_var = tk.StringVar(value="mp4")
        format_combo = ttk.Combobox(card, textvariable=self.video_format_var,
                                  values=["mp4", "webm", "mkv"],
                                  style='Dark.TCombobox', state='readonly', width=15, font=('Segoe UI', 10))
        format_combo.grid(row=1, column=3, sticky=tk.W)
        
    def create_audio_settings_card(self, parent, row):
        """Creates the audio settings section"""
        card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        card.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        card.columnconfigure(1, weight=1)
        card.columnconfigure(3, weight=1)
        
        title = ttk.Label(card, text="Audio Settings", style='Subtitle.TLabel')
        title.grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 15))
        
        ttk.Label(card, text="Format:", style='Dark.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 15))
        self.audio_format_var = tk.StringVar(value="mp3")
        format_combo = ttk.Combobox(card, textvariable=self.audio_format_var, 
                                  values=["mp3", "aac", "wav", "opus"], 
                                  style='Dark.TCombobox', state='readonly', width=15, font=('Segoe UI', 10))
        format_combo.grid(row=1, column=1, sticky=tk.W, padx=(0, 30))
        
        ttk.Label(card, text="Quality:", style='Dark.TLabel').grid(row=1, column=2, sticky=tk.W, padx=(0, 15))
        self.audio_quality_var = tk.StringVar(value="192")
        quality_combo = ttk.Combobox(card, textvariable=self.audio_quality_var,
                                   values=["best", "320", "256", "192", "128"],
                                   style='Dark.TCombobox', state='readonly', width=15, font=('Segoe UI', 10))
        quality_combo.grid(row=1, column=3, sticky=tk.W)
        
    def create_url_list_card(self, parent, row):
        """Creates the URL list section for batch download"""
        card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        card.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        card.columnconfigure(0, weight=1)
        card.rowconfigure(2, weight=1)
        
        title = ttk.Label(card, text="URL List", style='Subtitle.TLabel')
        title.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))
        
        input_frame = ttk.Frame(card, style='Dark.TFrame')
        input_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        
        self.batch_url_var = tk.StringVar()
        url_entry = ttk.Entry(input_frame, textvariable=self.batch_url_var, style='Dark.TEntry', font=('Segoe UI', 10))
        url_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 15))
        
        ttk.Button(input_frame, text="Add", 
                  command=self.add_url_to_list,
                  style='Accent.TButton').grid(row=0, column=1)
        
        list_frame = ttk.Frame(card, style='Card.TFrame')
        list_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
        self.url_listbox = tk.Listbox(list_frame, 
                                     bg=self.colors['bg_tertiary'],
                                     fg=self.colors['text_primary'],
                                     selectbackground=self.colors['accent'],
                                     selectforeground=self.colors['text_primary'],
                                     borderwidth=0,
                                     highlightthickness=0,
                                     font=('Segoe UI', 10))
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.url_listbox.yview)
        self.url_listbox.configure(yscrollcommand=scrollbar.set)
        
        self.url_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 2))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        controls_frame = ttk.Frame(card, style='Dark.TFrame')
        controls_frame.grid(row=3, column=0, pady=(15, 0))
        
        ttk.Button(controls_frame, text="Remove", 
                  command=self.remove_url_from_list,
                  style='Dark.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="Clear All", 
                  command=self.clear_url_list,
                  style='Dark.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="Load List", 
                  command=self.load_url_list,
                  style='Dark.TButton').pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(controls_frame, text="Save List", 
                  command=self.save_url_list,
                  style='Dark.TButton').pack(side=tk.LEFT)
        
    def create_batch_settings_card(self, parent, row):
        """Creates settings for batch download"""
        card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        card.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        card.columnconfigure(1, weight=1)
        card.columnconfigure(3, weight=1)
        
        title = ttk.Label(card, text="Batch Settings", style='Subtitle.TLabel')
        title.grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 15))
        
        ttk.Label(card, text="Mode:", style='Dark.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 15))
        self.batch_mode_var = tk.StringVar(value="video")
        mode_combo = ttk.Combobox(card, textvariable=self.batch_mode_var, 
                                values=["video", "audio"], 
                                style='Dark.TCombobox', state='readonly', width=15, font=('Segoe UI', 10))
        mode_combo.grid(row=1, column=1, sticky=tk.W, padx=(0, 30))
        
        ttk.Label(card, text="Quality:", style='Dark.TLabel').grid(row=1, column=2, sticky=tk.W, padx=(0, 15))
        self.batch_quality_var = tk.StringVar(value="1080p")
        quality_combo = ttk.Combobox(card, textvariable=self.batch_quality_var,
                                   values=["best", "1080p", "720p", "480p"],
                                   style='Dark.TCombobox', state='readonly', width=15, font=('Segoe UI', 10))
        quality_combo.grid(row=1, column=3, sticky=tk.W)
        
    def create_info_display_card(self, parent, row):
        """Creates the section to display video info"""
        card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        card.grid(row=row, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        card.columnconfigure(0, weight=1)
        card.rowconfigure(1, weight=1)
        
        title = ttk.Label(card, text="Video Information", style='Subtitle.TLabel')
        title.grid(row=0, column=0, sticky=tk.W, pady=(0, 15))
        
        self.info_text = scrolledtext.ScrolledText(card, 
                                                  bg=self.colors['bg_tertiary'],
                                                  fg=self.colors['text_primary'],
                                                  insertbackground=self.colors['text_primary'],
                                                  selectbackground=self.colors['accent'],
                                                  selectforeground=self.colors['text_primary'],
                                                  borderwidth=0,
                                                  wrap=tk.WORD,
                                                  height=15,
                                                  font=('Segoe UI', 10),
                                                  relief='flat')
        self.info_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
    def create_output_card(self, parent, row, card_id):
        """Creates the output section"""
        card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        card.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        card.columnconfigure(1, weight=1)
        
        title = ttk.Label(card, text="Output Folder", style='Subtitle.TLabel')
        title.grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))
        
        ttk.Label(card, text="Folder:", style='Dark.TLabel').grid(row=1, column=0, sticky=tk.W, padx=(0, 15))
        
        output_var_name = f"output_var_{card_id}"
        setattr(self, output_var_name, tk.StringVar(value=str(Path.home() / "Downloads")))
        output_var = getattr(self, output_var_name)
        
        output_entry = ttk.Entry(card, textvariable=output_var, style='Dark.TEntry', font=('Segoe UI', 10))
        output_entry.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=(0, 15))
        
        ttk.Button(card, text="Browse", command=lambda: self.select_output_folder(output_var), style='Dark.TButton').grid(row=1, column=2)
        
    def create_progress_card(self, parent, row, card_id):
        """Creates the progress section"""
        card = ttk.Frame(parent, style='Card.TFrame', padding="20")
        card.grid(row=row, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        card.columnconfigure(0, weight=1)
        
        progress_var_name = f"progress_var_{card_id}"
        setattr(self, progress_var_name, tk.DoubleVar())
        progress_var = getattr(self, progress_var_name)
        
        progress_bar_name = f"progress_bar_{card_id}"
        progress_bar = ttk.Progressbar(card, variable=progress_var, style='Dark.Horizontal.TProgressbar', length=400, mode='indeterminate')
        progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 15))
        setattr(self, progress_bar_name, progress_bar)
        
        status_var_name = f"status_var_{card_id}"
        setattr(self, status_var_name, tk.StringVar(value="Ready for download"))
        status_var = getattr(self, status_var_name)
        
        status_label = ttk.Label(card, textvariable=status_var, style='Status.TLabel')
        status_label.grid(row=1, column=0, sticky=tk.W)
        
    def create_video_control_buttons(self, parent, row):
        """Creates the video control buttons"""
        button_frame = ttk.Frame(parent, style='Dark.TFrame')
        button_frame.grid(row=row, column=0, pady=(25, 0))
        
        self.video_download_button = ttk.Button(button_frame, text="Download Video", command=self.start_video_download, style='Accent.TButton')
        self.video_download_button.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(button_frame, text="Open Folder", command=lambda: self.open_output_folder(self.output_var_video), style='Dark.TButton').pack(side=tk.LEFT)
        
    def create_audio_control_buttons(self, parent, row):
        """Creates the audio control buttons"""
        button_frame = ttk.Frame(parent, style='Dark.TFrame')
        button_frame.grid(row=row, column=0, pady=(25, 0))
        
        self.audio_download_button = ttk.Button(button_frame, text="Download Audio", command=self.start_audio_download, style='Secondary.TButton')
        self.audio_download_button.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(button_frame, text="Open Folder", command=lambda: self.open_output_folder(self.output_var_audio), style='Dark.TButton').pack(side=tk.LEFT)
        
    def create_batch_control_buttons(self, parent, row):
        """Creates the batch control buttons"""
        button_frame = ttk.Frame(parent, style='Dark.TFrame')
        button_frame.grid(row=row, column=0, pady=(25, 0))
        
        self.batch_download_button = ttk.Button(button_frame, text="Start Batch Download", command=self.start_batch_download, style='Accent.TButton')
        self.batch_download_button.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Button(button_frame, text="Open Folder", command=lambda: self.open_output_folder(self.output_var_batch), style='Dark.TButton').pack(side=tk.LEFT)
        
    def create_info_control_buttons(self, parent, row):
        """Creates the info control buttons"""
        button_frame = ttk.Frame(parent, style='Dark.TFrame')
        button_frame.grid(row=row, column=0, pady=(25, 0))
        
        self.info_button = ttk.Button(button_frame, text="Get Info", command=self.get_info, style='Accent.TButton')
        self.info_button.pack(side=tk.LEFT, padx=(0, 15))
        
        self.clear_info_button = ttk.Button(button_frame, text="Clear", command=self.clear_info_text, style='Dark.TButton')
        self.clear_info_button.pack(side=tk.LEFT)
        
    def setup_variables(self):
        """Initializes variables"""
        self.is_downloading = False
        self.current_process = None
        self.download_queue = []
        self.progress_hooks = {
            "video": self.update_video_progress,
            "audio": self.update_audio_progress,
            "batch": self.update_batch_progress
        }
        
    def paste_url(self, var):
        """Pastes URL from clipboard"""
        try:
            url = self.root.clipboard_get()
            var.set(url)
        except tk.TclError:
            messagebox.showwarning("Warning", "No URL found in clipboard.")
            
    def validate_url(self, var, validation_var):
        """Validates the URL format"""
        url = var.get()
        if re.match(r'https?://(?:www\.)?(?:youtube\.com|youtu\.be|vimeo\.com|dailymotion\.com|archive\.org)/.+$', url):
            validation_var.set("Valid URL ✅")
        elif not url:
            validation_var.set("")
        else:
            validation_var.set("Invalid URL ❌")
    
    def add_url_to_list(self):
        """Adds URL to the batch list"""
        url = self.batch_url_var.get()
        if url and url not in self.urls_list:
            self.urls_list.append(url)
            self.url_listbox.insert(tk.END, url)
            self.batch_url_var.set("")
        
    def remove_url_from_list(self):
        """Removes selected URL from the list"""
        try:
            index = self.url_listbox.curselection()[0]
            self.url_listbox.delete(index)
            self.urls_list.pop(index)
        except IndexError:
            messagebox.showwarning("Warning", "Select an URL to remove.")
            
    def clear_url_list(self):
        """Clears all URLs from the list"""
        self.url_listbox.delete(0, tk.END)
        self.urls_list.clear()
        
    def load_url_list(self):
        """Loads URLs from a text file"""
        file_path = filedialog.askopenfilename(
            title="Select URL file",
            filetypes=[("Text files", "*.txt")]
        )
        if file_path:
            self.clear_url_list()
            with open(file_path, 'r') as f:
                for line in f:
                    url = line.strip()
                    if url:
                        self.urls_list.append(url)
                        self.url_listbox.insert(tk.END, url)
            
    def save_url_list(self):
        """Saves URLs to a text file"""
        if not self.urls_list:
            messagebox.showwarning("Warning", "The list is empty.")
            return
        
        file_path = filedialog.asksaveasfilename(
            title="Save URL list",
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        
        if file_path:
            with open(file_path, 'w') as f:
                for url in self.urls_list:
                    f.write(url + '\n')
            messagebox.showinfo("Success", "List saved successfully!")
    
    def get_info(self):
        """Gets video information and displays it"""
        url = self.url_var_info.get()
        if not url:
            messagebox.showwarning("Warning", "Enter a video URL.")
            return
            
        self.clear_info_text()
        self.info_text.insert(tk.END, "Getting information, please wait...\n")
        
        self.info_thread = threading.Thread(target=self.info_worker, args=(url,))
        self.info_thread.daemon = True
        self.info_thread.start()
        
    def info_worker(self, url):
        """Worker thread to get video info"""
        try:
            ydl_opts = {'quiet': True, 'logger': self}
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(url, download=False)
                
                title = info_dict.get('title', 'N/A')
                uploader = info_dict.get('uploader', 'N/A')
                duration = info_dict.get('duration', 'N/A')
                
                formats = info_dict.get('formats', [])
                
                info_str = f"--- Video Information ---\n"
                info_str += f"Title: {title}\n"
                info_str += f"Uploader: {uploader}\n"
                info_str += f"Duration: {self.format_duration(duration)}\n"
                info_str += f"\n--- Available Formats ---\n"
                
                for f in formats:
                    f_id = f.get('format_id')
                    res = f.get('resolution')
                    ext = f.get('ext')
                    vcodec = f.get('vcodec')
                    acodec = f.get('acodec')
                    filesize = f.get('filesize')
                    
                    info_str += f"\nFormat ID: {f_id}\n"
                    info_str += f"  Resolution: {res}\n"
                    info_str += f"  Extension: {ext}\n"
                    info_str += f"  Video Codec: {vcodec}\n"
                    info_str += f"  Audio Codec: {acodec}\n"
                    info_str += f"  File Size: {self.format_size(filesize)}\n"
                    
                self.info_text.delete(1.0, tk.END)
                self.info_text.insert(tk.END, info_str)
                
        except Exception as e:
            self.info_text.delete(1.0, tk.END)
            self.info_text.insert(tk.END, f"Error getting info: {str(e)}")
    
    def clear_info_text(self):
        """Clears the info text box"""
        self.info_text.delete(1.0, tk.END)
        
    def start_video_download(self):
        """Starts video download"""
        url = self.url_var_video.get()
        output_path = self.output_var_video.get()
        quality = self.video_quality_var.get()
        file_format = self.video_format_var.get()
        
        if not url:
            messagebox.showwarning("Warning", "Enter a video URL.")
            return
        if not os.path.exists(output_path):
            messagebox.showerror("Error", "The output folder does not exist.")
            return
            
        self.set_download_state(True, "video")
        self.download_thread = threading.Thread(target=self.download_worker, 
                                                args=(url, output_path, "video", quality, file_format))
        self.download_thread.daemon = True
        self.download_thread.start()
        
    def start_audio_download(self):
        """Starts audio download"""
        url = self.url_var_audio.get()
        output_path = self.output_var_audio.get()
        quality = self.audio_quality_var.get()
        file_format = self.audio_format_var.get()
        
        if not url:
            messagebox.showwarning("Warning", "Enter a video URL.")
            return
        if not os.path.exists(output_path):
            messagebox.showerror("Error", "The output folder does not exist.")
            return
            
        self.set_download_state(True, "audio")
        self.download_thread = threading.Thread(target=self.download_worker, 
                                                args=(url, output_path, "audio", quality, file_format))
        self.download_thread.daemon = True
        self.download_thread.start()
        
    def start_batch_download(self):
        """Starts batch download"""
        if not self.urls_list:
            messagebox.showwarning("Warning", "The URL list is empty.")
            return
        
        output_path = self.output_var_batch.get()
        if not os.path.exists(output_path):
            messagebox.showerror("Error", "The output folder does not exist.")
            return
            
        mode = self.batch_mode_var.get()
        quality = self.batch_quality_var.get()
        
        self.set_download_state(True, "batch")
        self.download_queue = list(self.urls_list)
        
        self.download_thread = threading.Thread(target=self.batch_download_worker, 
                                                args=(output_path, mode, quality))
        self.download_thread.daemon = True
        self.download_thread.start()
        
    def download_worker(self, url, output_path, download_type, quality, file_format):
        """Worker thread for single downloads"""
        try:
            if download_type == "video":
                ydl_opts = self.get_video_options(output_path, quality, file_format)
            elif download_type == "audio":
                ydl_opts = self.get_audio_options(output_path, quality, file_format)
            
            ydl_opts['progress_hooks'] = [self.progress_hooks[download_type]]
            
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                
            self.progress_hooks[download_type]({'status': 'finished'})
            
        except youtube_dl.DownloadError as e:
            self.show_error(f"Download Error: {str(e)}", download_type)
        except Exception as e:
            self.show_error(f"An unexpected error occurred: {str(e)}", download_type)
        finally:
            self.set_download_state(False, download_type)
            
    def batch_download_worker(self, output_path, mode, quality):
        """Worker thread for batch download"""
        try:
            total_urls = len(self.download_queue)
            for i, url in enumerate(self.download_queue):
                if mode == "video":
                    ydl_opts = self.get_video_options(output_path, quality, "mp4")
                else: # audio
                    ydl_opts = self.get_audio_options(output_path, quality, "mp3")
                
                ydl_opts['progress_hooks'] = [lambda d: self.update_batch_progress(d, i, total_urls)]
                
                self.root.after(100, lambda: self.status_var_batch.set(f"Downloading {i+1} of {total_urls}: {url}"))
                
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])
                    
            self.progress_hooks["batch"]({'status': 'finished'})
            
        except Exception as e:
            self.show_error(f"Batch Download Error: {str(e)}", "batch")
        finally:
            self.set_download_state(False, "batch")
            
    def get_video_options(self, output_path, quality, file_format):
        """Returns video download options"""
        filename_template = os.path.join(output_path, '%(title)s.%(ext)s')
        
        if quality == "best":
            format_string = f"bestvideo[ext={file_format}]+bestaudio[ext=m4a]/best[ext={file_format}]/best"
        else:
            height = quality.replace("p", "")
            format_string = f"bestvideo[height<={height}][ext={file_format}]+bestaudio[ext=m4a]/best[ext={file_format}]/best"
            
        return {
            'format': format_string,
            'outtmpl': filename_template,
            'merge_output_format': file_format,
            'noplaylist': True
        }
    
    def get_audio_options(self, output_path, quality, file_format):
        """Returns audio download options"""
        filename_template = os.path.join(output_path, '%(title)s.%(ext)s')
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': filename_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': file_format,
                'preferredquality': quality
            }],
            'noplaylist': True
        }
        return ydl_opts
        
    def update_video_progress(self, d):
        """Updates video progress bar"""
        if d['status'] == 'downloading':
            self.progress_var_video.set(d['_percent_str'].replace('%', ''))
            self.status_var_video.set(f"Downloading... {d['_percent_str']} - {d['_eta_str']} remaining")
        elif d['status'] == 'finished':
            self.progress_bar_video.stop()
            self.progress_var_video.set(100)
            self.status_var_video.set("Download completed successfully!")
            messagebox.showinfo("Success", "Video downloaded successfully!")
            
    def update_audio_progress(self, d):
        """Updates audio progress bar"""
        if d['status'] == 'downloading':
            self.progress_var_audio.set(d['_percent_str'].replace('%', ''))
            self.status_var_audio.set(f"Downloading... {d['_percent_str']} - {d['_eta_str']} remaining")
        elif d['status'] == 'finished':
            self.progress_bar_audio.stop()
            self.progress_var_audio.set(100)
            self.status_var_audio.set("Download completed successfully!")
            messagebox.showinfo("Success", "Audio downloaded successfully!")
    
    def update_batch_progress(self, d, index=None, total=None):
        """Updates batch progress bar"""
        if d['status'] == 'downloading':
            percent = (index / total) * 100 + (d['_percent_str'].replace('%', '') / total)
            self.progress_var_batch.set(percent)
            self.status_var_batch.set(f"Downloading {index+1} of {total}: {d['_percent_str']} - {d['_eta_str']} remaining")
        elif d['status'] == 'finished':
            self.progress_bar_batch.stop()
            self.progress_var_batch.set(100)
            self.status_var_batch.set("Batch download completed!")
            messagebox.showinfo("Success", "Batch download completed successfully!")
            
    def show_error(self, message, tab_type):
        """Displays a download error"""
        self.root.after(0, lambda: messagebox.showerror("Error", message))
        self.root.after(0, lambda: self.status_var_batch.set("Download failed"))
        
    def set_download_state(self, is_downloading, tab_type):
        """Sets the UI state based on download status"""
        self.is_downloading = is_downloading
        
        button = getattr(self, f"{tab_type}_download_button")
        progressbar = getattr(self, f"progress_bar_{tab_type}")
        
        if is_downloading:
            button.config(state="disabled")
            progressbar.start()
        else:
            button.config(state="normal")
            progressbar.stop()
            
    def select_output_folder(self, var):
        """Selects the output folder"""
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            var.set(folder)
            
    def open_output_folder(self, var):
        """Opens the output folder"""
        folder_path = var.get()
        if os.path.exists(folder_path):
            os.startfile(folder_path)
        else:
            messagebox.showerror("Error", "Output folder not found.")
            
    def format_duration(self, seconds):
        """Formats duration in HH:MM:SS format"""
        if seconds is None:
            return "N/A"
        return time.strftime("%H:%M:%S", time.gmtime(seconds))
        
    def format_size(self, size_bytes):
        """Formats file size"""
        if size_bytes is None:
            return "N/A"
        if size_bytes == 0:
            return "0 B"
        
        size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {size_name[i]}"
        
def main():
    root = tk.Tk()
    app = VideoDownloaderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()