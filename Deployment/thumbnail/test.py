import cv2
import os

def save_video_thumbnail(video_path, thumbnail_folder='thumbnails'):
    # Create the thumbnail folder if it doesn't exist
    os.makedirs(thumbnail_folder, exist_ok=True)

    # Extract the video filename (without extension) as the thumbnail filename
    video_filename = os.path.splitext(os.path.basename(video_path))[0]
    thumbnail_filename = f"{video_filename}_thumbnail.jpg"
    
    # Create the full path to save the thumbnail
    thumbnail_path = os.path.join(thumbnail_folder, thumbnail_filename)

    # Create a VideoCapture object
    cap = cv2.VideoCapture(video_path)

    # Check if the video file is opened successfully
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    # Read the first frame (thumbnail)
    ret, frame = cap.read()
    if ret:
        # Save the frame as an image (thumbnail)
        cv2.imwrite(thumbnail_path, frame)
        print(f"Thumbnail saved as {thumbnail_path}")
    else:
        print("Error: Could not read the video frame.")

    # Release the VideoCapture object
    cap.release()
    return thumbnail_filename
# # Example usage:
# video=r"D:\a.mp4"
# save_video_thumbnail(video)
