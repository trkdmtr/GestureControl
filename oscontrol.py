import cv2
import pyautogui
import core
import time  


class Controller:
    def __init__(self, smoothen=5):
        self.x0,self.y0 = -1,-1
        self.smoothen = smoothen

    def process_gesture(self,gesture: core.Gesture):
        if gesture.id == -1:
            pass
        elif gesture.id == 0:
            self.x0,self.y0 = -1,-1
        elif gesture.id == 2:
            x,y = gesture.coords[1]
            if self.x0 == -1:
                self.x0,self.y0 = x,y
            else:
                dx,dy = (self.x0-x)//self.smoothen, (y-self.y0)//self.smoothen
                pyautogui.move(dx,dy)
                self.x0 -= dx
                self.y0 += dy
        elif gesture.id == 3:
            if gesture.get_distance(0,1) <= 40:
                pyautogui.click(button='right')
                print('RMB')
        elif gesture.id == 6:
            if gesture.get_distance(1,2) <= 40:
                pyautogui.click(button='left')
                print('LMB')    
        else:
            pass


if __name__ == '__main__':
    cam = core.Cam(0,1280,720)
    tracker = core.HandTracker()
    magic_mouse = Controller()
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



