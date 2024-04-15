import cv2
import numpy as np
import os
from picamera2 import Picamera2

ESC_KEY_ID  = 27
MIN_W       = 20
MIN_H       = 20

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')

detector_path = "/usr/share/opencv4/haarcascades/haarcascade_frontalface_default.xml"
detector = cv2.CascadeClassifier(detector_path);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Nora: id=1,  etc.
names = ['None', 'Nora', 'Aden', 'Kaitlyn', 'Kaylin', 'Caleb']

# Initialize and start realtime video capture
picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (1080, 1080)}))
picam2.start()

while True:
    img = picam2.capture_array()
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    faces = detector.detectMultiScale(
        gray,     
        scaleFactor=1.2,
        minNeighbors=5,    
        minSize=(MIN_W, MIN_H)
    )
    
    for(x,y,w,h) in faces:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
        
        # If confidence is less than 100 ==> "0" : perfect match 
        if (confidence < 100):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(
                    img, 
                    str(id), 
                    (x+5,y-5), 
                    font, 
                    1, 
                    (255,255,255), 
                    2
                   )
        cv2.putText(
                    img, 
                    str(confidence), 
                    (x+5,y+h-5), 
                    font, 
                    1, 
                    (255,255,0), 
                    1
                   )
    
    print("Prediction: " + str(id))
    #cv2.imshow('Camera',img) 
    
    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == ESC_KEY_ID:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program")
