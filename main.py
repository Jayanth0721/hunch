import streamlit as st
from pytube import YouTube
import os
import re

st.set_page_config(layout='wide')
st.markdown('<h1 style="font-size: 100px;">Hunch..</h1>', unsafe_allow_html=True)
st.write('Welcome folks!')

def get_video_id(youtube_url):
    video_id_match = re.match(r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
                             '(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})', youtube_url)
    if video_id_match:
        return video_id_match.group(6)
    else:
        return None

def sanitize_filename(filename):
    invalid_chars = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    return filename

def get_available_quality_options(youtube_url):
    try:
        video_id = get_video_id(youtube_url)
        if video_id:
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
            all_quality_options = [stream.resolution for stream in yt.streams.filter(file_extension="mp4") if stream.resolution]
            
            # Display available quality options
            if all_quality_options:
                all_quality_options.sort()
                all_quality_options = list(set(all_quality_options))  # Convert back to list to preserve order
                st.info(f"Available quality options: {', '.join(all_quality_options)}")
                return all_quality_options
            else:
                st.warning("No valid quality options found.")
                return []
        else:
            st.warning("Insert URL")
            return []
    except Exception as e:
        st.error(f"An error occurred while fetching quality options: {str(e)}")
        return []

def download_video(youtube_url, video_quality):
    try:
        video_id = get_video_id(youtube_url)
        if video_id:
            yt = YouTube(f"https://www.youtube.com/watch?v={video_id}")
        
            # Try a different stream if the selected quality is not available
            video_stream = yt.streams.filter(res=video_quality, file_extension="mp4").first()
            if not video_stream:
                st.warning("Selected video quality not available. Fallback to a lower resolution.")
                video_stream = yt.streams.filter(file_extension="mp4").first()

            if video_stream:
                st.success("Downloading... Please wait.")
                
                # Sanitize the filename before saving
                sanitized_filename = sanitize_filename(video_stream.title)
                
                download_path = os.path.join("downloads", sanitized_filename + ".mp4")
                video_stream.download(download_path)
                st.success(f"Download complete! [Download Link](/{download_path})")
            else:
                st.error("No suitable video stream available.")
        else:
            st.warning("Invalid YouTube video URL. Please check the URL and try again.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

def main():
    st.header("YouTube Video Downloader")

    # Get YouTube URL input from the user
    youtube_url = st.text_input("Enter YouTube Video URL:")

    # Fetch and display available video quality options
    quality_options = get_available_quality_options(youtube_url)
    if not quality_options:
        st.stop()

    # Choose video quality
    video_quality = st.selectbox("Select Video Quality:", quality_options)

    # Display image using URL
    st.markdown(
        f'<div style="display: flex; justify-content: center;">'
        f'<img src="{image_url}" alt="Your Image" width="300"/>'
        f'</div>',
        unsafe_allow_html=True
    )

    # Display download button
    if st.button("Download"):
        if youtube_url:
            download_video(youtube_url, video_quality)
        else:
            st.warning("Please enter a YouTube video URL.")
    st.text("Thanks")


# Image URL
image_url = "https://th.bing.com/th/id/OIP.x0Rq4SdaNp4GwHuiWh6r1gHaGC?w=212&h=180&c=7&r=0&o=5&dpr=1.3&pid=1.7"



st.markdown("<p style='color: red;'>If the downloaded video is unplayable, please try downloading it in a different quality.</p>", unsafe_allow_html=True)






if __name__ == "__main__":
    main()


