#!/usr/bin/env python
# coding: utf-8
from pytubefix import YouTube
from moviepy.audio.io.AudioFileClip import AudioFileClip
import pandas as pd
# Tải video YouTube chất lượng cao nhất và ghép với âm thanh
def download_high_quality_youtube_video(video_url):
    try:
        yt = YouTube(video_url)
        title = yt.title.replace("/", "-").replace("\\", "-").replace(":", "-").replace("?", "-").replace("*", "-").replace('"', '-').replace('<', '-').replace('>', '-').replace('|', '-')
        print(f"Đang tải âm nhạc: {title}")
        # Đặt tên file đầu ra
        output_filename = f"{title}.mp4"
        output_filename = "Music Output/" + output_filename  # Đảm bảo lưu vào thư mục Output
        
        # Tải audio chất lượng cao nhất
        audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()
        audio_path = "temp_audio.mp4"
        audio_stream.download(filename=audio_path)

        # Chuyển đổi định dạng âm thanh sang mp3
        audio_clip = AudioFileClip(audio_path)
        audio_clip.write_audiofile(output_filename, codec='mp3')
        audio_clip.close()

        print(f"✅ Đã tải âm nhạc: '{title}' và lưu vào '{output_filename}'")
        audio_clip.close()
    except Exception as e:
        print(f"❌ Lỗi xảy ra: {e}")
    return output_filename
def delete_temp_audio():
    import os
    temp_audio_path = "temp_audio.mp4"
    if os.path.exists(temp_audio_path):
        os.remove(temp_audio_path)
# Đọc thông tin từ excel và tải video
def download_videos_from_excel(excel_file):
    df = pd.read_excel(excel_file)
    df["Tiêu đề"] = df["Tiêu đề"].astype(str)
    df["Trạng thái"] = df["Trạng thái"].astype(str)
    for index, row in df.iterrows():
        if row['Trạng thái'] == "Đã tải":
            continue  # Bỏ qua nếu video đã được tải
        try:
            video_url = row['Link']
            video_title = download_high_quality_youtube_video(video_url)
            # Cập nhật tiêu đề và trạng thái
            df.at[index, "Tiêu đề"] = video_title
            df.at[index, "Trạng thái"] = "Đã tải"
        except Exception as e:
            print(f"❌ Lỗi với {row['Link']}: {e}")
    # Ghi lại vào file Excel
    df.to_excel("video_list.xlsx", index=False)
    delete_temp_audio()
download_videos_from_excel("music_list.xlsx")