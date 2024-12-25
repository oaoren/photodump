#!/usr/bin/env python3
import os
import shutil
from pathlib import Path
from datetime import datetime
import argparse
from collections import defaultdict

# Define target base directory for organizing files
TARGET_BASE_DIR = Path("/Volumes/RED/00_photo_raw")

# Supported file formats
PHOTO_FORMATS = [".raw", ".cr2", ".cr3", ".jpg", ".jpeg", ".png", ".tiff", ".tif"]
VIDEO_FORMATS = [".mp4", ".mov", ".avi", ".mkv"]
SUPPORTED_FORMATS = PHOTO_FORMATS + VIDEO_FORMATS

def organize_files(source_dir, target_base_dir):
    """
    Organize files from the source directory into the target directory
    based on file creation date and type (photos, videos, unknown).
    """
    source_path = Path(source_dir)
    target_base_path = Path(target_base_dir)

    # Stats for source directories and target directories
    source_stats = defaultdict(lambda: {"moved": 0, "failed": 0})
    target_stats = defaultdict(int)

    if not source_path.exists():
        print(f"Source directory {source_path} does not exist.")
        return source_stats, target_stats

    for file in source_path.rglob("*"):  # Recursively find all files
        if not file.is_file():
            print(f"Skipping {file} as it is not a file.")
            continue

        # Get file creation date
        try:
            created_time = datetime.fromtimestamp(file.stat().st_ctime)
        except Exception as e:
            print(f"Could not retrieve creation date for {file}: {e}")
            source_stats[str(file.parent)]["failed"] += 1
            continue

        # Determine target folder path based on file type
        year = created_time.strftime("%Y")
        month = created_time.strftime("%Y-%m")
        if file.suffix.lower() in PHOTO_FORMATS:
            target_folder = target_base_path / year / month
        elif file.suffix.lower() in VIDEO_FORMATS:
            target_folder = target_base_path / year / "video"
        else:
            target_folder = target_base_path / year / "unknown"

        target_file = target_folder / file.name

        # Ensure target folder exists
        target_folder.mkdir(parents=True, exist_ok=True)

        # Move the file
        try:
            if target_file.exists():
                print(f"Warning: File already exists: {target_file}")
                source_stats[str(file.parent)]["failed"] += 1
            else:
                shutil.move(str(file), target_file)
                print(f"Moved: {file} -> {target_file}")
                source_stats[str(file.parent)]["moved"] += 1
                target_stats[str(target_folder)] += 1
        except Exception as e:
            print(f"Error moving {file}: {e}")
            source_stats[str(file.parent)]["failed"] += 1

    return source_stats, target_stats

def print_summary(source_stats, target_stats):
    """Print a summary of moved and failed files for each directory."""
    print("\nSummary of file organization:")

    # Source directory summary
    print("Source Directory Summary:")
    for dir_path, counts in source_stats.items():
        print(f"Directory: {dir_path}")
        print(f"  Moved files: {counts['moved']}")
        print(f"  Failed files: {counts['failed']}")

    # Target directory summary
    print("\nTarget Directory Summary:")
    for dir_path, count in target_stats.items():
        print(f"Target Directory: {dir_path}")
        print(f"  Total files moved: {count}")

    print("\nDone.")

def main():
    parser = argparse.ArgumentParser(description="Organize files from memory cards.")
    parser.add_argument(
        "source_dir",
        type=str,
        help="Source directory (e.g., memory card path).",
    )
    parser.add_argument(
        "--target",
        type=str,
        default=TARGET_BASE_DIR,
        help=f"Target base directory for organized files (default: {TARGET_BASE_DIR}).",
    )

    args = parser.parse_args()

    source_stats, target_stats = organize_files(args.source_dir, args.target)
    print_summary(source_stats, target_stats)

if __name__ == "__main__":
    main()