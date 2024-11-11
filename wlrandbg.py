#!/usr/bin/env python3
import os
import sys
import time
import random
import subprocess
import argparse
from pathlib import Path
def process_running(process_name: str):
    result = subprocess.run(["pgrep", process_name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return result.returncode == 0  # Return True if process was found
def set_wallpaper(image_path):
    if process_running("swaybg"): subprocess.run(["pkill", "swaybg"])
    subprocess.Popen(["swaybg", "-i", str(image_path), '-m', 'fill'])
    print(f"Wallpaper set to {image_path}")
def cycle_wallpapers(directory, cycle_time, randomized):
    displayed_images = []
    while True:
        images = list(Path(directory).glob("*.jpg")) + \
                list(Path(directory).glob("*.jpeg")) + \
                list(Path(directory).glob("*.png"))
        if not images:
            print("No image files found in the specified directory.")
            sys.exit(1)
        for image in displayed_images:
            images.remove(image)
        if not images:
            displayed_images.clear()
            continue
        if randomized:
            displayed_images.append(random.choice(images))
        else:
            displayed_images.append(images[0])
        set_wallpaper(displayed_images[-1])
        time.sleep(cycle_time)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="wallpaper setter for wlroots compositors with folder cycling")
    parser.add_argument("path", help="path to an image or directory of images")
    parser.add_argument("-c", "--cycle-time", type=int, default=300, help="how fast in seconds to cycle through wallpapers when the path is a folder [default: 300]")
    parser.add_argument("-r", "--randomized", action="store_true", help="cycles through images randomly when path is a folder")
    args = parser.parse_args()
    if not args.path and not args.cycle_time and not args.randomized:
        sys.exit(0)
    else:
        try:
            if os.path.isfile(args.path):
                set_wallpaper(args.path)
            elif os.path.isdir(args.path):
                cycle_wallpapers(args.path, args.cycle_time, args.randomized)
                print(args.path, args.cycle_time, args.randomized)
            else:
                print("Error: Specified path is neither a file nor a directory.")
                sys.exit(1)
        except KeyboardInterrupt:
            print("\nInterrupted by user. Exiting...")
            subprocess.run(['pkill', 'swaybg'])
            sys.exit(0)
