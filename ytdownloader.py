import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Downloader", page_icon="🎵")

st.title("🎬 YouTube Video & Audio Downloader")
st.write("Download YouTube videos in different formats and resolutions.")

# User input
url = st.text_input("🔗 Enter YouTube URL")

# Options
file_type = st.selectbox("📁 Select Format", ["MP3 (Audio)", "MP4 (Video)"])
resolution = st.selectbox("🎥 Select Resolution", ["Best", "1080p", "720p", "480p"])
custom_name = st.text_input("📝 Enter File Name (optional)")


def get_common_options(custom_name):
    """Common yt-dlp options for fixing 403 errors"""
    return {
        'outtmpl': f'{custom_name if custom_name else "%(title)s"}.%(ext)s',
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36'
        },
        'quiet': True,
        'noplaylist': True
    }


def download_file(url, file_type, resolution, custom_name):
    try:
        base_opts = get_common_options(custom_name)

        # Format selection
        if file_type == "MP3 (Audio)":
            ydl_opts = {
                **base_opts,
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

        else:
            if resolution == "Best":
                format_code = "best"
            elif resolution == "1080p":
                format_code = "bestvideo[height<=1080]+bestaudio/best"
            elif resolution == "720p":
                format_code = "bestvideo[height<=720]+bestaudio/best"
            elif resolution == "480p":
                format_code = "bestvideo[height<=480]+bestaudio/best"

            ydl_opts = {
                **base_opts,
                'format': format_code,
                'merge_output_format': 'mp4'
            }

        # Download
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return filename

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None


# Download button
if st.button("⬇️ Download"):
    if url:
        with st.spinner("Downloading... Please wait ⏳"):
            file_path = download_file(url, file_type, resolution, custom_name)

        if file_path and os.path.exists(file_path):
            with open(file_path, "rb") as f:
                st.success("✅ Download Complete!")
                st.download_button(
                    label="📥 Download File",
                    data=f,
                    file_name=os.path.basename(file_path)
                )
        else:
            st.error("❌ Failed to download. Try another video.")

    else:
        st.warning("⚠️ Please enter a valid URL")
