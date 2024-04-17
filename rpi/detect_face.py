import cv2
import numpy as np
import os
from picamera2 import Picamera2
import serial

ESC_KEY_ID  = 27
MIN_W       = 100
MIN_H       = 100
SHOW_SCREEN = False

ser = serial.Serial("/dev/ttyGS0", 115200, timeout=0.1)

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

try:
    while True:
        img = picam2.capture_array()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        faces = detector.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(MIN_W, MIN_H)
        )
        
        name = "Unknown"
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            
            # If confidence is less than 40 (lower confidence is better)
            if (confidence < 40):
                name = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            
        if (SHOW_SCREEN):
            cv2.putText(
                        img,
                        str(name),
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
            cv2.imshow('Camera',img)
        
        # print("Prediction: " + str(id))
        # with open("log.txt", "w") as f:
        #     f.write(str(name))    
        
        # k = cv2.waitKey(30) & 0xff # Press 'ESC' for exiting video
        # if k == ESC_KEY_ID:
        #     break
        
        # Check serial port for messages
        if ser.is_open:
            data = ser.readline()
            if data != b'':
                # print(data)
                # print("Received a message!")
                string = name + "\n"
                ser.write(string.encode())
except:
    # Do a bit of cleanup
    print("\n[INFO] Exiting Program")
