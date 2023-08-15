import threading
from PIL import Image
import numpy
import pyvirtualcam
import sounddevice
import platform

SENSITIVITY = 2
DEVICE_FILE = None if platform.platform() == "Windows" else "/dev/video111"

def block():
    threading.Event().wait()

width, height = Image.open("freddy_frames/1.png").size

frames = [
    numpy.array(Image.open(f"freddy_frames/{frame_num}.png"))
    for frame_num in range(1, 7)
]

with pyvirtualcam.Camera(width=width, height=height, fps=1, device="/dev/video2") as cam:
    print(f'Using virtual camera: {cam.device}')

    last_index = 0
    cam.send(frames[last_index])

    def process_sound(indata, _frames, _time, _status):
        global last_index
        volume_norm = numpy.linalg.norm(indata)
        index = float(volume_norm) // SENSITIVITY
        if index > last_index:
            index = last_index + 1
            if index == len(frames):
                index -= 1
        elif index < last_index:
            index = last_index - 1
        if index != last_index:
            last_index = index
            cam.send(frames[index])

    sounddevice.InputStream(callback=process_sound, latency=0.1).start()
    block()
