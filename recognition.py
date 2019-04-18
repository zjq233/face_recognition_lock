import cv2,math,datetime
import numpy as np
import os
from PIL import Image
from Image_preprocessing import Distance,CropFace, takeSecond,yuchuli

faceCascade=cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#eyeCascade= cv2.CascadeClassifier('haarcascade_eye_tree_eyeglasses.xml')
recognizer=cv2.face.EigenFaceRecognizer_create()
recognizer.read('trainer.yml')

def recognition():
    names = ['unknowns', 'Marcelo', 'LDK', 'QL', 'ZCL','ZJM','LZY']
    font = cv2.FONT_HERSHEY_SIMPLEX
    a=0
    #flag1=1
    id = 0
    cam = cv2.VideoCapture(0)
    cam.set(3, 640)
    cam.set(4, 480)
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)
    count=0
    dict={names[0]:0,names[1]:0,names[2]:0,names[3]:0,names[4]:0,names[5]:0,names[6]:0}
    stat_time=datetime.datetime.now()
    while (True):
        end_time=datetime.datetime.now()
        ret, img = cam.read()
        img = cv2.flip(img, -1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(int(minW), int(minH)), )
        for (x, y, w, h) in faces:
            if len(faces) == 1:
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                face_numpy = cv2.resize(img[y:y + h, x:x + w],(250,250))
                flag,image=yuchuli(face_numpy)
                if flag :
                    count+=1
                    id,confidence=recognizer.predict(image)
                    if (confidence<4000):
                        id = names[id]
                        dict[id] = dict[id] + 1
                    else:
                         id='unknowns'
                         dict[Unknow]= dict[Unknow]+1
        if count>30 or (end_time-star_time).seconds>60:
            cam.release()
            dist = sorted(dict.items(), key=lambda item: item[1], reverse=True)
            #flag1 = 0
            break
    for i in range(7):
        a = a + dist[i][1]

    return dist[0][0], dist[0][1]/a



