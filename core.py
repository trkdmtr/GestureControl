import cv2
import mediapipe as mp


class Cam:
    def __init__(self, device_id, img_width, img_height):
        self.cap = cv2.VideoCapture(device_id)
        self.cap.set(3,img_width)
        self.cap.set(4,img_height)

    def __call__(self):
        _,img = self.cap.read()
        return img 


class Gesture:
    def __init__(self,id,coords):
        self.id = id
        self.coords = coords.copy()

    def get_distance(self,p1,p2):
        dist = ((self.coords[p1][0]-self.coords[p2][0])**2+
                (self.coords[p1][1]-self.coords[p2][1])**2)**0.5
        return dist


class HandTracker:
    '''
    Analyzes an image, returns fingertip positions
    '''
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(max_num_hands = 1)

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

    def get_gesture(self,base_points):
        gesture_desc = []
        gesture_id = -1
        fingertips = []
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
            gesture_id = 0
            for i,finger in enumerate(gesture_desc):
                if finger == 1:
                    gesture_id += 2**i
            for i in range(4,24,4):
                fingertips.append(base_points[i])
        return Gesture(gesture_id,fingertips)                                                          

    def visualize(self,img,base_points):
        for point in base_points:
                cv2.circle(img,(point[0],point[1]),10,(0,0,255),cv2.FILLED)
        return img        

   