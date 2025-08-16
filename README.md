# Multimedia Tools Collection

A comprehensive suite of modern Python desktop applications for multimedia processing, password management, image viewing, and content downloading. Each tool features a dark theme, modern UI, and powerful functionality built with customtkinter and tkinter.

## 🛠️ Applications Included

### 1. 🎬 Audio & Video Converter (`audio_and_video_converter.py`)
Unified media converter with tabbed interface for audio extraction and video conversion using MoviePy and FFmpeg.

**Features:**
- **Tabbed Interface**: Separate tabs for audio extraction and video conversion
- **Audio Extraction**: Extract MP3, AAC, WAV, OGG from video files using MoviePy
- **Video Conversion**: Convert videos to MP4 with customizable quality settings
- **Batch Processing**: Multiple file support with progress tracking
- **Modern UI**: Dark theme with card-based design and progress indicators
- **Smart Dependencies**: Automatic detection and fallback for missing libraries
- **Real-time Progress**: Thread-based processing with queue communication

**Technical Components:**
- MoviePy for audio extraction from video files
- Mock FFmpeg converter with quality presets
- Threading with queue-based progress updates
- Card-style UI with ttk styling
- Automatic library detection and warnings

### 2. 📺 Video Downloader (`download_video_and_audio.py`)
Advanced video and audio downloader with support for multiple platforms using yt-dlp.

**Features:**
- **Multi-Platform Support**: YouTube, Vimeo, Dailymotion, Archive.org compatibility
- **Quality Selection**: Choose from 144p to 4K with format options (MP4, WebM, MKV)
- **Audio Extraction**: Download audio-only in MP3, AAC, WAV, Opus formats
- **Batch Downloads**: Queue multiple URLs with progress tracking
- **Video Information**: Detailed metadata extraction and format analysis
- **URL Validation**: Real-time URL format checking with visual feedback
- **Playlist Support**: Handle individual videos or entire playlists

**Advanced Features:**
- yt-dlp integration for robust downloading
- Tabbed interface for video, audio, batch, and info modes
- Progress hooks with ETA and percentage tracking
- URL list management with save/load functionality
- Format analysis with codec and file size information

### 3. 🖼️ Image Processor (`convert_compress_resize_image.py`)
Professional image processing tool with resize, compress, and format conversion capabilities using PIL and FFmpeg.

**Features:**
- **Resize Images**: Custom dimensions with maintain aspect ratio option
- **FFmpeg Compression**: Quality slider (1-31) with real-time preview
- **Format Conversion**: Convert between PNG, JPEG, BMP, TIFF, WEBP with transparency handling
- **Modern UI**: Dark theme with customtkinter, progress bars, and status logging
- **Flexible Output**: Choose output directory or use same as input
- **Real-time Feedback**: Console-style output log and progress tracking

**Key Components:**
- PIL for image manipulation and resizing
- FFmpeg integration for advanced compression
- Threading for non-blocking operations
- Automatic JPEG background conversion for transparency

### 6. 🔐 Password Manager (`password_generator.py`)
Advanced password generation and security analysis tool with comprehensive breach checking and strength analysis.

**Features:**
- **Smart Generation**: Length 8-64 characters with multiple character sets
- **Advanced Options**: Exclude ambiguous characters, no repeats, custom criteria
- **Bulk Generation**: Generate multiple passwords at once (up to 100+)
- **Security Analysis**: 100-point scoring system with detailed vulnerability assessment
- **Breach Checking**: Integration with HaveIBeenPwned API using k-anonymity
- **Password History**: Save, export, and manage generated passwords
- **Crack Time Estimation**: Calculate brute-force attack times for different scenarios

**Security Features:**
- Common password detection (24+ known weak passwords)
- Sequential pattern detection (123, abc, etc.)
- Dictionary word scanning
- Repeated character analysis
- Character diversity scoring
- Real-time strength visualization
High-performance image slideshow application with advanced caching, preloading, and smooth navigation.

