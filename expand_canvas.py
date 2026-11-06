"""
expand_canvas.py - Post-processes koi/ assets to expand the swimming pond
to a 3x-wide, 2x-tall canvas (768×512), with:
  1. Multi-directional roaming loop (Lap 1 visits right side, Lap 2 visits left side).
  2. 100% transparent background to match any GitHub theme.
"""
import math
import os
from PIL import Image, ImageSequence

TARGET_W = 768  # 3 × 256 native pixels
TARGET_H = 512  # 2 × 256 native pixels
KOI_DIR = "koi"
DRIFT_AMPLITUDE = 85  # Pixels the fish roams across the widescreen pond

def expand_gif():
    gif_path = os.path.join(KOI_DIR, "koi.gif")
    if not os.path.exists(gif_path):
        print(f"File not found: {gif_path}")
        return

    im = Image.open(gif_path)
    total_frames = im.n_frames
    src_w, src_h = im.size

    base_offset_x = (TARGET_W - 512) // 2  # 128px default center
    offset_y = (TARGET_H - 512) // 2

    rgba_frames = []
    durations = []

    for i, frame in enumerate(ImageSequence.Iterator(im)):
        rgba = frame.convert("RGBA")

        # Smooth sinusoidal wandering drift across the widescreen pond:
        # Lap 1 (frames 0..59) roams across the right side of the pond (+85px)
        # Lap 2 (frames 60..119) roams across the left side of the pond (-85px)
        # Seamless 360-degree loop with zero seam/jitter
        drift_x = int(math.sin(2.0 * math.pi * i / total_frames) * DRIFT_AMPLITUDE)
        frame_offset_x = base_offset_x + drift_x

        canvas = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
        canvas.paste(rgba, (frame_offset_x, offset_y))
        rgba_frames.append(canvas)
        durations.append(frame.info.get("duration", 70))

    rgba_frames[0].save(
        gif_path,
        format="GIF",
        save_all=True,
        append_images=rgba_frames[1:],
        loop=0,
        duration=durations,
        disposal=2,
    )
    print(f"Saved expanded roaming GIF ({TARGET_W}x{TARGET_H}, drift={DRIFT_AMPLITUDE}px): {gif_path}")

def expand_png():
    png_path = os.path.join(KOI_DIR, "koi.png")
    if not os.path.exists(png_path):
        return
    im = Image.open(png_path).convert("RGBA")
    offset_x = (TARGET_W - 512) // 2
    offset_y = (TARGET_H - 512) // 2
    canvas = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
    canvas.paste(im, (offset_x, offset_y))
    canvas.save(png_path)
    print(f"Saved expanded transparent PNG: {png_path}")

def update_preview():
    preview_path = os.path.join(KOI_DIR, "preview.html")
    if os.path.exists(preview_path):
        with open(preview_path, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace('width="512" height="512"', f'width="{TARGET_W}" height="{TARGET_H}"')
        with open(preview_path, "w", encoding="utf-8") as f:
            f.write(content)

if __name__ == "__main__":
    expand_gif()
    expand_png()
    update_preview()
