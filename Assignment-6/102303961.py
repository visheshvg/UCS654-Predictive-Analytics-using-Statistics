"""
Mashup Generator - CLI Program
Usage: python <rollnumber>.py <singer> <videos> <duration> <output.mp3>
"""

import sys
import os
import shutil
from pathlib import Path

def validate_inputs(args):
    """Check if user provided correct arguments"""
    if len(args) != 4:
        print("Error: Invalid number of arguments")
        print("Usage: python script.py <SingerName> <NumVideos> <Duration> <Output>")
        print('Example: python script.py "Arijit Singh" 15 25 output.mp3')
        return None
    
    singer = args[0].strip()
    
    try:
        num_videos = int(args[1])
        duration = int(args[2])
    except:
        print("Error: Number of videos and duration must be integers")
        return None
    
    if num_videos <= 10:
        print("Error: Number of videos must be greater than 10")
        return None
    
    if duration <= 20:
        print("Error: Duration must be greater than 20 seconds")
        return None
    
    output_file = args[3]
    if not output_file.endswith('.mp3'):
        output_file += '.mp3'
    
    return singer, num_videos, duration, output_file


def download_songs(singer, count):
    """Download songs from YouTube"""
    try:
        from yt_dlp import YoutubeDL
    except ImportError:
        print("Error: Please install yt-dlp using: pip install yt-dlp")
        sys.exit(1)
    
    print(f"Searching for {singer} songs...")
    
    # Create temp folder
    temp_dir = Path("temp_downloads")
    temp_dir.mkdir(exist_ok=True)
    
    # Search and download
    options = {
        'format': 'bestaudio/best',
        'outtmpl': str(temp_dir / '%(title)s.%(ext)s'),
        'quiet': True,
        'no_warnings': True,
        'ignoreerrors': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
        }],
    }
    
    # Search for songs
    search_query = f"ytsearch{count*2}:{singer} song"
    
    print(f"Downloading {count} songs...")
    
    downloaded = []
    try:
        with YoutubeDL(options) as ydl:
            # Get search results first
            search_results = ydl.extract_info(search_query, download=False)
            
            if not search_results or 'entries' not in search_results:
                print("Error: No songs found")
                return []
            
            # Download videos one by one
            for i, entry in enumerate(search_results['entries'][:count]):
                if entry:
                    try:
                        url = entry.get('webpage_url') or entry.get('url')
                        print(f"  {i+1}/{count}...", end='\r')
                        ydl.download([url])
                    except:
                        continue
        
        # Get downloaded files
        downloaded = list(temp_dir.glob("*.mp3"))
        print(f"\nDownloaded {len(downloaded)} songs successfully")
        
    except Exception as e:
        print(f"Error during download: {e}")
    
    return downloaded


def cut_audio(audio_files, duration):
    """Cut first N seconds from each audio file"""
    try:
        from pydub import AudioSegment
    except ImportError:
        print("Error: Please install pydub using: pip install pydub")
        sys.exit(1)
    
    print(f"Cutting first {duration} seconds from each song...")
    
    clips_dir = Path("temp_clips")
    clips_dir.mkdir(exist_ok=True)
    
    clips = []
    duration_ms = duration * 1000
    
    for i, audio_file in enumerate(audio_files):
        try:
            # Load audio
            audio = AudioSegment.from_mp3(audio_file)
            
            # Cut first duration seconds
            clip = audio[:duration_ms]
            
            # Save clip
            clip_path = clips_dir / f"clip_{i}.mp3"
            clip.export(clip_path, format="mp3")
            clips.append(clip_path)
            
        except Exception as e:
            print(f"Warning: Skipped {audio_file.name}: {e}")
            continue
    
    print(f"Created {len(clips)} clips")
    return clips


def merge_clips(clips, output_file):
    """Merge all clips into one file"""
    try:
        from pydub import AudioSegment
    except ImportError:
        print("Error: Please install pydub")
        sys.exit(1)
    
    print("Merging clips...")
    
    # Start with empty audio
    final = AudioSegment.empty()
    
    # Add each clip
    for clip in clips:
        audio = AudioSegment.from_mp3(clip)
        final += audio
    
    # Export final mashup
    final.export(output_file, format="mp3")
    
    # Get file size
    size_mb = os.path.getsize(output_file) / (1024 * 1024)
    
    print(f"\nMashup created: {output_file}")
    print(f"Size: {size_mb:.2f} MB")
    print(f"Duration: {len(final)/1000:.0f} seconds")


def cleanup():
    """Remove temporary folders"""
    temp_dirs = ["temp_downloads", "temp_clips"]
    for folder in temp_dirs:
        if os.path.exists(folder):
            shutil.rmtree(folder)


def main():
    # Check FFmpeg
    if not shutil.which("ffmpeg"):
        print("Error: FFmpeg not found. Please install FFmpeg first.")
        sys.exit(1)
    
    # Validate inputs
    result = validate_inputs(sys.argv[1:])
    if not result:
        sys.exit(1)
    
    singer, num_videos, duration, output_file = result
    
    print(f"\n{'='*50}")
    print(f"Singer: {singer}")
    print(f"Videos: {num_videos}")
    print(f"Duration: {duration}s per video")
    print(f"Output: {output_file}")
    print(f"{'='*50}\n")
    
    try:
        # Download songs
        audio_files = download_songs(singer, num_videos)
        
        if len(audio_files) < 11:
            print(f"Error: Only downloaded {len(audio_files)} songs. Need at least 11.")
            cleanup()
            sys.exit(1)
        
        # Cut audio clips
        clips = cut_audio(audio_files[:num_videos], duration)
        
        if not clips:
            print("Error: No clips created")
            cleanup()
            sys.exit(1)
        
        # Merge clips
        merge_clips(clips, output_file)
        
        print(f"\n{'='*50}")
        print("SUCCESS!")
        print(f"{'='*50}\n")
        
    except KeyboardInterrupt:
        print("\nCancelled by user")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        cleanup()


if __name__ == "__main__":
    main()