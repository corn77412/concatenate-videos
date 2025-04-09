import subprocess  # Import the subprocess module to run external commands like FFmpeg.
import os  # Import the os module for operating system related tasks, like file path manipulation.
import natsort  # Import the natsort module for natural sorting of strings.

def concatenate_videos_ffmpeg(video_folder, output_video):
    """
    Uses FFmpeg to concatenate MP4 video files in a specified folder, sorted by filename, into a single output video file.

    Args:
        video_folder (str): The path to the folder containing the MP4 video files.
        output_video (str): The desired filename for the concatenated output video file.
    """

    video_files = [f for f in os.listdir(video_folder) if f.endswith('.mp4')]  # Create a list of all MP4 files in the given folder.
    sorted_video_files = natsort.natsorted(video_files)  # Sort the video files naturally by their filenames.

    # Create the content for the filelist.txt
    file_list_content = ""
    for filename in sorted_video_files:
        file_path = os.path.join(video_folder, filename)  # Create the full path to each video file.
        file_list_content += f"file '{file_path.replace('\\', '/')}'\n"  # Format each file path for FFmpeg's concat demuxer, replacing backslashes with forward slashes.

    # Write the content to filelist.txt in the current working directory
    filelist_path = "filelist.txt"
    with open(filelist_path, "w", encoding="utf-8") as f:  # Open filelist.txt in write mode with UTF-8 encoding.
        f.write(file_list_content)  # Write the list of video file paths to filelist.txt.

    print(f"已生成 filelist.txt，內容如下：\n{file_list_content}")  # Print the content of filelist.txt for inspection.

    # Build the FFmpeg command
    ffmpeg_cmd = [
        'ffmpeg',
        '-f', 'concat',
        '-safe', '0',
        '-i', filelist_path,  # Specify the input filelist.txt.
        '-c', 'copy',  # Instruct FFmpeg to stream copy the video and audio without re-encoding.
        output_video  # Specify the output video file.
    ]

    try:
        # Execute the FFmpeg command
        subprocess.run(ffmpeg_cmd, check=True)  # Run the FFmpeg command and raise an exception if it returns a non-zero exit code.
        print(f"影片已成功串接並儲存至：{output_video}")  # Print a success message.
    except subprocess.CalledProcessError as e:
        print(f"FFmpeg 執行錯誤：{e}")  # Print an error message if FFmpeg execution fails.
    except FileNotFoundError:
        print("找不到 FFmpeg，請確認 FFmpeg 是否已安裝並加入系統路徑。")  # Print an error message if FFmpeg executable is not found.
    finally:
        # Remove the temporary filelist.txt file
        if os.path.exists(filelist_path):
            os.remove(filelist_path)  # Delete filelist.txt after FFmpeg execution.

# Example usage
video_folder = input("請輸入影片資料夾路徑：")  # Prompt the user to input the path to the video folder.
output_video = r"D:\114年高雄市健康職場幸福永續論壇暨展示活動\concatenated_video.mp4"  # Define the output video file path.
concatenate_videos_ffmpeg(video_folder, output_video)  # Call the function to concatenate the videos.
