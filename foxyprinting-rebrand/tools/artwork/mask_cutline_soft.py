"""Face mask cut file with a softer outline for very pale hair (used for Jimin, 6 Oct 2026).

Usage: python3 mask_cutline_soft.py face.jpg OUT_DIR eyes.json   (eyes.json: {"Jimin": [lx, ly, rx, ry]} image px)
"""
import sys, json, cv2, numpy as np
sys.path.insert(0, '/home/user/panda/foxyprinting-rebrand/tools/artwork')
import mask_cutline as M
orig = M.face_mask
def soft_mask(img):
    diff = 255 - img.min(axis=2)
    fg = (cv2.GaussianBlur(diff, (9, 9), 0) > 11).astype(np.uint8) * 255
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, np.ones((45, 45), np.uint8))
    cnts, _ = cv2.findContours(fg, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    big = max(cnts, key=cv2.contourArea)
    filled = np.zeros_like(fg); cv2.drawContours(filled, [big], -1, 255, -1)
    # smooth the hair edge
    filled = cv2.GaussianBlur(filled, (0, 0), 15); filled = ((filled > 127) * 255).astype(np.uint8)
    filled = cv2.morphologyEx(filled, cv2.MORPH_OPEN, np.ones((25, 25), np.uint8))
    return filled
M.face_mask = soft_mask
eyes = json.load(open(sys.argv[3]))
M.process(sys.argv[1], sys.argv[2], 2.0, 0.1, 26.0, 11.0, eye_override=eyes[__import__('os').path.splitext(__import__('os').path.basename(sys.argv[1]))[0]])