**Features:**
- **Smart Caching**: Preload nearby images with configurable cache size (5-50 images)
- **Full-Screen Experience**: Immersive viewing with overlay controls
- **Auto-Slideshow**: Customizable timing (0.5s to 10s intervals)
- **Shuffle Mode**: Random image order with position tracking
- **Performance Optimized**: Multi-threaded preloading and memory management
- **Rich Controls**: Keyboard shortcuts and context menu
- **Format Support**: PNG, JPG, JPEG, GIF, BMP, WEBP, TIFF with progress loading

**Advanced Features:**
- Background image preloading thread
- Smart cache cleanup algorithms
- Recursive directory scanning
- Image resizing with aspect ratio preservation
- Real-time status display with cache information

### 4. 📸 Slideshow Viewer (`slideshow.py`)
High-performance image slideshow application with advanced caching, preloading, and smooth navigation.

**Features:**
- **Smart Caching**: Preload nearby images with configurable cache size (5-50 images)
- **Full-Screen Experience**: Immersive viewing with overlay controls
- **Auto-Slideshow**: Customizable timing (0.5s to 10s intervals)
- **Shuffle Mode**: Random image order with position tracking
- **Performance Optimized**: Multi-threaded preloading and memory management
- **Rich Controls**: Keyboard shortcuts and context menu
- **Format Support**: PNG, JPG, JPEG, GIF, BMP, WEBP, TIFF with progress loading

**Advanced Features:**
- Background image preloading thread
- Smart cache cleanup algorithms
- Recursive directory scanning
- Image resizing with aspect ratio preservation
- Real-time status display with cache information

### 5. 🎥 Video Compressor (`video_compressor.py`)
Professional video compression tool with preset configurations and real-time progress tracking.

**Features:**
- **Compression Presets**: Ultra, High, Balanced, Quality with optimized settings
- **Advanced Controls**: CRF quality slider (18-30), custom preset selection
- **Real-Time Progress**: Duration-based progress calculation with time estimates
- **Size Analysis**: Before/after file size comparison with reduction percentage
- **Modern Interface**: Card-based dark UI with visual feedback
- **FFmpeg Integration**: Full FFmpeg command-line integration with error handling

**Technical Specifications:**
- H.264/AAC encoding pipeline
- Movflags optimization for streaming
- Custom CRF (Constant Rate Factor) control
- Automatic file extension handling
- Process monitoring with stderr parsing

## 🚀 Installation & Setup

### Prerequisites
- **Python 3.7+** (tested on 3.8+)
- **FFmpeg** (required for video/audio processing and image compression)

### Install Python Dependencies

```bash
# Core dependencies for all applications
pip install customtkinter pillow ttkthemes

# For audio/video converter
pip install moviepy

# For video downloader
pip install yt-dlp

# For password manager additional features
pip install pyperclip requests

# Verify installation
python -c "import customtkinter, PIL, tkinter, moviepy, yt_dlp; print('Dependencies OK')"
```

### FFmpeg Installation

#### Windows:
1. Download from https://ffmpeg.org/download.html
2. Extract to `C:\ffmpeg\` 
3. Update paths in applications to `C:\ffmpeg\bin\ffmpeg.exe`

#### Linux/Ubuntu:
```bash
sudo apt update
sudo apt install ffmpeg
# Path will be: /usr/bin/ffmpeg
```

#### macOS:
```bash
brew install ffmpeg
# Path will be: /usr/local/bin/ffmpeg
```

## 🎯 Usage Guide

### Running Applications

```bash
# Audio & Video Converter
python audio_and_video_converter.py

# Video Downloader
python download_video_and_audio.py

# Image Processor
python convert_compress_resize_image.py

# Password Manager  
python password_generator.py

# Slideshow Viewer
python slideshow.py

