"""
expand_canvas.py - Post-processes koi/ assets to expand the swimming pond
to a 3x-wide, 2x-tall canvas (768×512), centering the full-grown koi inside it.
"""
from PIL import Image, ImageSequence
import os
import sys

TARGET_W = 768  # 3 × 256 native pixels
TARGET_H = 512  # 2 × 256 native pixels
KOI_DIR = "koi"

def expand_gif():
    gif_path = os.path.join(KOI_DIR, "koi.gif")
    if not os.path.exists(gif_path):
        print(f"File not found: {gif_path}")
        return
    im = Image.open(gif_path)
    src_w, src_h = im.size
    if (src_w, src_h) == (TARGET_W, TARGET_H):
        print(f"GIF is already {TARGET_W}x{TARGET_H}.")
        return

    offset_x = (TARGET_W - src_w) // 2
    offset_y = (TARGET_H - src_h) // 2
    print(f"Expanding GIF {src_w}x{src_h} -> {TARGET_W}x{TARGET_H}")

    frames = []
    durations = []
    for frame in ImageSequence.Iterator(im):
        rgba = frame.convert("RGBA")
        canvas = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
        canvas.paste(rgba, (offset_x, offset_y))
        frames.append(canvas.convert("P", palette=Image.Palette.ADAPTIVE, colors=255))
        durations.append(frame.info.get("duration", 70))

    frames[0].save(
        gif_path,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        loop=0,
        duration=durations,
        disposal=2,
        transparency=255,
        optimize=False,
    )
    print(f"Saved expanded GIF: {gif_path}")

def expand_png():
    png_path = os.path.join(KOI_DIR, "koi.png")
    if not os.path.exists(png_path):
        return
    im = Image.open(png_path)
    src_w, src_h = im.size
    if (src_w, src_h) == (TARGET_W, TARGET_H):
        print(f"PNG is already {TARGET_W}x{TARGET_H}.")
        return
    offset_x = (TARGET_W - src_w) // 2
    offset_y = (TARGET_H - src_h) // 2
    canvas = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
    canvas.paste(im, (offset_x, offset_y))
    canvas.save(png_path)
    print(f"Saved expanded PNG: {png_path}")

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
