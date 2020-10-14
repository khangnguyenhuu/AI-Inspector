import cv2
import numpy as np

class Color_check:
    def __init__(self, img_path):
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        img = cv2.resize(img, (500,500))
        self.img = img

    def Color_check(self):
        # define green threshold
        lower_green = (38, 90, 30)
        upper_green = (70, 255,255)
        # If pixel in range of green threshold then this pixel = 1 and if not this pixel = 0
        mask_img = cv2.inRange (self.img, lower_green, upper_green)
        # convert img from HSV back to RGB
        self.img = cv2.cvtColor (self.img, cv2.COLOR_HSV2RGB)
        # bitwise the grayscale img and origin img to get mask of img
        result = cv2.bitwise_and(self.img, self.img, mask=mask_img)
        return result

    def visualize(self, mask_img):
        cv2.imshow('img', mask_img)
        cv2.waitKey(0)
    
    def Process(self):
        mask_img = self.Color_check()
        count_green_pixel = 0
        count_notgreen_pixel = 0
        for i in range (mask_img.shape[0]):
            for j in range (mask_img.shape[1]):
                if ((mask_img[i,j,0], mask_img[i,j,1], mask_img[i,j,2]) != (0,0,0)):
                    count_green_pixel += 1
        count_notgreen_pixel = 500*500 - count_green_pixel
        ratio = count_notgreen_pixel / count_green_pixel
        print (ratio)
        if (count_green_pixel < count_notgreen_pixel):
            cv2.putText(self.img, 'Chai khong dong nap', (500//4,500//4), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
        else:
            cv2.putText(self.img, 'Chai dong nap', (500//4,500//4), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)

        
        #self.visualize(self.img)
        self.visualize(mask_img)

color_check = Color_check('Capture3.PNG')
color_check.Process()