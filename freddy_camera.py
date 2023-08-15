from PIL import Image

frames = [
    Image.open(f"freddy_frames/{frame_num}.png").convert("RGB").resize((1280, 720))
    for frame_num in range(1, 7)
]

import colorsys
import numpy
import pyvirtualcam

with pyvirtualcam.Camera(width=1280, height=720, fps=20, device="/dev/video2") as cam:
    print(f'Using virtual camera: {cam.device}')
    while True:
        cam.send(numpy.array(frames[0]))
        cam.sleep_until_next_frame()
