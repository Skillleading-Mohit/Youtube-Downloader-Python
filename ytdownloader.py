import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="Pro YouTube Downloader", page_icon="🎬")

st.title("🎬 Pro YouTube Downloader")
st.write("Download videos & audio with preview, formats, and quality selection.")

url = st.text_input("🔗 Enter YouTube URL")

# -------------------------
# Common yt-dlp options
# -------------------------
def get_common_options():
    return {
        'quiet': True,
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                          'AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/120.0.0.0 Safari/537.36'
        },
    }


# -------------------------
# Get video info
# -------------------------
def fetch_video_info(url):
    try:
        with yt_dlp.YoutubeDL(get_common_options()) as ydl:
            info = ydl.extract_info(url, download=False)
        return info
    except:
        return None


# -------------------------
# UI: Show Video Preview
# -------------------------
if url:
    with st.spinner("Fetching video info..."):
        info = fetch_video_info(url)

    if info:
        st.image(info.get("thumbnail"))
        st.subheader(info.get("title"))

        formats = info.get("formats", [])

        video_formats = []
        audio_available = False

        for f in formats:
            if f.get("vcodec") != "none":
                resolution = f.get("format_note") or f.get("height")
                ext = f.get("ext")
                if resolution:
                    video_formats.append(f"{resolution} - {ext}")
            if f.get("acodec") != "none" and f.get("vcodec") == "none":
                audio_available = True

        video_formats = list(set(video_formats))
        video_formats.sort(reverse=True)

        file_type = st.selectbox("📁 Select Format", ["MP4 (Video)", "MP3 (Audio)"])

        selected_format = None

        if file_type == "MP4 (Video)":
            selected_format = st.selectbox("🎥 Select Quality", video_formats)
        else:
            if audio_available:
                st.success("Audio available ✅")
            selected_format = "bestaudio"

        custom_name = st.text_input("📝 Custom File Name (optional)")

# -------------------------
# Download logic
# -------------------------
def download_file(url, format_choice, file_type, custom_name):
    try:
        base_opts = get_common_options()

        filename_template = f'{custom_name if custom_name else "%(title)s"}.%(ext)s'

        if file_type == "MP3 (Audio)":
            ydl_opts = {
                **base_opts,
                'format': 'bestaudio',
                'outtmpl': filename_template,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

        else:
            # Extract resolution number from selected option
            height = None
            if isinstance(format_choice, str):
                for part in format_choice.split():
                    if part.isdigit():
                        height = part

            if height:
                format_code = f"bestvideo[height<={height}]+bestaudio/best"
            else:
                format_code = "best"

            ydl_opts = {
                **base_opts,
                'format': format_code,
                'outtmpl': filename_template,
                'merge_output_format': 'mp4'
            }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        return filename

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        return None


# -------------------------
# Download Button
# -------------------------
if url and st.button("⬇️ Download"):
    with st.spinner("Downloading... ⏳"):
        file_path = download_file(url, selected_format, file_type, custom_name)

    if file_path and os.path.exists(file_path):
        with open(file_path, "rb") as f:
            st.success("✅ Download Complete!")

            st.download_button(
                label="📥 Download File",
                data=f,
                file_name=os.path.basename(file_path)
            )
    else:
        st.error("❌ Download failed. Try another video.")