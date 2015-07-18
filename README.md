# GIFer, a GIF animation maker

## Screenshots

Screenshot with generated GIF

![screenshot Shirobako](screenshots/gifer_screenshot_shirobako.PNG)

Screenshot on start.

![screenshot empty](screenshots/gifer_screenshot.PNG)

## Parameters Overview
Generate GIF animations with some most useful parameters:
- *Video File*, the video source file to generate GIF.
- *Start Time*, in second, starting time of animation in video file,
  default is zero.
- *End Time*, in second, ending time of animation in video file, default is total
  seconds of video file.
- *Width*, in pixel, width of animation, default is original video size.
- *Height*, in pixel, height of animation, default is original video size.
- *Scale*, determine animation size by multiplying (width, height) with Scale
  parameter, e.g. 0.5.
- *FPS*, frames per second of animation, default is video's original fps.
- *Speed*, play speed of animation, default is 1.0, which means keeping the
  the video's speed.
- *Mirror GIF*, make time symmetric GIF animation.

## Gallery
Don-Don Donuts, let's go nuts!

![donuts](screenshots/gifer_gallery_donuts.gif)

## How to

### Install binary file
- Windows 64 binary file

### Build from source

#### Requirements
GIFer uses [MoviePy](https://github.com/Zulko/moviepy) to make GIF animations.
The GUI is made using [PyQt4](http://www.riverbankcomputing.com/software/pyqt/download).

##### Install Requirements
1. Install [SIP](http://www.riverbankcomputing.com/software/sip/download).
2. Install [PyQt4](http://www.riverbankcomputing.com/software/pyqt/download).
3. Install MoviePy, `pip install moviepy`.

#### Build
`python build.py`
