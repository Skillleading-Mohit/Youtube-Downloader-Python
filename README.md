# **YouTube MP3 Downloader (Local Use) 🎵**  

A simple Python script to download **MP3 audio** from YouTube videos using **yt-dlp** and **FFmpeg**.  

## **🚀 Features**  
✅ Download best-quality audio from YouTube videos  
✅ Automatically converts to **MP3 (192 kbps)**  
✅ Saves file with video title as the filename  
✅ No GUI, lightweight, and easy to use  

---

## **📌 Requirements**  
Make sure you have the following installed:  

1. **Python**  → [Download here](https://www.python.org/downloads/)  
2. **yt-dlp** (YouTube downloader)  
3. **FFmpeg** (For audio conversion)  

---

## **🔧 Installation & Setup**  

### **1️⃣ Install Required Dependencies**  
Open **Command Prompt (cmd)** and run:  

```sh
pip install yt-dlp
```

### **2️⃣ Download and Set Up FFmpeg**  
1. Download FFmpeg from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/)  
2. Extract the **ZIP file** and place it in **C:\ffmpeg** (or any preferred location).  
3. Add FFmpeg to the **system PATH**:  
   - Open **Environment Variables** (Win + Search for "Environment Variables").  
   - Edit **Path** → Add **C:\ffmpeg\bin**.  
   - Click **OK**, then restart the terminal.  
4. Verify installation by running:  
   ```sh
   ffmpeg -version
   ```
   If it shows version details, FFmpeg is ready!

---

## ⚡ Usage  
1. ## Clone the Repository
To get started, clone this repository using the following command:

```sh
git clone https://github.com/Skillleading-Mohit/Youtube-Downloader-Python.git
   ```
or just download the ytdownloader.py file 

2. Run the script:  
   ```sh
   python youtube_mp3_downloader.py
   ```
3. Enter the **YouTube video URL** when prompted.  
4. The **MP3 file** will be saved in the same folder as the script.  

---

## **❗ Troubleshooting**  
- **"FFmpeg not found" error?** → Ensure FFmpeg is installed and added to the system PATH.  
- **Low audio quality?** → Change `'preferredquality': '192'` to `'320'` for better quality.  
- **File not found?** → Ensure you run the script in the correct directory.  

---

## **📜 License**  
This project is for **personal use only**. Do not use it for downloading copyrighted content.  

---

Let me know if you need any modifications!
