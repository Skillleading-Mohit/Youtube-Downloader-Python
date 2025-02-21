import yt_dlp

def download_audio(url):
    # Define yt-dlp options
    ydl_opts = {
        'format': 'bestaudio/best',  # Select best audio format
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  # Convert audio to MP3
            'preferredquality': '192',  # Set bitrate to 192kbps
        }],
        'outtmpl': '%(title)s.%(ext)s',  # Save file with video title as name
    }

    # Download the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = input("Enter the YouTube video URL: ")
    download_audio(url)
    print("Download complete! ✅ The MP3 file is saved in the same folder.")
