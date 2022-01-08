import sys

import cv2
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image

import pycubelut_modified as pcl


# Source: https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
def calibrate(img, threshold_val=100, debug=False):
    img = np.array(img)
    thresh = cv2.threshold(img, threshold_val, 255, cv2.THRESH_BINARY_INV)[1]

    # Notice: need to swap the order of two arrays returned from np.where
    # so that the x and y values will match those in plot/draw parameters
    coordinates = np.column_stack((np.where(thresh > 0)[1], np.where(thresh > 0)[0]))
    rect = cv2.minAreaRect(coordinates)

    if debug:
        print(rect, file=sys.stderr)

        cv2.drawContours(thresh, [np.int0(cv2.boxPoints(rect))], 0, 150, 10)
        bordered = img
        cv2.drawContours(bordered, [np.int0(cv2.boxPoints(rect))], 0, 150, 10)

        plt.imshow(thresh, cmap='gray')
        plt.show()
        plt.imshow(bordered, cmap='gray')
        plt.show()

    angle = rect[-1]
    if angle > 45:
        angle = angle - 90

    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_CONSTANT, borderValue=255)

    print("angle: {:.3f}".format(angle), file=sys.stderr)

    return Image.fromarray(rotated)

def threshold(img):
    lut = pcl.CubeLUT('threshold.cube')
    img = pcl.process_image(img, 0, lut, 0)
    img = img.convert('L')
    return img
