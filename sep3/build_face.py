#!/usr/bin/env python3
"""Regenerate the sep3 template from the Wikimedia photo of Mikhail Shufutinsky:
downsample the photo to a cell grid (backgrounds) and emit sep3.json for SheetsOperator.
Requires ImageMagick (`magick`). Usage: python3 build_face.py"""
import json, re, subprocess, urllib.request, os
PHOTO = ("https://upload.wikimedia.org/wikipedia/commons/thumb/d/d4/"
         "%D0%9C%D0%B8%D1%85%D0%B0%D0%B8%D0%BB_%D0%A8%D1%83%D1%84%D1%83%D1%82%D0%B8%D0%BD%D1%81%D0%BA%D0%B8%D0%B9_"
         "%2803-09-2021%29_%28cropped%29.png/500px-thumbnail.png")  # taken 03-09-2021, fittingly
WIDTH = 46   # cells across; height follows the photo's aspect
def main():
    urllib.request.urlretrieve(PHOTO, "shufik.png")
    subprocess.run(["magick", "shufik.png", "-resize", f"{WIDTH}x", "-modulate", "106,118",
                    "-depth", "8", "txt:pixels.txt"], check=True)
    cells, W, H = {}, 0, 0
    for ln in open("pixels.txt"):
        m = re.match(r"(\d+),(\d+):.*?(#[0-9A-Fa-f]{6})", ln)
        if not m: continue
        x, y = int(m.group(1)), int(m.group(2)); cells[(x, y)] = "#" + m.group(3)[1:].lower()
        W = max(W, x + 1); H = max(H, y + 1)
    grid = [[cells.get((x, y), "#ffffff") for x in range(W)] for y in range(H)]
    json.dump({"banner": "И СНОВА ТРЕТЬЕ СЕНТЯБРЯ",
               "caption": "edit anything — the SheetsOperator reconciles it back",
               "w": W, "h": H, "grid": grid}, open("sep3.json", "w"))
    print(f"wrote sep3.json ({W}x{H} = {W*H} cells)")
if __name__ == "__main__":
    main()
