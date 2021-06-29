import cv2
import pyautogui
import core
import time  


class Controller:
    def __init__(self, img_width, img_height):
        self.screen_width,self.screen_height = pyautogui.size()
        self.width_transform,self.height_transform = self.screen_width/img_width,self.screen_height/img_height

    def process_gesture(self,gesture: core.Gesture):
        if gesture.id == -1:
            pass
        elif gesture.id == 2:
            x,y = gesture.coords[1]
            x,y = (self.screen_width - x*self.width_transform,
                    y*self.height_transform)
            pyautogui.moveTo(x,y)
        elif gesture.id == 6:
            if gesture.get_distance(1,2) <= 50:
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
    gesture = tracker.get_gesture(points)
    magic_mouse.process_gesture(gesture)
    c_time = time.time()
    fps = 1/(c_time-p_time)
    p_time = c_time
    cv2.putText(img,str(int(fps)),(20,50),cv2.FONT_HERSHEY_PLAIN,3,(0,0,255))
    cv2.imshow('Image',img)
    cv2.waitKey(1)



