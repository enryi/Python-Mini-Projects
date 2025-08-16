import tkinter as tk
from tkinter import filedialog, Menu, Toplevel, messagebox, ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import os
import random
import threading
from queue import Queue
import time

class SlideshowApp:
    def __init__(self, root):
        self.root = root
        self.root.set_theme("black")
        self.root.title("Slideshow App - Optimized Version")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="black")
        
        self.root.bind("<Escape>", self.exit_program)
        self.root.bind("a", self.previous_image)
        self.root.bind("d", self.next_image)
        self.root.bind("<Right>", self.next_image)
        self.root.bind("<Left>", self.previous_image)
        self.root.bind("<Button-3>", self.show_context_menu)
        self.root.bind("<space>", self.toggle_slideshow)
        self.root.bind("s", self.toggle_shuffle)
        self.root.bind("f", self.toggle_fullscreen)
        self.root.bind("r", self.reload_current_image)
        
        self.images = []
        self.current_index = 0
        self.slideshow_running = False
        self.shuffle_images = False
        self.slideshow_timer = None
        self.slideshow_speed = 3000
        self.is_fullscreen = True
        
        self.image_cache = {}
        self.cache_size = 10
        self.preload_queue = Queue()
        self.preload_thread = None
        self.preload_active = False
        
        self.canvas_size = (1920, 1080)
        self.loading = False
        
        self.setup_ui()

    def setup_ui(self):
        self.canvas = tk.Canvas(self.root, bg="black", highlightthickness=0)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        self.canvas.bind('<Configure>', self.on_canvas_configure)
        
        self.control_frame = tk.Frame(self.root, bg="black")
        
        self.load_button = tk.Button(
            self.root, 
            text="📁 Load Folder", 
            command=self.load_images, 
            font=("Arial", 16, "bold"), 
            bg="gray25", 
            fg="white",
            activebackground="gray35",
            activeforeground="white",
            relief="flat",
            padx=30,
            pady=15,
            cursor="hand2"
        )
        self.load_button.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            self.root, 
            variable=self.progress_var, 
            maximum=100,
            length=400,
            style="TProgressbar"
        )
        
        self.info_label = tk.Label(
            self.root,
            text="ESC: exit | ↔ A/D: navigate | SPACE: slideshow | S: shuffle | F: fullscreen | Right-click: menu",
            font=("Arial", 11),
            bg="black",
            fg="gray60",
            wraplength=800,
            justify="center"
        )
        self.info_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)
        
        self.status_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 10),
            bg="black",
            fg="yellow"
        )

    def on_canvas_configure(self, event):
        """Updates canvas dimensions"""
        self.canvas_size = (event.width, event.height)

    def load_images(self):
        """Loads images with progress bar"""
        folder_path = filedialog.askdirectory(title="Select folder with images")
        if not folder_path:
            return
            
        self.load_button.config(state="disabled", text="Loading...")
        self.progress_bar.place(relx=0.5, rely=0.6, anchor=tk.CENTER)
        self.status_label.config(text="Searching for images...")
        self.status_label.place(relx=0.5, rely=0.65, anchor=tk.CENTER)
        
        threading.Thread(target=self._load_images_thread, args=(folder_path,), daemon=True).start()

    def _load_images_thread(self, folder_path):
        """Thread for loading images"""
        try:
            images = self.find_images_in_directory(folder_path)
            
            self.root.after(0, self._on_images_loaded, images)
            
        except Exception as e:
            self.root.after(0, self._on_loading_error, str(e))

    def _on_images_loaded(self, images):
        """Callback when images have been loaded"""
        if not images:
            messagebox.showwarning("Warning", "No images found in the selected folder!")
            self.load_button.config(state="normal", text="📁 Load Folder")
            self.progress_bar.place_forget()
            self.status_label.place_forget()
            return
        
        self.images = images
        
        if self.shuffle_images:
            random.shuffle(self.images)
        
        self.current_index = 0
        
        self.load_button.place_forget()
        self.info_label.place_forget()
        self.progress_bar.place_forget()
        self.status_label.place_forget()
        
        self.start_preloading()
        
        self.show_image()

    def _on_loading_error(self, error):
        """Callback for errors during loading"""
        messagebox.showerror("Error", f"Error during loading: {error}")
        self.load_button.config(state="normal", text="📁 Load Folder")
        self.progress_bar.place_forget()
        self.status_label.place_forget()

    def find_images_in_directory(self, directory):
        """Finds all images in the directory with progress"""
        image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.tiff', '.tif')
        image_list = []
        
        total_files = 0
        for root, dirs, files in os.walk(directory):
            total_files += len(files)
        
        processed = 0
        
        for root, dirs, files in os.walk(directory):
            for file in files:
                if file.lower().endswith(image_extensions):
                    image_list.append(os.path.join(root, file))
                
                processed += 1
                if processed % 50 == 0:
                    progress = (processed / total_files) * 100
                    self.root.after(0, self._update_progress, progress, f"Found {len(image_list)} images...")
        
        self.root.after(0, self._update_progress, 100, f"Loaded {len(image_list)} images!")
        return sorted(image_list)

    def _update_progress(self, value, text):
        """Updates progress bar"""
        self.progress_var.set(value)
        self.status_label.config(text=text)
        self.root.update_idletasks()

    def start_preloading(self):
        """Starts image preloading"""
        if self.preload_thread and self.preload_thread.is_alive():
            self.preload_active = False
            self.preload_thread.join(timeout=1)
        
        self.preload_active = True
        self.preload_thread = threading.Thread(target=self._preload_worker, daemon=True)
        self.preload_thread.start()

    def _preload_worker(self):
        """Worker thread for preloading"""
        while self.preload_active and self.images:
            try:
                indices_to_preload = self._get_preload_indices()
                
                for idx in indices_to_preload:
                    if not self.preload_active:
                        break
                    
                    if idx not in self.image_cache:
                        try:
                            img_path = self.images[idx]
                            img = Image.open(img_path)
                            resized_img = self.resize_image(img)
                            photo = ImageTk.PhotoImage(resized_img)
                            self.image_cache[idx] = photo
                            
                            if len(self.image_cache) > self.cache_size * 2:
                                self._cleanup_cache()
                                
                        except Exception as e:
                            print(f"Preloading error for {img_path}: {e}")
                            continue
                
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error in preloader: {e}")
                time.sleep(1)

    def _get_preload_indices(self):
        """Gets indices of images to preload"""
        if not self.images:
            return []
        
        indices = []
        half_cache = self.cache_size // 2
        
        for i in range(-half_cache, half_cache + 1):
            idx = (self.current_index + i) % len(self.images)
            indices.append(idx)
        
        return indices

    def _cleanup_cache(self):
        """Cleans up cache, keeping only nearby images"""
        if not self.images:
            return
        
        indices_to_keep = set(self._get_preload_indices())
        keys_to_remove = [k for k in self.image_cache.keys() if k not in indices_to_keep]
        
        for key in keys_to_remove:
            del self.image_cache[key]

    def show_image(self):
        """Displays the current image (optimized)"""
        if not self.images or self.loading:
            return
        
        self.loading = True
        self.canvas.delete("all")
        
        try:
            if self.current_index in self.image_cache:
                photo = self.image_cache[self.current_index]
                self._display_cached_image(photo)
            else:
                self._load_image_immediately()
            
            self.show_image_info()
            
        except Exception as e:
            print(f"Error showing image: {e}")
            self.next_image()
        finally:
            self.loading = False

    def _display_cached_image(self, photo):
        """Displays image from cache"""
        canvas_width, canvas_height = self.canvas_size
        self.canvas.create_image(
            canvas_width // 2, 
            canvas_height // 2, 
            image=photo, 
            anchor=tk.CENTER
        )
        self.canvas.image = photo
        self.restart_slideshow_timer()

    def _load_image_immediately(self):
        """Loads and displays an image immediately"""
        try:
            image_path = self.images[self.current_index]
            img = Image.open(image_path)
            img = self.resize_image(img)
            photo = ImageTk.PhotoImage(img)
            
            self.image_cache[self.current_index] = photo
            
            self._display_cached_image(photo)
            
        except Exception as e:
            print(f"Immediate loading error: {e}")
            raise

    def resize_image(self, img):
        """Resizes the image (optimized)"""
        canvas_width, canvas_height = self.canvas_size
        
        if canvas_width <= 1 or canvas_height <= 1:
            canvas_width, canvas_height = 1920, 1080
        
        margin = 40
        target_width = canvas_width - margin
        target_height = canvas_height - margin
        
        img_width, img_height = img.size
        img_ratio = img_width / img_height
        target_ratio = target_width / target_height
        
        if img_ratio > target_ratio:
            new_width = target_width
            new_height = int(target_width / img_ratio)
        else:
            new_height = target_height
            new_width = int(target_height * img_ratio)
        
        if hasattr(Image, 'Resampling'):
            resample = Image.Resampling.LANCZOS
        else:
            resample = Image.LANCZOS
            
        return img.resize((new_width, new_height), resample)

    def show_image_info(self):
        """Displays image information"""
        if not self.images:
            return
            
        image_path = self.images[self.current_index]
        filename = os.path.basename(image_path)
        
        info_text = f"{self.current_index + 1}/{len(self.images)} - {filename}"
        self.canvas.create_text(
            15, 15,
            text=info_text,
            font=("Arial", 12, "bold"),
            fill="white",
            anchor="nw"
        )
        
        status_text = ""
        if self.slideshow_running:
            status_text += "▶ Slideshow "
        if self.shuffle_images:
            status_text += "🔀 Shuffle "
        
        if status_text:
            self.canvas.create_text(
                15, 40,
                text=status_text.strip(),
                font=("Arial", 10),
                fill="lime",
                anchor="nw"
            )
        
        cache_info = f"Cache: {len(self.image_cache)}/{self.cache_size*2}"
        self.canvas.create_text(
            15, self.canvas_size[1] - 25,
            text=cache_info,
            font=("Arial", 9),
            fill="gray",
            anchor="nw"
        )

    def previous_image(self, event=None):
        """Previous image"""
        if self.images and not self.loading:
            self.current_index = (self.current_index - 1) % len(self.images)
            self.show_image()

    def next_image(self, event=None):
        """Next image"""
        if self.images and not self.loading:
            self.current_index = (self.current_index + 1) % len(self.images)
            self.show_image()

    def reload_current_image(self, event=None):
        """Reloads the current image"""
        if self.images:
            if self.current_index in self.image_cache:
                del self.image_cache[self.current_index]
            self.show_image()

    def restart_slideshow_timer(self):
        """Restarts slideshow timer"""
        if self.slideshow_timer:
            self.root.after_cancel(self.slideshow_timer)
        
        if self.slideshow_running and self.images:
            self.slideshow_timer = self.root.after(self.slideshow_speed, self.next_image)

    def toggle_slideshow(self, event=None):
        """Toggles slideshow"""
        self.slideshow_running = not self.slideshow_running
        if self.images:
            self.show_image()
        self.restart_slideshow_timer()

    def toggle_shuffle(self, event=None):
        """Toggles shuffle"""
        if not self.images:
            return
            
        self.shuffle_images = not self.shuffle_images
        
        self.image_cache.clear()
        
        if self.shuffle_images:
            current_image = self.images[self.current_index]
            random.shuffle(self.images)
            try:
                self.current_index = self.images.index(current_image)
            except ValueError:
                self.current_index = 0
        else:
            current_image = self.images[self.current_index]
            self.images = sorted(self.images)
            try:
                self.current_index = self.images.index(current_image)
            except ValueError:
                self.current_index = 0
        
        self.show_image()

    def toggle_fullscreen(self, event=None):
        """Toggles fullscreen"""
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes('-fullscreen', self.is_fullscreen)

    def show_context_menu(self, event):
        """Displays context menu"""
        context_menu = Menu(self.root, tearoff=0, bg="gray15", fg="white", activebackground="gray25")
        
        slideshow_status = "⏸ Stop Slideshow" if self.slideshow_running else "▶ Start Slideshow"
        context_menu.add_command(label=slideshow_status, command=self.toggle_slideshow)
        
        shuffle_status = "🔀 Disable Shuffle" if self.shuffle_images else "🔀 Enable Shuffle"
        context_menu.add_command(label=shuffle_status, command=self.toggle_shuffle)
        
        context_menu.add_separator()
        
        speed_menu = Menu(context_menu, tearoff=0, bg="gray15", fg="white", activebackground="gray25")
        speeds = [
            ("⚡ Very fast (0.5s)", 500),
            ("🚀 Fast (1s)", 1000),
            ("📊 Normal (3s)", 3000),
            ("🐢 Slow (5s)", 5000),
            ("🦕 Very slow (10s)", 10000)
        ]
        
        for label, speed in speeds:
            marker = "● " if self.slideshow_speed == speed else "○ "
            speed_menu.add_command(label=marker + label, command=lambda s=speed: self.set_speed(s))
        
        context_menu.add_cascade(label="⚙ Slideshow Speed", menu=speed_menu)
        
        cache_menu = Menu(context_menu, tearoff=0, bg="gray15", fg="white", activebackground="gray25")
        cache_sizes = [(f"{size} images", size) for size in [5, 10, 20, 50]]
        
        for label, size in cache_sizes:
            marker = "● " if self.cache_size == size else "○ "
            cache_menu.add_command(label=marker + label, command=lambda s=size: self.set_cache_size(s))
        
        context_menu.add_cascade(label="💾 Cache Size", menu=cache_menu)
        
        context_menu.add_separator()
        context_menu.add_command(label="🔄 Reload image", command=self.reload_current_image)
        context_menu.add_command(label="📁 Load new folder", command=self.load_new_folder)
        context_menu.add_command(label="🖥 Fullscreen On/Off", command=self.toggle_fullscreen)
        context_menu.add_separator()
        context_menu.add_command(label="❌ Exit", command=self.exit_program)
        
        try:
            context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            context_menu.grab_release()

    def set_speed(self, speed):
        """Sets slideshow speed"""
        self.slideshow_speed = speed
        self.restart_slideshow_timer()

    def set_cache_size(self, size):
        """Sets cache size"""
        self.cache_size = size
        self._cleanup_cache()

    def load_new_folder(self):
        """Loads new folder"""
        self.slideshow_running = False
        self.preload_active = False
        
        if self.slideshow_timer:
            self.root.after_cancel(self.slideshow_timer)
        
        self.image_cache.clear()
        
        self.canvas.delete("all")
        self.load_button.config(state="normal", text="📁 Load Folder")
        self.load_button.place(relx=0.5, rely=0.45, anchor=tk.CENTER)
        self.info_label.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

    def exit_program(self, event=None):
        """Exits the program"""
        self.preload_active = False
        
        if self.slideshow_timer:
            self.root.after_cancel(self.slideshow_timer)
        
        if self.preload_thread and self.preload_thread.is_alive():
            self.preload_thread.join(timeout=1)
        
        self.root.quit()
        self.root.destroy()

if __name__ == "__main__":
    root = ThemedTk(theme="black")
    app = SlideshowApp(root)
    root.mainloop()