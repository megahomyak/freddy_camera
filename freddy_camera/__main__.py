import threading
from PIL import Image
import numpy
import pyvirtualcam
import sounddevice
import argparse
import os
import logging

frames_path = os.path.dirname(__file__) + "/frames"

parser = argparse.ArgumentParser(
    description="Replaces your camera with Withered Freddy that talks while you're talking",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    prog="python -m freddy_camera",
)
    
parser.add_argument('-vd', '--video-device', type=str, help="the camera device to use", default=None)
parser.add_argument('-ad', '--audio-device', type=str, help="the microphone device to use (index or name)", default=None)
parser.add_argument('-b', '--backend', type=str, help="the camera backend to use", default=None)
parser.add_argument('-s', '--sensitivity', type=float, help="the sensitivity of the microphone", default=0.5)
parser.add_argument('--debug', action="store_true", help="whether the debug logging is enabled or not")
parser.add_argument('-sad', '--show-audio-devices', action="store_true", help="whether to show audio devices at startup and exit")
batch_names = ", ".join(f'"{name}"' for name in os.listdir(frames_path))
parser.add_argument('-i', '--image-batch', help=f'the name of the image batch (available batches: {batch_names})', default="withered_freddy")
parser.set_defaults(debug=False)

args = parser.parse_args()

if args.show_audio_devices:
    devices: sounddevice.DeviceList = sounddevice.query_devices() # type: ignore
    for device in devices:
        if device["max_input_channels"] > 0:
            print(f"Index: {device['index']}, name: \"{device['name']}\"")
    exit()

if args.debug:
    log_level = logging.DEBUG
else:
    log_level = logging.WARNING

logging.basicConfig(format="%(asctime)s;%(levelname)s;%(message)s", level=log_level)

def block():
    threading.Event().wait()

image_batch_path = frames_path + f"/{args.image_batch}"

try:
    width, height = Image.open(f"{image_batch_path}/1.png").size
except FileNotFoundError:
    raise Exception(f'there is no "{args.image_batch}" image batch') from None

frames = []

for frame_num in range(1, 999999):
    try:
        frames.append(numpy.array(Image.open(f"{image_batch_path}/{frame_num}.png")))
    except FileNotFoundError:
        break

with pyvirtualcam.Camera(width=width, height=height, fps=60, device=args.video_device, backend=args.backend) as cam:
    logging.debug("Connected the camera using the device %s!", cam.device)
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
            logging.debug("Changing the frame to %s!", index)
            cam.send(frames[index])

    audio_device = args.audio_device
    logging.debug("Audio device variable type: %s", type(audio_device))
    if audio_device:
        try:
            audio_device = int(audio_device)
        except ValueError:
            pass

    sounddevice.InputStream(device=args.audio_device, callback=process_sound, latency=0.1).start()
    block()
