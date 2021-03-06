import cv2
from typing import List

from model import GroundTruth, Rectangle
import numpy as np


class Data:
    """
    In this class we store in a list the content of a data element of our dataset:

    - Images
    - masks
    - Groundtruths

    In the case of Groundtruth we read the txt file to store the information:

    - Top left of groundtruth rectangle

    - Then with this point he find the width and height of the groundtruth

    - And we store the type of signals (A,B,C,D,E,F)

    Finally we read images and masks with the functions get_img and get_mask.

    """

    name: str
    gt: List[GroundTruth]
    img_path: str
    mask_path: str
    img: np.array
    mask_img: np.array

    def __init__(self, directory: str, name: str):
        self.name = name
        self.gt = []
        self.img_path = '{}/{}.jpg'.format(directory, name)
        self.mask_path = '{}/mask/mask.{}.png'.format(directory, name)
        self.img = None
        self.mask_img = None
        with open('{}/gt/gt.{}.txt'.format(directory, name)) as f:
            for line in f.readlines():
                parts = line.strip().split(' ')
                gt = GroundTruth(
                    sign_type=parts[4],
                    top_left=(int(float(parts[0])), int(float(parts[1]))),
                    width=int(float(parts[3]) - float(parts[1]) + 1),
                    height=int(float(parts[2]) - float(parts[0]) + 1)
                )
                self.gt.append(gt)

    def get_img(self):
        if self.img is None:
            self.img = cv2.imread(self.img_path, cv2.IMREAD_COLOR)
        return self.img

    def get_mask_img(self):
        if self.mask_img is None:
            self.mask_img = cv2.imread(self.mask_path, cv2.IMREAD_GRAYSCALE)
        return self.mask_img
