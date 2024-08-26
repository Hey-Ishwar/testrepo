import cv2
import time
import os

def video_to_frames(input_loc, output_loc, fps=1):
    try:
        os.makedirs(output_loc, exist_ok=True)
    except OSError:
        print(f"Error creating directory {output_loc}")
        return

    # Log the time
    time_start = time.time()
    # Start capturing the feed
    cap = cv2.VideoCapture(input_loc)
    # Find the number of frames
    video_length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    video_fps = cap.get(cv2.CAP_PROP_FPS)
    print(f"Number of frames: {video_length}, Video FPS: {video_fps}")
    
    interval = int(video_fps / fps)
    count = 0
    frame_count = 0
    print(f"Converting video {input_loc}..\n")
    # Start converting the video
    while cap.isOpened():
        # Extract the frame
        ret, frame = cap.read()
        if not ret:
            break
        # Write the results back to output location at the specified fps
        if count % interval == 0:
            cv2.imwrite(f"{output_loc}/frame_{frame_count + 1:05d}.jpg", frame)
            frame_count += 1
        count += 1
        # If there are no more frames left
        if count >= video_length:
            break

    # Log the time again
    time_end = time.time()
    # Release the feed
    cap.release()
    # Print stats
    print(f"Done extracting frames from {input_loc}.\n{frame_count} frames extracted.")
    print(f"It took {time_end - time_start:.2f} seconds for conversion.")

def process_all_videos(input_folder, output_folder, fps=1):

    video_files = [f for f in os.listdir(input_folder) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    for video_file in video_files:
        input_loc = os.path.join(input_folder, video_file)
        output_loc = os.path.join(output_folder, os.path.splitext(video_file)[0])
        video_to_frames(input_loc, output_loc, fps)

if __name__ == "__main__":

    input_folder = '/input_videos/' 
    output_folder = 'output_frames'  
    fps = 2  
    process_all_videos(input_folder, output_folder, fps)

