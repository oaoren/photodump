# Photo and Video Organizer Script

## Overview
This Python script organizes files (photos, videos, and other file types) from a source directory (e.g., memory card) into a structured folder hierarchy in a target directory. The script processes files recursively and organizes them based on their creation date.

## Features
1. **Recursive Processing**:
   - The script traverses all subdirectories of the source directory.

2. **Automatic Organization**:
   - Photos are moved to: `./YYYY/YYYY-MM/[original_photo_filename]`
   - Videos are moved to: `./YYYY/video/[original_video_filename]`
   - Other file types are moved to: `./YYYY/unknown/[original_filename]`

3. **Duplicate Handling**:
   - If a file already exists in the target directory, it will be skipped, and a warning will be logged.

4. **Supported Formats**:
   - **Photos**: `.raw`, `.cr2`, `.cr3`, `.jpg`, `.jpeg`, `.png`, `.tiff`, `.tif`
   - **Videos**: `.mp4`, `.mov`, `.avi`, `.mkv`
   - Files not in the above formats will be categorized as "unknown."

5. **Summary Report**:
   - The script generates a summary at the end, detailing:
     - Number of files successfully moved.
     - Number of files skipped or failed.
     - Breakdown of files moved to each target directory.

## Requirements
- Python 3.8 or later.
- Standard Python libraries: `os`, `shutil`, `pathlib`, `datetime`, `argparse`, `collections`.

## Installation
1. Clone or download the repository.
2. Ensure Python 3.8 or later is installed.
3. Install dependencies (if any are added in the future):
   ```bash
   pip install -r requirements.txt