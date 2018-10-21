from typing import List, Dict
import numpy as np
from model import GroundTruth, Rectangle
from model import rectangle
from model import Data
import cv2
from matplotlib import pyplot as plt
from PIL.ImageOps import grayscale


class Template:
    signs: List[Rectangle]
    masks: List[np.array]

    def __init__(self):
        self.signs = []
        self.masks = []

    def add_sign(self, a: rectangle):
        self.signs.append(a)

    def get_sizes(self, data: List[Data]) -> (Dict[str, 'Template'], int):
        sign_type = {}
        total = 0
        for sample in data:
            for gt in sample.gt:
                if gt.type not in sign_type.keys():
                    sign_type[gt.type] = Template()

                sign_type[gt.type].signs.append(Rectangle(
                    top_left=gt.top_left,
                    width=gt.width,
                    height=gt.height))
            total += 1

        return sign_type, total

    def get_max_areas(self, data: List[Data]):
        sign_types, total = self.get_sizes(data)
        types = ['A', 'B', 'C', 'D', 'E', 'F']
        max = []
        max1 = 0
        for pos, i in enumerate(types):
            max.append(Template())
            for j in range(len(sign_types[i].signs)):
                if sign_types[i].signs[j].get_area() > max1:
                    max1 = sign_types[i].signs[j].get_area()

                max[pos].add_sign(sign_types[i].signs[j])

        return max

    def draw_mask_circle(self, width: int, height: int):
        radio=height
        if width>height:
            radio=width   
        image = np.zeros((int(radio) , int(radio) ), np.uint8)
        image[:] = 0 
        center = (int(radio / 2), int(radio / 2))
        cv2.circle(image, center, int(radio / 2), (255,), -1)
        return image
   
    def draw_mask_circle_dif(self, width: int, height: int):
        image = np.zeros((int(width) , int(width)), np.uint8)
        image[:] = 0
        center = (int(width / 2), int(width / 2))
        cv2.circle(image, center, int(width / 2), (255,), -1)
        image=cv2.resize(image, (width,height))
        return image
   
    def draw_mask_triangle(self, width: int, height: int):
        image = np.zeros((int(width) , int(height) ), np.uint8)
        image[:] = 0

        point1 = (0, int(width / 2) + 0)
        point2 = ((height +0), 0)
        point3 = ((height + 0), 0 + width)

        cv2.circle(image, point1, 2, (255), -1)
        cv2.circle(image, point2, 2, (255), -1)
        cv2.circle(image, point3, 2, (255), -1)

        triangle = np.array([point1, point3, point2])

        cv2.drawContours(image, [triangle], 0, (255,), -1)

        return image

    def draw_mask_triangle_inv(self, width: int, height: int):
        image = np.zeros((int(width) , int(height)  ), np.uint8)
        image[:] = 0

        point1 = (0,0)
        point2 = (0, width)
        point3 = (height , int(width / 2) )

        cv2.circle(image, point1, 2, (255), -1)
        cv2.circle(image, point2, 2, (255), -1)
        cv2.circle(image, point3, 2, (255), -1)

        triangle = np.array([point1, point3, point2])

        cv2.drawContours(image, [triangle], 0, (255,), -1)

        return image

    def draw_rectangles(self, width: int, height: int):
        image = np.zeros((int(width) , int(height) ), np.uint8)
        image[:] = 0
        top_rigth = (0, 0)
        bottom_right = (int(width),  int(height))
        cv2.rectangle(image, (top_rigth), (bottom_right), (255,), -1)
        return image

    def draw_by_type(self, type: str, width: int, height: int):
        switcher = {
            'A': self.draw_mask_triangle,
            'B': self.draw_mask_triangle_inv,
            'C': self.draw_mask_circle,
            'D': self.draw_mask_circle_dif,
            'E': self.draw_mask_circle_dif,
            'F': self.draw_rectangles
        }

        func = switcher.get(type, lambda: "Invalid Type")

        # Execute the function
        image = func(width, height)

        return image

    def train_masks(self, data: List[Data]):
        maxes = self.get_max_areas(data)
        types = ['A', 'B', 'C', 'D', 'E', 'F']

        for pos, i in enumerate(types):
            average_width = 0
            average_height = 0
            for j in range(len(maxes)):
                average_width = average_width + maxes[pos].signs[j].width
                average_height = average_height + maxes[pos].signs[j].height
            self.masks.append(self.draw_by_type(i, int(average_width / len(maxes)),
                                                int(average_height / len(maxes))))

    def template_matching_global(self, img: np.array) -> (np.array, int):
        types = ['A', 'B', 'C', 'D', 'E', 'F']
        final = 0
        final2= 0
        signal_type = 0
        position = (0, 0)
        for pos, i in enumerate(types):
            print(types[pos])
            plt.imshow(self.masks[pos],cmap="gray")
            res = cv2.matchTemplate(img, self.masks[pos], cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
           
            if max_val > final:
                final = max_val
                
                position = max_loc
                signal_type = i

        return position, signal_type
    def template_matching_reg(self, img: np.array, regions: List[Rectangle]) -> (np.array, int):
        types = ['A', 'B', 'C', 'D', 'E', 'F']
        imag=[]
        signal_type = []
        position = List[np.array]
        
        for region in regions:
            imag=img[region.top_left[0]:region.top_left[0]+ region.height, region.top_left[1]:region.top_left[1]+region.width]
            for pos, i in enumerate(types):
                resized_mask= cv2.resize(self.masks[pos], (region.width,region.height))
                res = cv2.matchTemplate(imag, resized_mask, cv2.TM_CCOEFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                print(max_val)
                if max_val > 0.4:
                    position.append(max_loc)
                    signal_type.append(i)

        return position, signal_type

instance = Template()
