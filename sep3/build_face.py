#!/usr/bin/env python3
"""Regenerate the sep3 template from the Wikimedia photo of Mikhail Shufutinsky:
downsample the photo to a cell grid (backgrounds) and emit sep3.json for SheetsOperator.
Requires ImageMagick (`magick`). Usage: python3 build_face.py"""
import json, re, subprocess, urllib.request, os
PHOTO = ("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/"
         "%D0%9C%D0%B8%D1%85%D0%B0%D0%B8%D0%BB_%D0%A8%D1%83%D1%84%D1%83%D1%82%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_"
         "%2803-09-2021%29_%28cropped%29.png/500px-thumbnail.png")  # taken 03-09-2021, fittingly
WIDTH = 138  # cells across; ~3x detail
def main():
    req = urllib.request.Request(PHOTO, headers={"User-Agent": "sncf-sep3/1.0 (demos)"})
    with urllib.request.urlopen(req) as r, open("shufik.png", "wb") as f:
        f.write(r.read())
    subprocess.run(["magick", "shufik.png", "-resize", f"{WIDTH}x", "-modulate", "106,118",
                    "-depth", "8", "txt:pixels.txt"], check=True)
    cells, W, H = {}, 0, 0
    for ln in open("pixels.txt"):
        m = re.match(r"(\d+),(\d+):.*?(#[0-9A-Fa-f]{6})", ln)
        if not m: continue
        x, y = int(m.group(1)), int(m.group(2)); cells[(x, y)] = "#" + m.group(3)[1:].lower()
        W = max(W, x + 1); H = max(H, y + 1)
    grid = [[cells.get((x, y), "#ffffff") for x in range(W)] for y in range(H)]
    strip, SW, SH = build_strip(W)
    json.dump({"banner": "И СНОВА ТРЕТЬЕ СЕНТЯБРЯ",
               "caption": "edit anything — the SheetsOperator reconciles it back",
               "banner2": "\U0001F525 ГОРЯТ КОСТРЫ РЯБИН \U0001F525",
               "w": W, "h": H, "grid": grid,
               "strip": strip, "strip_w": SW, "strip_h": SH}, open("sep3.json", "w"))
    print(f"wrote sep3.json ({W}x{H} face + {SW}x{SH} strip)")

def build_strip(width, height=26):
    """A pixel band under the face: bonfires (burning) and rowan berry clusters,
    drawn as cell backgrounds — 'горят костры рябин' rendered in cells."""
    BG, LOG = "#140f0a", "#5a3a1a"
    RED, ORANGE, YELLOW = "#c0201f", "#e8631a", "#f5c542"
    BERRY, LEAF, TWIG = "#d1202a", "#3f6b2e", "#6b4a2a"
    g = [[BG] * width for _ in range(height)]
    def fire(cx):
        base = height - 2
        for x in range(cx - 6, cx + 7):
            if 0 <= x < width: g[base][x] = LOG
        for lvl in range(14):
            row = base - 1 - lvl
            if row < 1: break
            hw = max(0, 6 - lvl // 2)
            col = RED if lvl < 4 else (ORANGE if lvl < 8 else YELLOW)
            for x in range(cx - hw, cx + hw + 1):
                if 0 <= x < width: g[row][x] = col
    def rowan(cx):
        for y in range(6):
            if 0 <= cx < width: g[y][cx] = TWIG
        for yy, xx in [(4, -2), (4, 2), (5, -3), (5, 3)]:
            if 0 <= cx + xx < width: g[yy][cx + xx] = LEAF
        for dy, dx in [(6,0),(7,-1),(7,1),(8,-2),(8,0),(8,2),(9,-3),(9,-1),(9,1),(9,3),(10,0)]:
            if 0 <= cx + dx < width and dy < height: g[dy][cx + dx] = BERRY
    step = max(30, width // 3)
    for i, cx in enumerate(range(step // 2, width, step)): fire(cx)
    for cx in range(step, width, step): rowan(cx)
    rowan(4)
    return g, width, height
if __name__ == "__main__":
    main()
