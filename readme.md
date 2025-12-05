# Video Splitter

Split videos horizontally into two halves. Left clip keeps audio, right clip has no audio.

## Installation

```bash
pip install git+https://github.com/offerrall/video-splitter.git
```

## Usage
```bash
split-video video.mp4
```

**Output:**
- `video_left.mp4` (with audio)
- `video_right.mp4` (no audio)

## Requirements

- Python 3.7+
- ffmpeg and ffprobe installed and available in PATH.

## Uninstall
```bash
pip uninstall video-splitter
```