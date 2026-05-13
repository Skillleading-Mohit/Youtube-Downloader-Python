import streamlit as st
import yt_dlp
import os
import random

st.set_page_config(page_title="Ultimate YouTube Downloader", page_icon="🚀")

st.title("🚀 Ultimate YouTube Downloader (403-Proof)")
st.write("Smart downloader with auto-retry, fallback & format optimization.")

url = st.text_input("🔗 Enter YouTube URL")

# --------------------------
# Advanced Headers Pool
# --------------------------
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (X11; Linux x86_64)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
]

# --------------------------
# Common options
# --------------------------
def get_common_options(custom_name):
    return {
        'outtmpl': f'{custom_name if custom_name else "%(title)s"}.%(ext)s',
        'quiet': True,
        'noplaylist': True,

        # ✅ Rotate headers (avoid detection)
        'http_headers': {
            'User-Agent': random.choice(USER_AGENTS)
        },

        # ✅ Use multiple clients (SUPER IMPORTANT)
        'extractor_args': {
            'youtube': {
                'player_client': ['android', 'web']
            }
        },

        # ✅ Retry system
        'retries': 5,
        'fragment_retries': 5,

        # ✅ Prefer safe formats
        'format_sort': ['res', 'ext:mp4:m4a'],

        # ✅ Timeout protection
        'socket_timeout': 15,

        # ✅ Optional cookies (uncomment if added)
        # 'cookiefile': 'cookies.txt'
    }

# --------------------------
# Get video info
# --------------------------
def get_video_info(url):
    try:
        with yt_dlp.YoutubeDL(get_common_options(None)) as ydl:
            return ydl.extract_info(url, download=False)
    except:
        return None

# --------------------------
# Smart Download Engine
# --------------------------
def smart_download(url, file_type, resolution, custom_name):
    base_opts = get_common_options(custom_name)

    # ✅ Different strategies (fallback system)
    strategies = []

    if file_type == "MP3":
        strategies = [
            {**base_opts,
             'format': 'bestaudio'},
        ]
    else:
        # Progressive FIRST (most stable)
        if resolution != "Best":
            res = resolution.replace("p", "")
            strategies.append({
                **base_opts,
                'format': f'best[height<={res}]'
            })

        # Then full best
        strategies.append({
            **base_opts,
            'format': 'best'
        })

        # LAST fallback (merge, risky)
        if resolution != "Best":
            res = resolution.replace("p", "")
            strategies.append({
                **base_opts,
                'format': f'bestvideo[height<={res}]+bestaudio/best',
                'merge_output_format': 'mp4'
            })

    # ✅ Try all strategies (AUTO FALLBACK)
    for i, opts in enumerate(strategies):
        try:
            st.info(f"⚙️ Trying method {i+1}...")

            with yt_dlp.YoutubeDL(opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            return filename

        except Exception as e:
            st.warning(f"❌ Method {i+1} failed")

    return None

# --------------------------
# UI Preview
# --------------------------
if url:
    with st.spinner("Fetching video info..."):
        info = get_video_info(url)

    if info:
        st.image(info.get("thumbnail"))
        st.subheader(info.get("title"))

        file_type = st.selectbox("📁 Format", ["MP4", "MP3"])
        resolution = st.selectbox("🎥 Resolution", ["Best", "1080p", "720p", "480p"])
        custom_name = st.text_input("📝 File Name (optional)")

# --------------------------
# Download Button
# --------------------------
if url and st.button("⬇️ Download"):
    with st.spinner("Downloading smartly... ⏳"):
        file_path = smart_download(url, file_type, resolution, custom_name)

    if file_path and os.path.exists(file_path):
        with open(file_path, "rb") as f:
            st.success("✅ Download Complete!")

            st.download_button(
                label="📥 Download File",
                data=f,
                file_name=os.path.basename(file_path)
            )
    else:
        st.error("❌ ALL methods failed. Try another video.")