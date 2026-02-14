# Music Mashup Generator

A simple tool to create audio mashups from YouTube videos. This project has two parts - a command-line program and a web application.

---

## What This Does

Takes a singer's name, downloads their songs from YouTube, cuts a portion from each song, and merges them into one audio file. You can use it from the command line or through a web interface.

---

## Project Structure

```
├── 102303961.py          # Command-line program (Part 1)
└── web_service_mashup/   # Web application (Part 2)
    ├── app.py
    ├── requirements.txt
    └── .gitignore
```

---

## Part 1: Command Line Program

### How to Use

```bash
python 102303961.py "<singer_name>" <num_videos> <duration> <output_file>
```

**Example:**
```bash
python 102303961.py "Arijit Singh" 15 30 output.mp3
```

This will:
- Download 15 Arijit Singh songs
- Cut first 30 seconds from each
- Merge them into output.mp3

### Requirements

```bash
pip install yt-dlp pydub moviepy
```

You also need FFmpeg installed on your system.

### Parameters

- `singer_name` - Name of the singer (in quotes)
- `num_videos` - Number of videos to download (must be > 10)
- `duration` - Seconds to cut from each video (must be > 20)
- `output_file` - Name of output file (e.g., mashup.mp3)

---

## Part 2: Web Application

A Streamlit-based web interface for the same functionality.

### Live Demo

🔗 [Mashup Generator Web App](https://mashup-webapp-g9k5.onrender.com/)

### Features

- Simple form interface
- Download button for generated mashup
- Email delivery of mashup file (ZIP format)
- Progress tracking
- Input validation

### Local Setup

```bash
cd web_service_mashup
pip install -r requirements.txt
streamlit run app.py
```

Create `.streamlit/secrets.toml` for email functionality:
```toml
SENDER_EMAIL = "your_email@gmail.com"
SENDER_PASSWORD = "your_app_password"
```

---

## How It Works

### Methodology

The program follows these steps:

**1. Video Search and Download**
- Uses yt-dlp to search YouTube for the singer's songs
- Downloads audio from the top results
- Filters out live performances, concerts, and playlists to get actual songs
- Downloads videos one at a time to avoid rate limiting

**2. Audio Extraction**
- Converts downloaded videos to MP3 format
- Uses FFmpeg through yt-dlp's post-processor
- Each video becomes a separate audio file

**3. Audio Trimming**
- Loads each audio file using pydub
- Cuts the first N seconds (as specified by user)
- Saves each trimmed portion as a separate clip
- Duration is converted to milliseconds for precise cutting

**4. Merging**
- Creates an empty audio segment
- Sequentially adds each trimmed clip
- Combines all clips into a single continuous audio file
- Exports as MP3 format

**5. Cleanup**
- Removes all temporary files and folders
- Keeps only the final mashup file

### Technical Details

**Libraries Used:**

- **yt-dlp**: YouTube video downloading
  - Searches YouTube with custom queries
  - Downloads best available audio quality
  - Built-in audio extraction using FFmpeg
  
- **pydub**: Audio manipulation
  - Loading MP3 files
  - Cutting/trimming audio segments
  - Merging multiple audio files
  - Exporting final output
  
- **moviepy**: Video to audio conversion (backup method)
  - Alternative extraction if needed
  
- **streamlit**: Web interface (Part 2 only)
  - Form inputs and validation
  - Progress tracking
  - File downloads

**Why These Libraries?**

- yt-dlp is the most reliable YouTube downloader
- pydub makes audio editing simple and intuitive
- All are available on PyPI as required

---

## Installation

### Prerequisites

1. **Python 3.7+**
   ```bash
   python --version
   ```

2. **FFmpeg**
   - Ubuntu/Debian: `sudo apt-get install ffmpeg`
   - macOS: `brew install ffmpeg`
   - Windows: Download from https://ffmpeg.org

3. **Python Packages**
   ```bash
   pip install yt-dlp pydub moviepy streamlit
   ```

### Quick Start

**For CLI:**
```bash
python 102303961.py "Sharry Maan" 12 25 mashup.mp3
```

**For Web App:**
```bash
cd web_service_mashup
streamlit run app.py
```

---

## Examples

### CLI Usage

```bash
# Download 15 songs, cut 30 seconds each
python 102303961.py "Atif Aslam" 15 30 atif_mashup.mp3

# Download 20 songs, cut 25 seconds each
python 102303961.py "Shreya Ghoshal" 20 25 shreya_mix.mp3
```

### Web Interface

1. Open the web app
2. Enter singer name: "Arijit Singh"
3. Number of videos: 15
4. Duration: 30 seconds
5. Email: your@email.com
6. Click "Generate Mashup"
7. Download the ZIP file or check your email

---

## Notes

- The web app is deployed on Streamlit Cloud (free tier)
- Email functionality uses Gmail SMTP

---