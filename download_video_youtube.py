#!/usr/bin/env python
# coding: utf-8
from pytubefix import YouTube
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
import pandas as pd
# Tải video YouTube chất lượng cao nhất và ghép với âm thanh
def download_high_quality_youtube_video(video_url):
    try:
        yt = YouTube(video_url)
        title = yt.title
        print(f"Đang tải video: {title}")
        # Tải video chất lượng cao nhất (không có âm thanh)
        video_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_video=True).order_by('resolution').desc().first()
        video_path = "temp_video.mp4"
        video_stream.download(filename=video_path)
        # Tải audio chất lượng cao nhất
        audio_stream = yt.streams.filter(adaptive=True, file_extension='mp4', only_audio=True).order_by('abr').desc().first()
        audio_path = "temp_audio.mp4"
        audio_stream.download(filename=audio_path)
        # Ghép video và audio bằng moviepy
        video_clip = VideoFileClip(video_path)
        audio_clip = AudioFileClip(audio_path)
        final_clip = video_clip.with_audio(audio_clip)
        # Đặt tên file đầu ra
        output_filename = f"{title}.mp4"
        output_filename = "Video Output/" + output_filename  # Đảm bảo lưu vào thư mục Output
        # Lưu video đã ghép
        final_clip.write_videofile(output_filename, codec="libx264", audio_codec="aac")
        print(f"✅ Đã tải video: '{title}' và lưu vào '{output_filename}'")
    except Exception as e:
        print(f"❌ Lỗi xảy ra: {e}")
    return output_filename
# Xoá các file tạm thời sau khi hoàn thành
def delete_temp_files():
    import os
    if os.path.exists("temp_video.mp4"):
        os.remove("temp_video.mp4")
    if os.path.exists("temp_audio.mp4"):
        os.remove("temp_audio.mp4")
# Đọc thông tin từ excel và tải video
def download_videos_from_excel(excel_file):
    df = pd.read_excel(excel_file)
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
    delete_temp_files()
download_videos_from_excel("video_list.xlsx")
