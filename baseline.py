import cv2
from Detector.yolo_detect import *
from Process.color_check import *
from datetime import date, datetime
import time

def get_day_time():
    today = date.today()
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    return today, current_time

if __name__ == "__main__":
    Yolo = Yolo_detector("./Detector/cfg/obj.names", "./Detector/cfg/yolov3_Box.cfg", "./Detector/model_weigths/yolov3_BB_last.weights")
    ori_img = cv2.imread('Data\SNB-6004_20201015113600.jpeg')
    img = cv2.resize(ori_img, (int (ori_img.shape[1]*0.4), int(ori_img.shape[0]*0.4)))
    
    #detect step
    cuda.select_device(0)
    boxes, class_ids = Yolo.detect_image(img)
    cuda.close()

    Not_good = 0
    Blank = np.ones((img.shape[0],400,3), np.uint8)*255
    Blank_to_save = Blank.copy()
    img_to_save = img.copy()
    print(class_ids)
    if (6 in class_ids):
        Not_good = 1
        cv2.putText(Blank, 'Status: Not good', (Blank.shape[0]//8, Blank.shape[1]//8), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
                        
        day, time = get_day_time()
    else:
        for i in range (len(boxes)):
            if (2 in class_ids and 3 in class_ids):
                if (class_ids[i] == 3):
                    process_img = img[boxes[i][1]:boxes[i][1]+boxes[i][3], boxes[i][0]: boxes[i][0] + boxes[i][2]]
                    color_check = Color_check(process_img)
                    check = color_check.Process()
                    if (check == 0):
                        Not_good = 1
                        cv2.putText(Blank, 'Status: Not good', (Blank.shape[0]//8, Blank.shape[1]//8), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
                        day, time = get_day_time()
                    else:
                        cv2.putText(Blank, 'Status: OK', (Blank.shape[0]//8, Blank.shape[1]//8), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
            else:
                Not_good = 1
                cv2.putText(Blank, 'Status: Not good', (Blank.shape[0]//8, Blank.shape[1]//8), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
                day, time = get_day_time()   

    # write log
    if not os.path.exists ("logs"):
        os.makedirs('logs')
    # write 
    # write time not good
    h = open('logs/NG_times.txt', 'r+', encoding = 'utf-8')
    a = h.read()
    a = a.split('\n')
    try:
        a.remove('')
    except:
        pass
    NG_times = int (a[len(a) - 1])
    if (Not_good == 1):
        NG_times += 1
        h.write('{} {}'.format(str(NG_times), '\n'))
        h.close()
    cv2.putText(Blank, 'Not good times: ' + str(NG_times), (Blank.shape[0]//8, Blank.shape[1]//2), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)


    # write time OK
    g = open('logs/Ok_times.txt', 'r+', encoding = 'utf-8')
    a = g.read()
    a = a.split('\n')
    try:
        a.remove('')
    except:
        pass
    Ok_times = int (a[len(a) - 1])
    if (Not_good == 0):
        Ok_times += 1
        g.write('{} {}'.format(str(Ok_times), '\n'))
        g.close()
    cv2.putText(Blank, 'Good times: ' + str(Ok_times), (Blank.shape[0]//8, Blank.shape[1]//3), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)

    # write time iterations
    f = open('logs/test_times.txt', 'r+', encoding = 'utf-8')
    a = f.read()
    a = a.split('\n')
    try:
        a.remove('')
    except:
        pass
    times = int (a[len(a) - 1])
    times += 1
    cv2.putText(Blank, 'Times: ' + str(times), (Blank.shape[0]//8, Blank.shape[1]//4), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
    f.write('{} {}'.format(str(times), '\n'))
    f.close()

    # write image if they art Not good image
    if not os.path.exists ("Notgood_information"):
        os.makedirs('Notgood_information')
    if (Not_good == 1):
        cv2.putText(Blank_to_save, 'Date: ' + str(day), (Blank.shape[0]//8, Blank.shape[1]//4), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
        cv2.putText(Blank_to_save, 'Time: ' + str(time), (Blank.shape[0]//8, Blank.shape[1]//3), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
        cv2.putText(Blank_to_save, 'Times: ' + str(times), (Blank.shape[0]//8, Blank.shape[1]//2), cv2.FONT_HERSHEY_SIMPLEX, fontScale = 1, color = (0,0,0), thickness = 2)
        img_to_save = cv2.hconcat([img, Blank_to_save])
        cv2.imwrite('Notgood_information/Notgood' + str(times) + '.png', img_to_save)
    img = cv2.hconcat([img, Blank])
    cv2.imshow('img', img)
    cv2.waitKey()
