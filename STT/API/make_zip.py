import os
import zipfile

def zip_folder(relative_folder_path):
    # Define the output zip file name based on the relative path
    output_zip_path = f"{os.path.basename(relative_folder_path)}.zip"

    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(relative_folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, relative_folder_path)
                zipf.write(file_path, arcname)

# Assuming video_folder points to 'uploads\a'
upload_dir="uploads"
video_name="a"
video_folder = os.path.join(upload_dir, video_name)
zip_folder(video_folder)
