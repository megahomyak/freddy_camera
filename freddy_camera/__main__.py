import threading
from PIL import Image
import numpy
import pyvirtualcam
import sounddevice
import argparse
import os

frames_path = os.path.dirname(__file__) + "/freddy_frames"

parser = argparse.ArgumentParser(
    description="Replaces your camera with Withered Freddy that talks while you're talking",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    prog="python -m freddy_camera",
)
    
parser.add_argument('-d', '--device', type=str, help="the camera device to use", default=None)
parser.add_argument('-b', '--backend', type=str, help="the camera backend to use", default=None)
parser.add_argument('-s', '--sensitivity', type=float, help="the sensitivity of the microphone", default=0.5)

args = parser.parse_args()

def block():
    threading.Event().wait()

width, height = Image.open(f"{frames_path}/1.png").size

frames = [
    numpy.array(Image.open(f"{frames_path}/{frame_num}.png"))
    for frame_num in range(1, 7)
]

with pyvirtualcam.Camera(width=width, height=height, fps=1, device=args.device, backend=args.backend) as cam:
    last_index = 0
    cam.send(frames[last_index])

    def process_sound(indata, _frames, _time, _status):
        global last_index
        volume_norm = numpy.linalg.norm(indata)
        index = int(float(volume_norm) * args.sensitivity)
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