# Video Compressor
python video_compressor.py
```

### Keyboard Shortcuts

#### Slideshow Viewer:
- `ESC` - Exit application
- `A` / `←` - Previous image  
- `D` / `→` - Next image
- `SPACE` - Toggle auto-slideshow
- `S` - Toggle shuffle mode
- `F` - Toggle fullscreen
- `R` - Reload current image
- `Right-click` - Context menu with settings

#### Video Downloader:
- `Ctrl+V` - Paste URL in focused entry field
- `Delete` - Remove selected URL from batch list
- `Tab` - Navigate between different download modes
- URL validation happens in real-time

#### Audio & Video Converter:
- `Tab` - Switch between audio extraction and video conversion modes
- Progress bars show real-time conversion status
- Drag & drop support for multiple files

## ⚙️ Configuration & Settings

### Image Processor Settings
```python
# Default FFmpeg path (update as needed)
ffmpeg_path = "E:\\HDD\\ffmpeg\\bin\\ffmpeg.exe"

# Supported formats
formats = ["PNG", "JPEG", "BMP", "TIFF", "WEBP"]

# Quality range for compression
quality_range = (1, 31)  # Lower = better quality
```

### Password Manager Configuration
```python
# Security settings
min_length = 8
max_length = 64
cache_size = 100  # Password history

# Character sets
uppercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
lowercase = "abcdefghijklmnopqrstuvwxyz"  
numbers = "0123456789"
symbols = "!@#$%^&*()_+-=[]{}|;:,.<>?"
```

### Slideshow Viewer Options
```python
# Performance settings
default_cache_size = 10
max_cache_size = 50
preload_thread_delay = 0.1

# Slideshow timing options
speed_options = [500, 1000, 3000, 5000, 10000]  # milliseconds
```

### Video Compressor Presets
```python
presets = {
    "ultra": {"crf": 28, "preset": "faster"},     # Smallest file
    "high": {"crf": 25, "preset": "fast"},        # Small file, good quality  
    "balanced": {"crf": 23, "preset": "medium"},  # Recommended
    "quality": {"crf": 20, "preset": "slow"}      # Best quality, larger file
}
```

## 🎨 Technical Features

### Modern UI Design
- **CustomTkinter Framework**: Modern, themed widgets with dark mode
- **Card-Based Layouts**: Clean, organized interface design
- **Progress Indicators**: Real-time feedback with progress bars
- **Responsive Design**: Scalable UI elements and layouts

### Performance Optimizations
- **Multi-Threading**: Background processing for heavy operations
- **Smart Caching**: Efficient memory usage with cleanup algorithms  
- **Async Operations**: Non-blocking UI during file processing
- **Resource Management**: Automatic cleanup and memory optimization

### Error Handling & Validation
- **Input Validation**: File format checking and path validation
- **Exception Handling**: Comprehensive error catching with user feedback
- **Process Monitoring**: Real-time status updates and error reporting
- **Recovery Options**: Graceful failure handling with retry options

## 📁 Project Structure

```
multimedia-tools/
├── audio_and_video_converter.py       # Unified media converter
├── download_video_and_audio.py        # Video/audio downloader  
├── convert_compress_resize_image.py   # Image processing application
├── password_generator.py              # Password management tool  
├── slideshow.py                       # Image slideshow viewer
├── video_compressor.py                # Video compression utility
├── README.md                          # Documentation (this file)
└── requirements.txt                   # Python dependencies
```

## 🛠️ Troubleshooting

### Common Issues & Solutions

**FFmpeg Not Found Error:**
```bash
# Test FFmpeg installation
ffmpeg -version

# Update path in applications
# Windows: "C:\\ffmpeg\\bin\\ffmpeg.exe"  
# Linux/Mac: "/usr/bin/ffmpeg" or "/usr/local/bin/ffmpeg"
```

**Missing Dependencies:**
```bash
# Install all required packages
pip install --upgrade customtkinter pillow ttkthemes pyperclip requests moviepy yt-dlp

