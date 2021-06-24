import cv2
import mediapipe as mp

cap = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands = 1)
mp_draw = mp.solutions.drawing_utils

while True:
    success,img = cap.read()
    h,w,c = img.shape
    img_rgb = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    res = hands.process(img_rgb)
    if res.multi_hand_landmarks:
        for my_hand in res.multi_hand_landmarks:
            for id, landmark in enumerate(my_hand.landmark):
                if id%4 == 0:
                    cx,cy = int(landmark.x*w),int(landmark.y*h)
                    cv2.circle(img,(cx,cy),10,(0,0,255),cv2.FILLED)
    cv2.imshow('Image',img)
    cv2.waitKey(1)