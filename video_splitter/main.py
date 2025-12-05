import subprocess
import sys
import os
import json

def get_video_info(input_file: str):
    cmd = ['ffprobe', '-v', 'quiet', '-print_format', 'json', '-show_streams', input_file]
    result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    data = json.loads(result.stdout)
    
    for stream in data['streams']:
        if stream['codec_type'] == 'video':
            return int(stream['width']), int(stream['height'])
    
    raise ValueError("No video stream found")

def split_video(input_file: str):
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' not found")
        sys.exit(1)
    
    width, height = get_video_info(input_file)
    half_width = width // 2
    
    print(f"Original: {width}x{height}")
    print(f"Split: {half_width}x{height}")
    
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
    if len(sys.argv) != 2:
        print("Usage: split-video <video_file>")
        sys.exit(1)
    
    split_video(sys.argv[1])

if __name__ == "__main__":
    main()