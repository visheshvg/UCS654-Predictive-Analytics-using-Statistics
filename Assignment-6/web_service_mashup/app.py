"""
Mashup Web App - Streamlit Version
Simple web interface for creating music mashups
"""

import streamlit as st
import os
import sys
import shutil
import re
import smtplib
import zipfile
from pathlib import Path
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email import encoders
import tempfile

# Page setup
st.set_page_config(page_title="Mashup Generator", page_icon="🎵")

# Simple CSS
st.markdown("""
    <style>
    .main { padding: 2rem; }
    h1 { color: #1f77b4; text-align: center; }
    </style>
""", unsafe_allow_html=True)


def check_email(email):
    """Check if email is valid"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def download_songs(singer, count):
    """Download songs from YouTube"""
    from yt_dlp import YoutubeDL
    
    temp_dir = Path(tempfile.mkdtemp())
    
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
    
    # Search for more videos to increase chances
    search_query = f"ytsearch{count*3}:{singer} song"
    
    downloaded = []
    try:
        with YoutubeDL(options) as ydl:
            search_results = ydl.extract_info(search_query, download=False)
            
            if search_results and 'entries' in search_results:
                # Try to download more than requested
                for entry in search_results['entries'][:count*2]:
                    if entry:
                        try:
                            url = entry.get('webpage_url') or entry.get('url')
                            ydl.download([url])
                            
                            # Stop if we have enough
                            current_files = list(temp_dir.glob("*.mp3"))
                            if len(current_files) >= count:
                                break
                        except:
                            continue
        
        downloaded = list(temp_dir.glob("*.mp3"))
    except:
        pass
    
    return downloaded, temp_dir


def cut_and_merge(audio_files, duration, output_file):
    """Cut audio clips and merge them"""
    from pydub import AudioSegment
    
    duration_ms = duration * 1000
    final = AudioSegment.empty()
    
    for audio_file in audio_files:
        try:
            audio = AudioSegment.from_mp3(audio_file)
            clip = audio[:duration_ms]
            final += clip
        except:
            continue
    
    final.export(output_file, format="mp3")
    return output_file


def create_zip_file(file_path):
    """Create zip file"""
    zip_path = file_path.replace('.mp3', '.zip')
    with zipfile.ZipFile(zip_path, 'w') as zipf:
        zipf.write(file_path, os.path.basename(file_path))
    return zip_path


def send_email(to_email, zip_file, singer):
    """Send email with attachment"""
    
    # Get credentials from secrets
    try:
        from_email = st.secrets.get("SENDER_EMAIL", "")
        password = st.secrets.get("SENDER_PASSWORD", "")
    except:
        return False
    
    if not from_email or not password:
        return False
    
    # Create email
    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = f'Your {singer} Mashup'
    
    body = f"""
Hello!

Your mashup for {singer} is ready!

Please find it attached.

Enjoy!
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Attach file
    with open(zip_file, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
    
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', f'attachment; filename={os.path.basename(zip_file)}')
    msg.attach(part)
    
    # Send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        server.send_message(msg)
        server.quit()
        return True
    except:
        return False


def cleanup(temp_dir, output_file, zip_file):
    """Clean up files"""
    try:
        if temp_dir and os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        if output_file and os.path.exists(output_file):
            os.remove(output_file)
        if zip_file and os.path.exists(zip_file):
            os.remove(zip_file)
    except:
        pass


# Main app
st.title("🎵 Mashup Generator")
st.write("Create awesome mashups from your favorite singer's songs!")

# Form
with st.form("mashup_form"):
    col1, col2 = st.columns(2)
    
    with col1:
        singer = st.text_input("Singer Name", placeholder="e.g., Arijit Singh")
        num_videos = st.number_input("Number of Videos", min_value=11, max_value=50, value=15)
    
    with col2:
        duration = st.number_input("Duration (seconds)", min_value=21, max_value=60, value=30)
        email = st.text_input("Email Address", placeholder="your@email.com")
    
    submit = st.form_submit_button("Generate Mashup", use_container_width=True)

# Process form
if submit:
    # Validate
    errors = []
    
    if not singer.strip():
        errors.append("Please enter a singer name")
    
    if num_videos <= 10:
        errors.append("Number of videos must be greater than 10")
    
    if duration <= 20:
        errors.append("Duration must be greater than 20 seconds")
    
    if not email or not check_email(email):
        errors.append("Please enter a valid email address")
    
    if errors:
        for error in errors:
            st.error(error)
    else:
        # Generate mashup
        output_file = f"mashup_{singer.replace(' ', '_')}.mp3"
        zip_file = None
        temp_dir = None
        
        try:
            # Show progress
            progress = st.progress(0)
            status = st.empty()
            
            # Download
            status.text(f"Searching for {singer} songs...")
            progress.progress(20)
            
            audio_files, temp_dir = download_songs(singer, num_videos)
            
            # Be more lenient - accept at least half of requested or minimum 5
            min_required = max(5, num_videos // 2)
            
            if len(audio_files) < min_required:
                st.error(f"Only found {len(audio_files)} songs. Need at least {min_required}. Try a different singer.")
            else:
                status.text(f"Downloaded {len(audio_files)} songs")
                progress.progress(50)
                
                # Use what we got (up to num_videos)
                songs_to_use = min(len(audio_files), num_videos)
                
                # Cut and merge
                status.text(f"Creating mashup from {songs_to_use} songs...")
                cut_and_merge(audio_files[:songs_to_use], duration, output_file)
                progress.progress(70)
                
                # Create zip
                status.text("Creating zip file...")
                zip_file = create_zip_file(output_file)
                progress.progress(90)
                
                # Success
                progress.progress(100)
                status.text("Done!")
                
                st.success("✅ Mashup created successfully!")
                
                # Download button
                with open(zip_file, 'rb') as f:
                    st.download_button(
                        label="📥 Download Mashup",
                        data=f,
                        file_name=os.path.basename(zip_file),
                        mime="application/zip"
                    )
                
                # Send email
                st.info("Sending email...")
                if send_email(email, zip_file, singer):
                    st.success(f"📧 Sent to {email}!")
                else:
                    st.warning("Email not sent (download above instead)")
                
        except Exception as e:
            st.error(f"Error: {str(e)}")
        
        finally:
            # Cleanup
            cleanup(temp_dir, output_file, zip_file)

# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Made with Streamlit</p>", unsafe_allow_html=True)