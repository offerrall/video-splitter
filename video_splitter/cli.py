import subprocess
import sys
import os
import json
from pathlib import Path

def get_video_info(input_file: str) -> tuple[int, int]:
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', input_file]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    
    for stream in data['streams']:
        if stream['codec_type'] == 'video':
            return int(stream['width']), int(stream['height'])
    
    raise ValueError("No video stream found")

def split_video(input_file: str, output_folder: str | None = None) -> None:
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    width, height = get_video_info(input_file)
    half_width = width // 2
    
    print(f"Original: {width}x{height}")
    print(f"Split: {half_width}x{height}")
    
    base_name = Path(input_file).stem
    
    if output_folder:
        output_path = Path(output_folder)
        output_path.mkdir(parents=True, exist_ok=True)
        left = str(output_path / f"{base_name}_left.mp4")
        right = str(output_path / f"{base_name}_right.mp4")
    else:
        base = os.path.splitext(input_file)[0]
        left = f"{base}_left.mp4"
        right = f"{base}_right.mp4"

    print("\nProcessing left (with audio)...")
    subprocess.run([
        'ffmpeg', '-i', input_file,
        '-vf', f'crop={half_width}:{height}:0:0',
        '-c:v', 'libx264', '-crf', '0', '-preset', 'ultrafast',
        '-c:a', 'copy', '-map', '0:v:0', '-map', '0:a?',
        '-y', left
    ], check=True)
    print(f"✓ {left}")

    print("\nProcessing right (no audio)...")
    subprocess.run([
        'ffmpeg', '-i', input_file,
        '-vf', f'crop={half_width}:{height}:{half_width}:0',
        '-c:v', 'libx264', '-crf', '0', '-preset', 'ultrafast',
        '-an', '-y', right
    ], check=True)
    print(f"✓ {right}")
    
    print("\nDone!")

def main():
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: split-video <video_file> [output_folder]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_folder = sys.argv[2] if len(sys.argv) == 3 else None
    
    split_video(input_file, output_folder)

if __name__ == "__main__":
    main()