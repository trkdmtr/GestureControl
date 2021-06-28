import cv2
import pyautogui
import core
import time  


class Controller:
    def __init__(self, img_width, img_height):
        screen_width,screen_height = pyautogui.size()
        self.width_transform,self.height_transform = screen_width/img_width,screen_height/img_height

    def process_gesture(self,gesture,base_points,distance):
        if gesture == 2:
            x,y = base_points[8]
            x,y = x*self.width_transform,y*self.height_transform
            pyautogui.moveTo(x,y)
        elif gesture == 6:
            if distance <= 50:
                pyautogui.click()    
        else:
            pass





cam = core.Cam(0,1280,720)
tracker = core.HandTracker()
magic_mouse = Controller(1280,720)
p_time = 0
while True:
    img = cam()
    points = tracker.track(img)
    gesture_id = tracker.get_gesture(points)
    distance = tracker.get_distance(points,8,12)
    magic_mouse.process_gesture(gesture_id,points,distance)
    c_time = time.time()
    fps = 1/(c_time-p_time)
    p_time = c_time
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255))
    cv2.imshow('Image',img)
    cv2.waitKey(1)



