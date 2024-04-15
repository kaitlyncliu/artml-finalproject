#!/usr/bin/python3

import cv2
from picamera2 import Picamera2

NUM_SAMPLES = 50
ESC_KEY_ID  = 27
MIN_W       = 20
MIN_H       = 20

detector = cv2.CascadeClassifier("/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml")
cv2.startWindowThread()

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1080, 1080)}))
picam2.start()

# For each person, enter one numeric face id
face_id = input('\n Enter user id end press <return> ==>  ')

print("\n [INFO] Initializing face capture. Look the camera and wait ...")

# Initialize individual sampling face count
count = 0
while(True):
    img = picam2.capture_array()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    faces = detector.detectMultiScale(
        gray,     
        scaleFactor=1.2,
        minNeighbors=5,     
        minSize=(MIN_W, MIN_H)
    )
    
    for (x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
        count += 1
        print("\n [INFO] Captured sample " + str(count))
        # Save the captured image into the datasets folder
        cv2.imwrite("dataset/User." + str(face_id) + '.' +  
                    str(count) + ".jpg", gray[y:y+h,x:x+w])
        cv2.imshow('image', img)

    k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
    if k == ESC_KEY_ID:
        break
    elif count >= NUM_SAMPLES: # Take 50 face sample and stop video
         break

# Do a bit of cleanup
print("\n [INFO] Exiting data collection program")
