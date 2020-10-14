import cv2
from Detector.yolo_detect import *
from Process.color_check import *

if __name__ == "__main__":
    Yolo = Yolo_detector("./Detector/cfg/obj.names", "./Detector/cfg/yolov3_Box.cfg", "./Detector/model_weigths/yolov3_Box_last.weights")
    ori_img = cv2.imread('Data\data_21.jpeg')
    img = cv2.resize(ori_img, (int (ori_img.shape[1]*0.4), int(ori_img.shape[0]*0.4)))
    boxes, class_ids = Yolo.detect_image(img)
    if (6 in class_ids):
        cv2.putText(img, 'Not accept', (60, 30), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (255,0,0), thickness = 2)
    else:
        for i in range (len(boxes)):
            if (class_ids == [0,1]):
                if (class_ids == [0,1]):
                    process_img = img[boxes[i][1]:boxes[i][1]+boxes[i][3], boxes[i][0] + boxes[i][2]]
                    color_check = Color_check(process_img)
                    color_check.Process()
            elif (class_ids == [2,3]):
                if (class_ids[i] == 3):
                    process_img = img[boxes[i][1]:boxes[i][1]+boxes[i][3], boxes[i][0]: boxes[i][0] + boxes[i][2]]
                    color_check = Color_check(process_img)
                    check = color_check.Process()
                    if (check == 0):
                        cv2.putText(img, 'Not accept', (img.shape[0]//2, img.shape[1]//4), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
                    else:
                        cv2.putText(img, 'accept', (img.shape[0]//2, img.shape[1]//4), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
            elif (class_ids == [4,5]):
                if (class_ids[i] == 5):
                    process_img = img[boxes[i][1]:boxes[i][1]+boxes[i][3], boxes[i][0] + boxes[i][2]]
                    color_check = Color_check(process_img)
                    color_check.Process()
                    if (check == 0):
                        cv2.putText(img, 'Not accept', (img.shape[0]//2, img.shape[1]//4), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
                    else:
                        cv2.putText(img, 'Chai dong nap', (img.shape[0]//2, img.shape[1]//4), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
            else:
                cv2.putText(img, 'Not accept', (img.shape[0]//2, img.shape[1]//4), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
        cv2.imshow('img', img)
        cv2.waitKey()
    