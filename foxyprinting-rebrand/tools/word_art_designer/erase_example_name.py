"""Erase the example name ("Anna") that some traced word art shapes still carry.

Each entry: handle -> list of boxes (x0, y0, x1, y1 as fractions of the mask) and an optional
keep strip (kx0, kx1) inside the box that belongs to the picture (a leg or a glass stem).
Leftover specks are removed afterwards. Usage: erase_example_name.py masks_dir out_dir
"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

BOXES = {
    'copy-of-personalised-ballet-1-b-word-art-poster-print': [((0.10, 0.78, 0.85, 1.0), (0.40, 0.56))],
    'copy-of-personalised-beagle-dog-word-art-poster-print': [((0.20, 0.80, 0.78, 1.0), None)],
    'copy-of-personalised-car-5-word-art-poster-print': [((0.0, 0.0, 0.88, 0.28), None)],
    'copy-of-personalised-cat-1-word-art-poster-print': [((0.15, 0.18, 0.47, 0.45), None)],
    'copy-of-personalised-dog-bone-1-word-art-poster-print': [((0.33, 0.58, 0.92, 0.93), None)],
    'copy-of-personalised-fairy-1-word-art-poster-print': [((0.15, 0.65, 0.41, 0.95), None)],
    'copy-of-personalised-penguin-1-word-art-poster-print': [((0.14, 0.72, 0.44, 0.90), None)],
    'copy-of-personalised-rainbow-1-b-word-art-poster-print': [((0.32, 0.70, 0.68, 1.0), None)],
    'copy-of-personalised-unicorn-1-word-art-poster-print': [((0.38, 0.66, 0.80, 0.86), None)],
    'copy-of-personalised-unicorn-3-word-art-poster-print': [((0.0, 0.55, 1.0, 0.80), (0.44, 0.56))],
}


def main():
    src, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    for h, boxes in BOXES.items():
        im = np.asarray(Image.open(os.path.join(src, h + '.png')).convert('RGBA')).copy()
        H, W = im.shape[:2]
        a = im[..., 3] > 128
        for (x0, y0, x1, y1), keep in boxes:
            m = np.zeros_like(a)
            m[int(y0 * H):int(y1 * H), int(x0 * W):int(x1 * W)] = True
            if keep:
                m[:, int(keep[0] * W):int(keep[1] * W)] = False
            a &= ~m
        lab, n = ndi.label(a)
        if n:
            sizes = ndi.sum(a, lab, range(1, n + 1))
            a = np.isin(lab, 1 + np.where(sizes >= 0.01 * sizes.max())[0])
        im[..., 3] = np.where(a, im[..., 3], 0)
        # The kept strip (leg / stem) still carries the name's colour: repaint it with the colour just below the box.
        for (x0, y0, x1, y1), keep in boxes:
            if not keep:
                continue
            ys, ye, xs, xe = int(y0 * H), int(y1 * H), int(keep[0] * W), int(keep[1] * W)
            below = im[min(H - 1, ye + int(0.04 * H)):min(H, ye + int(0.12 * H)), xs:xe]
            sel = below[..., 3] > 128
            if sel.any():
                im[ys:ye, xs:xe, :3] = np.median(below[sel][:, :3], axis=0).astype(np.uint8)
        Image.fromarray(im).save(os.path.join(out, h + '.png'), optimize=True)
        print(h)


if __name__ == '__main__':
    main()
