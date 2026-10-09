"""Mask of the DCD TEAMWEAR logo inside a box (black outline + white + blue lettering)."""
import cv2, numpy as np

def logo_mask(im, box, grow=9):
    x0, y0, x1, y1 = box
    pad = 15
    sub = im[y0 - pad:y1 + pad, x0 - pad:x1 + pad]
    hsv = cv2.cvtColor(sub, cv2.COLOR_BGR2HSV)
    b, r = sub[..., 0].astype(int), sub[..., 2].astype(int)
    v, s = hsv[..., 2].astype(int), hsv[..., 1].astype(int)
    raw = ((v < 70) | ((s < 50) & (v > 190)) | (b > r + 20)).astype(np.uint8) * 255
    raw = cv2.morphologyEx(raw, cv2.MORPH_CLOSE, np.ones((5, 5), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(raw, 8)
    keep = np.zeros_like(raw)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] > 1500 * (im.shape[1] / 2000) ** 2:
            keep[lab == i] = 255
    cnts, _ = cv2.findContours(keep, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(keep, cnts, -1, 255, -1)
    g = max(3, int(grow * im.shape[1] / 2000)) | 1
    keep = cv2.dilate(keep, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (g, g)))
    m = np.zeros(im.shape[:2], np.uint8)
    m[y0 - pad:y1 + pad, x0 - pad:x1 + pad] = keep
    return m