# For import errors, try:
pip uninstall customtkinter
pip install customtkinter

# For MoviePy issues:
pip install --upgrade moviepy imageio imageio-ffmpeg

# For yt-dlp issues:
pip install --upgrade yt-dlp
```

**Network/Download Issues:**
- Check internet connection for video downloads
- Some videos may be region-restricted
- YouTube frequently updates - keep yt-dlp updated: `pip install --upgrade yt-dlp`
- For audio extraction, ensure FFmpeg is properly installed

**MoviePy/FFmpeg Integration Issues:**
- Ensure FFmpeg is in system PATH
- Update MoviePy: `pip install --upgrade moviepy`
- For Windows: Download FFmpeg and add to PATH environment variable

**Memory Issues (Large Files):**
- Reduce slideshow cache size (5-10 images)
- Close other applications before processing
- Process videos/images in smaller batches
- Use "Ultra" preset for faster video compression

**Permission Errors:**
```bash
# Windows: Run as Administrator
# Linux/Mac: Check file permissions
chmod +x *.py
sudo python script_name.py  # If needed
```

### Performance Tips

1. **Video Compression**: Start with "Balanced" preset, adjust CRF for quality vs. size
2. **Image Processing**: Use appropriate compression levels (15-25 for good balance)  
3. **Slideshow**: Reduce cache size on older systems, use shuffle for variety
4. **Password Generation**: Bulk generation is more efficient than individual passwords
5. **Video Downloads**: Use lower quality settings for faster downloads and less bandwidth
6. **Audio Conversion**: MP3 format generally processes faster than WAV or FLAC
7. **Batch Operations**: Process files in smaller groups to avoid memory issues

### System Requirements

- **RAM**: 4GB minimum, 8GB recommended for large video files
- **Storage**: Sufficient space for output files (compressed videos can be 50-80% smaller)
- **CPU**: Multi-core recommended for video processing
- **Display**: 1920x1080 or higher for optimal slideshow experience

## 📊 Feature Comparison

| Feature | Audio/Video Converter | Video Downloader | Image Processor | Password Manager | Slideshow Viewer | Video Compressor |
|---------|----------------------|------------------|-----------------|------------------|------------------|------------------|
| **UI Framework** | TTK/Tkinter | TTK/Tkinter | CustomTkinter | CustomTkinter | ThemedTk | Tkinter |
| **Threading** | ✅ Background | ✅ Downloads | ✅ Background | ✅ Network calls | ✅ Preloading | ✅ Processing |
| **Progress Tracking** | ✅ Queue-based | ✅ Real-time | ✅ Real-time | ✅ Analysis | ✅ Loading | ✅ Compression |
| **Batch Operations** | ✅ Multiple files | ✅ URL lists | ❌ Single file | ✅ Bulk generate | ✅ Folder scan | ❌ Single file |
| **Caching** | ❌ None | ❌ None | ❌ None | ✅ History | ✅ Smart cache | ❌ None |
| **External Tools** | ✅ MoviePy/FFmpeg | ✅ yt-dlp | ✅ FFmpeg | ✅ API calls | ❌ None | ✅ FFmpeg |
| **Network Required** | ❌ Local only | ✅ Downloads | ❌ Local only | ✅ Breach check | ❌ Local only | ❌ Local only |

## 🔄 Version History & Updates

**Current Version**: 1.0.0
- Initial release with all core features
- Modern dark theme UI across all applications  
- Multi-threading for performance
- Comprehensive error handling
- Advanced caching and optimization features
- Audio/video conversion and download capabilities

**Planned Features**:
- Batch processing for image processor
- Video format conversion options  
- Password manager encryption
- Slideshow transition effects
- Cloud storage integration options
- Playlist download support for video downloader
- Custom FFmpeg parameters for advanced users

---

**Note**: These applications are designed for desktop use and require appropriate system permissions for file operations. Always backup important files before processing.
