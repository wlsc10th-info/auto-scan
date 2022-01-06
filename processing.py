import sys

import cv2
import numpy as np
from PIL import Image

# Source: https://www.pyimagesearch.com/2017/02/20/text-skew-correction-opencv-python/
def calibrate(img):
    img = np.array(img)
    inverted = cv2.bitwise_not(img)
    thresh = cv2.threshold(inverted, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    # cv2.imshow('thresh', thresh)
    # cv2.waitKey()

    coordinates = np.column_stack(np.where(thresh > 0))
    angle = cv2.minAreaRect(coordinates)[-1]

    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle

    (h, w) = img.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(img, M, (w, h),
                             flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)

    print(cv2.minAreaRect(coordinates), file=sys.stderr)
    print("angle: {:.3f}".format(angle), file=sys.stderr)

    return Image.fromarray(img)

def threshold(img):
    raise NotImplementedError
