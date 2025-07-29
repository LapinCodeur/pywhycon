#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = "Ivo Marvan"
__email__ = "ivo@marvan.cz"
__description__ = '''
    Read images from camera and use whycon module.
    
    Calibration of coordinate transformation using 4 marks arranged in a square.
    Calibration is completed by finding a sufficient number of images with 4 marks found.
    
'''
import os
import sys
import argparse
from time import time, sleep

# root of project repository
THE_FILE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.abspath(os.path.join(THE_FILE_DIR, '..'))
sys.path.append(PROJECT_ROOT)

parser = argparse.ArgumentParser(description=__description__)
parser.add_argument("--set_cam_calib_path", help="Load the camera calibration file", type=str)
parser.add_argument("--set_space_calib_path_in", help="Load the space calibration file", type=str)
parser.add_argument("--set_space_calib_path_out", help="Path to save the space calibration file", type=str)
args = parser.parse_args()

try:
    from whycon import WhyCodeDetector, SpaceTransofmType as TransType
    import whycon
    print(f'Use installed whycon package in "{whycon.__file__}"')
except ModuleNotFoundError:
    PACKAGE_DIR = os.path.abspath(os.path.join(PROJECT_ROOT, 'bin'))
    sys.path.append(PACKAGE_DIR)
    from whycon import WhyCodeDetector, SpaceTransofmType as TransType
    print(f'Use whycon paskage from local installation: "{PACKAGE_DIR}"')

from window import ImgStorageWindow
import depthai

pipeline = depthai.Pipeline()

# First, we want the Color camera as the output
cam_rgb = pipeline.createColorCamera()
cam_rgb.setResolution(depthai.ColorCameraProperties.SensorResolution.THE_1352X1012)
cam_rgb.setInterleaved(False)
cam_rgb.setColorOrder(depthai.ColorCameraProperties.ColorOrder.BGR)
cam_rgb.setVideoSize(1352, 1012)

# XLinkOut is a "way out" from the device. Any data you want to transfer to host need to be send via XLink
xout_rgb = pipeline.createXLinkOut()
xout_rgb.setStreamName("rgb")

cam_rgb.video.link(xout_rgb.input)

with depthai.Device(pipeline) as device:
    q_rgb = device.getOutputQueue("rgb")
    # import py_whycon_code; help(py_whycon_code); exit()
    debug = True

    camera_calibration_path     = os.path.realpath(os.path.join(PROJECT_ROOT, 'config', 'camera_calibration.example.yml'))
    space_calibration_path_in   = os.path.realpath(os.path.join(PROJECT_ROOT, 'config', 'space_calibration.example.yml'))
    space_calibration_path_out  = os.path.realpath(os.path.join(PROJECT_ROOT, 'config', 'space_calibration.autocalibration_result.yml'))
    
    if args.set_cam_calib_path:
        camera_calibration_path     = os.path.realpath(args.set_cam_calib_path)
    if args.set_space_calib_path_in:
        space_calibration_path_in   = os.path.realpath(args.set_space_calib_path_in)
    if args.set_space_calib_path_out:
        space_calibration_path_out  = os.path.realpath(args.set_space_calib_path_out)

    # print('camera_calibration_path', camera_calibration_path)
    # print('space_calibration_path_in', space_calibration_path_in)

    window = ImgStorageWindow()

    
    detector = WhyCodeDetector(
        camera_calibration_path,    # path to existing camera calibration file
        space_calibration_path_in,  # path to existing space calibration file
        0.099,   # default black circle diameter [m];
        4,      # num of markers to track
        TransType.T_NONE,  # calibation transform type
        7,     # num of ID id_bits
        360,    # num of id_samples to identify ID
        2,      # hamming distance of ID code
        True,   # whether to identify ID
        True,   # whether to show coords
        True,   # whether to show segment
        False   # whether print debug info
    )

    stop    = False
    t_sum   = 0.0
    t_count = 0

    while not stop:
        detector_result = None
        in_rgb = q_rgb.tryGet()

        if in_rgb is not None:
            # If the packet from RGB camera is present, we're retrieving the frame in OpenCV format using getCvFrame
            img_array = in_rgb.getCvFrame()
            start_time = time()

            autocalib_results = detector.detect_and_calibrate(
                img_array, space_calibration_path_out, 1.0, 1.0, debug
            )
            stop_time = time()
            if autocalib_results:
                for i, marker in enumerate(autocalib_results.markers):
                    print(f'\t\tID {marker.segment_in_image.ID}')
                    print(f'{i}\t\tin image x:{marker.segment_in_image.x}, y:{marker.segment_in_image.y}')
                    print(f'\t\tin space x:{marker.coords.x}, y:{marker.coords.y}, z:{marker.coords.z}, d:{marker.coords.d}')
                stop = autocalib_results.saved
            window.swow(img_array)
            delta_time = stop_time - start_time
            t_sum += delta_time
            t_count += 1
        # print(f'delta time = {delta_time}')
        if not stop:
            stop = window.is_stopped()
    print(f'AVG(delta time) = {round(1000*delta_time, 1)} [ms]')


