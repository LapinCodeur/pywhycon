# pywhycon ![Whycon tag with ID](./whycon-code.jpg)

Python wrapper for Whycon. This is a forked of [pywhycon](https://github.com/ivomarvan/pywhycon).
I forked the project to add the modification from [Andrew123098](https://github.com/ivomarvan/pywhycon/issues/2) and update the [core](https://github.com/ivomarvan/whycon_core) with some of the update from the original [repository](https://github.com/jiriUlr/whycon-ros).

## Whycon is precise, efficient and low-cost localization system

_WhyCon_ is a version of a vision-based localization system that can be used with low-cost web cameras, and achieves millimiter precision with very high performance.
The system is capable of efficient real-time detection and precise position estimation of several circular markers in a video stream. 
It can be used both off-line, as a source of ground-truth for robotics experiments, or on-line as a component of robotic systems that require real-time, precise position estimation.
_WhyCon_ is meant as an alternative to widely used and expensive localization systems. It is fully open-source.
_WhyCon-orig_ is WhyCon's original, minimalistic version that was supposed to be ROS and openCV independent.

## Dependencies

- **OpenCV**
- **Whycon Core library** - see bellow
- **pkconfig** - only for module building
- **pybind11** - only for module building
- **numpy**

## Install

First step, clone the repo and the submodule

`git clone --recurse-submodules https://github.com/ivomarvan/pywhycon.git`

You have to install the package from your **active python environment**.

```bash
python3 -m venv whycon
source whycon/bin/activate
pip install numpy pybind11 pkgconfig
pip install opencv-python
```

## Install dependecies

```bash
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install build-essential cmake git pkg-config libjpeg-dev libtiff-dev libpng-dev
sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
sudo apt-get install libxvidcore-dev libx264-dev libgtk-3-dev
sudo apt-get install libatlas-base-dev gfortran python3-dev
sudo apt-get install build-essential cmake git
sudo apt-get install libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev
sudo apt-get install python3-dev python3-numpy libtbb2 libtbb-dev libdc1394-22-dev
sudo apt-get install libjpeg-dev libpng-dev libtiff-dev libopenexr-dev libatlas-base-dev gfortran
sudo apt-get install libhdf5-dev libhdf5-103
sudo apt-get install pybind11-dev
sudo apt-get install libopencv-dev
```

## Makefile

Compile and linking module to **./bin/whycon.so**.

(It also compiles the _Whycon Core library_.)

```bash
cd whycon_core
make all -d
cd ..
make all -d
```

## setup.py

`python3 setup.py install`

(It calls the make [see above] and installs the whycon package in the current python environment.)

## Examples

Examples are in the _usecases_ directory :
If you are using a webcam :
`python3 camera_test.py`

If you are using a depthai camera :
`python3 depthai_test.py`

### show_help.py

It only tests that the module was installed successfully. It prints the help message of the module.
`python3 show_help.py`

### autocalibration_test.py

Automatic calibration of space transformation parameters by monitoring
four WhyCon markers arranged in a square (with the configured length of its side).

### Whycon core library as a submodule

The Whycon core library is a git submodule of this repository.

If you do not have a _whycon_core_ directory in the root directory, enter :

```bash
git submodule init
git submodule update
```

## Whycon Core library

The package (pywhycon) is a wrapper of the [Whycon core library]("https://github.com/LapinCodeur/whycon_core").

**For citations of articles, contacts to the original author, please see these pages. You will also find citations of projects that contributed to the development of the Whycon.**
