# Multimedia Tools Collection

A comprehensive suite of modern Python desktop applications for multimedia processing, password management, and image viewing. Each tool features a dark theme, modern UI, and powerful functionality.

## 🛠️ Applications Included

### 1. 🎬 Audio & Video Converter (`audio_and_video_converter.py`)
A unified media converter with tabbed interface for audio extraction and video conversion.

**Features:**
- Extract audio from video files (MP3, WAV, AAC, OGG)
- Convert videos to MP4 format
- Batch processing support
- Modern dark theme interface
- Progress tracking and status updates
- Support for various quality settings

**Dependencies:** `moviepy`, `tkinter`, `pathlib`

### 2. 🖼️ Image Processor (`convert_compress_resize_image.py`)
Professional image processing tool with resize, compress, and format conversion capabilities.

**Features:**
- Resize images with aspect ratio options
- Compress images using FFmpeg
- Convert between formats (PNG, JPEG, BMP, TIFF, WEBP)
- Real-time progress tracking
- Batch operations support
- Quality slider for compression

**Dependencies:** `customtkinter`, `PIL (Pillow)`, `subprocess`

### 3. 🔐 Password Manager (`password_generator.py`)
Advanced password generation and security analysis tool with breach checking.

**Features:**
- Generate secure passwords with customizable criteria
- Bulk password generation
- Password strength analysis with detailed scoring
- Check passwords against known data breaches
- Password history tracking
- Export functionality
- Crack time estimation

**Dependencies:** `customtkinter`, `pyperclip`, `requests`, `hashlib`

### 4. 📸 Slideshow Viewer (`slideshow.py`)
High-performance image slideshow application with advanced caching and preloading.

**Features:**
- Full-screen image viewing
- Auto-slideshow with customizable timing
- Smart image preloading and caching
- Shuffle mode
- Keyboard shortcuts
- Context menu with settings
- Support for various image formats

**Dependencies:** `ttkthemes`, `PIL (Pillow)`, `threading`, `queue`

### 5. 🎥 Video Compressor (`video_compressor.py`)
Professional video compression tool with preset configurations and real-time progress.

**Features:**
- Multiple compression presets (Ultra, High, Balanced, Quality)
- Real-time compression progress
- Size reduction statistics
- Custom quality settings (CRF)
- Modern card-based interface
- FFmpeg integration

**Dependencies:** `tkinter`, `subprocess`, `pathlib`

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- FFmpeg (for video/audio processing applications)

### Install Dependencies

```bash
# Core dependencies
pip install pillow customtkinter ttkthemes

# For audio/video processing
pip install moviepy

# For password manager
pip install pyperclip requests

# Optional: For themed applications
pip install ttkthemes
```

### FFmpeg Setup
1. Download FFmpeg from https://ffmpeg.org/download.html
2. Extract to a folder (e.g., `C:\ffmpeg` or `/usr/local/ffmpeg`)
3. Update the FFmpeg path in applications that require it

## 🎯 Usage

### Running Applications

```bash
# Audio & Video Converter
python audio_and_video_converter.py

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
- `A/D` or `←/→` - Navigate images
- `SPACE` - Toggle slideshow
- `S` - Toggle shuffle
- `F` - Toggle fullscreen
- `R` - Reload current image
- `Right-click` - Context menu

#### General (Most Apps):
- `ESC` - Exit or cancel
- `F11` - Fullscreen (where applicable)

## 🎨 Features Overview

### Modern UI Design
- **Dark Theme**: All applications feature modern dark themes
- **Consistent Design**: Card-based layouts with consistent styling
- **Responsive**: Applications adapt to different screen sizes
- **Progress Indicators**: Real-time progress bars and status updates

### Performance Optimizations
- **Threading**: Background processing for heavy operations
- **Caching**: Smart caching systems (especially in slideshow)
- **Memory Management**: Efficient resource handling
- **Async Operations**: Non-blocking UI during processing

### User Experience
- **Intuitive Controls**: Easy-to-use interfaces
- **Keyboard Shortcuts**: Quick access to common functions
- **Context Menus**: Right-click menus with relevant options
- **Status Feedback**: Clear status messages and error handling

## 📁 File Structure

```
multimedia-tools/
├── audio_and_video_converter.py    # Media conversion tool
├── convert_compress_resize_image.py # Image processing tool
├── password_generator.py           # Password management tool
├── slideshow.py                    # Image slideshow viewer
├── video_compressor.py             # Video compression tool
├── README.md                       # This file
└── requirements.txt                # Python dependencies
```

## ⚙️ Configuration

### FFmpeg Path Configuration
Update the FFmpeg path in applications that require it:

```python
# Example for Windows
ffmpeg_path = "C:\\ffmpeg\\bin\\ffmpeg.exe"

# Example for Linux/Mac
ffmpeg_path = "/usr/local/bin/ffmpeg"
```

### Application Settings

#### Audio & Video Converter:
- Output formats: MP3, WAV, AAC, OGG (audio) / MP4 (video)
- Quality settings: 128k, 192k, 256k, 320k bitrates
- Batch processing: Multiple files at once

#### Image Processor:
- Resize: Custom dimensions with aspect ratio options
- Compression: Quality levels 1-31 (lower = better quality)
- Formats: PNG, JPEG, BMP, TIFF, WEBP

#### Password Manager:
- Length: 8-64 characters
- Character sets: Uppercase, lowercase, numbers, symbols
- Security options: Exclude ambiguous, no repeats
- Breach checking: HaveIBeenPwned API integration

#### Slideshow Viewer:
- Cache size: 5-50 images
- Speed settings: 0.5s to 10s intervals
- Supported formats: PNG, JPG, JPEG, GIF, BMP, WEBP, TIFF

#### Video Compressor:
- Presets: Ultra, High, Balanced, Quality
- CRF range: 18-30 (lower = better quality)
- Output: H.264/AAC MP4 format

## 🐛 Troubleshooting

### Common Issues

**FFmpeg Not Found:**
- Ensure FFmpeg is installed and path is correct
- Test FFmpeg installation: `ffmpeg -version`
- Update path in application settings

**Missing Dependencies:**
```bash
pip install --upgrade pillow customtkinter moviepy pyperclip requests ttkthemes
```

**Permission Errors:**
- Run as administrator (Windows) or use sudo (Linux/Mac)
- Check file permissions for input/output directories

**Memory Issues (Large Files):**
- Close other applications
- Reduce cache size in slideshow viewer
- Process files in smaller batches

### Performance Tips

1. **For Large Video Files**: Use "Ultra" or "High" presets for faster processing
2. **For Slideshow**: Reduce cache size if experiencing memory issues
3. **For Batch Processing**: Process files in smaller groups
4. **For Image Processing**: Use appropriate quality settings to balance size/quality
