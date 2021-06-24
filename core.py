import cv2
import mediapipe as mp


class HandTracker:
    '''
    Analyzes an image, returns fingertip positions
    '''
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(max_num_hands = 1)
        #self.mp_draw = mp.solutions.drawing_utils

    def track(self,img):
        base_points = []
        h,w,c = img.shape
        rgb_img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        res = self.hands.process(rgb_img)
        if res.multi_hand_landmarks:
            for my_hand in res.multi_hand_landmarks:
                for id,landmark in enumerate(my_hand.landmark):
                    cx,cy = int(landmark.x*w),int(landmark.y*h)
                    base_points.append([cx,cy])      
        return base_points

    def get_gesture(self,img):
        gesture_desc = []
        base_points = self.track(img)
        if len(base_points):
            #thumb case
            dist = ((base_points[4][0]-base_points[17][0])**2+
                    (base_points[4][1]-base_points[17][1])**2)**0.5
            base_dist = ((base_points[2][0]-base_points[17][0])**2+
                        (base_points[2][1]-base_points[17][1])**2)**0.5
            if dist >= base_dist:
                gesture_desc.append(1)
            else:
                gesture_desc.append(0)
            #all other fingers
            for i in range(8,24,4):
                dist = ((base_points[i][0]-base_points[0][0])**2+
                        (base_points[i][1]-base_points[0][1])**2)**0.5
                base_dist = ((base_points[i-2][0]-base_points[0][0])**2+
                            (base_points[i-2][1]-base_points[0][1])**2)**0.5
                if dist >= base_dist:
                    gesture_desc.append(1)
                else:
                    gesture_desc.append(0)
        return gesture_desc

    def get_distance(self,img,p1,p2):
        base_points = self.track(img)
        if p1<0 or p1>20 or p2<0 or p2>20 or len(base_points)==0:
            return None
        dist = ((base_points[p1][0]-base_points[p2][0])**2+
                (base_points[p1][1]-base_points[p2][1])**2)**0.5
        return dist                                                            

    def visualize(self,img):
        base_points = self.track(img)
        for point in base_points:
                cv2.circle(img,(point[0],point[1]),10,(0,0,255),cv2.FILLED)
        return img        


if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    tracker  = HandTracker()
    while True:
        success,img = cap.read()
        img = tracker.visualize(img)
        cv2.imshow('Image',img)
        """ gesture = tracker.get_gesture(img)
        if len(gesture):
            print(gesture) """
        """ dist = tracker.get_distance(img,8,12)
        if dist is not None:
            print(dist) """
        cv2.waitKey(1)
   