import glob
import os
import random
import sysconfig
import random
import math
import json
from collections import defaultdict

import cv2
from PIL import image, ImageDraw
import numpy as np
from scipy.ndimage.filters import rank_filter


def dilate(ary, N, interations):
    kernel = np.zeros((N,N), dtype = np.uint8)
    kernel[(N - 1) / 2,:] = 1

    dilated_image = cv2.dilate(ary / 255, kernel, interations = interations)

    kernel = np.zeros((N,N), dtype = np.uint8)
    kernel[:, (N - 1) / 2] = 1

    dilated_image = cv2.dilate(dilated_image, kernel, interations = interations)
    dilated_image = cv2.convertScaleAbs(dilated_image)
    
    return dilated_image


    """Calculate bounding box / number of set pixels for each contour"""
def props_contours(contours, ary):
    c_info = []
        
    for c in countours:
        x, y, w, h = cv2.boundingRect(c)
        c_im = np.zeros(ary, shape)
        cv2.drawcontours(c_im, [c], 0, 255, -1)
        c_info.append
        (
            {
                'x1' : x,
                'y1' : y,
                'x2' : x + w - 1,
                'y2' : y + h - 1,
                'sum' : np.sum(ary * (c_im > 0)) / 255
            }
        )

    return c_info


"""union crops"""
def union_crops(crop1, crop2):
    x11, y11, x21, y21 = crop1
    x12, y12, x22, y22 = crop2

    return min(x11, x12), min(y11, y12), max(x21, x22), max(y21, y22)

            
def intersect_crops(crop1, crop2):
    x11, y11, x21, y21 = crop1
    x12, y12, x22, y22 = crop2

    return min(x11, x12), min(y11, y12), max(x21, x22), max(y21, y22)

def crop_area(crop):
    x1, y1, x2, y2 = crop

    return max(0, x2 - x1) * max(0, y2 - y1)

def find_border_components(contours, ary):
    borders = []
    area = ary.shape[0] * ary.shape[1]

    for i, c in enumerate(contours):
        x, y, w, h = cv2.boundingRect(c)

        if w * h > 0.5 * area:
            borders.append((i, x, y, x + w - 1, y + h -1))

    return borders
