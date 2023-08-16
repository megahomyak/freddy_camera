# Freddy Camera

**Disclaimer**: I do not own Five Nights At Freddy's (the game from which the character and the jumpscare were taken from). This program is just a little silly joke.

**Advice**: if you had any issues during the installation, usage, or configuration of the program, please, contact the developer at https://t.me/megahomyak

This program will allow you to create a fake webcam and put the magnificient FREDDY FAZBEAR as its output. You will be able to use the added camera in Discord, Skype and other applications that accept camera output and allow you to choose the camera. Freddy's jaw will move with you speaking! All of the Freddy frames are taken from his jumpscare.

## Screenshots

![Me being FREDDY FAZBEAR in a Discord call, jaw closed](screenshots/closed_jaw.png "Me being FREDDY FAZBEAR in a Discord call, jaw closed")
![Me being FREDDY FAZBEAR in a Discord call, jaw open](screenshots/open_jaw.png "Me being FREDDY FAZBEAR in a Discord call, jaw open")

## Demonstration video

https://m.youtube.com/watch?v=LgtxSnCMJFs

## Installation

* Install Python (https://www.python.org/)
* Open the console
* Execute `pip install freddy_camera`
* Wait until the installation completes
* **Windows**: install OBS (https://obsproject.com/)
* **macOS**: install OBS (https://obsproject.com/), start OBS, click "Start Virtual Camera", click "Stop Virtual Camera", close OBS
* **Linux**: install v4l2loopback (`sudo apt install v4l2loopback-dkms`), check what cameras your system currently has (`ls /dev/ | grep video`), create a new virtual camera (`sudo modprobe v4l2loopback devices=1`), a new camera should appear on the list (`ls /dev/ | grep video`, compare to the previous output), remember the name of this new camera

## Usage

* **Windows or macOS**: execute `python -m freddy_camera`
* **Linux**: execute `python -m freddy_camera -d /dev/PUT_THE_NAME_OF_THE_CAMERA_HERE` (for example, `python -m freddy_camera -d /dev/video2`)
* In the settings of the application you're going to use, select the new camera
* To stop the program, press Control+c on your keyboard

## Settings

Type in `python -m freddy_camera --help` to get the list of available settings.
