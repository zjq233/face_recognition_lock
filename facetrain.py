import cv2
import os
import numpy as np
from PIL import Image

path = 'dataset3'
recognizer = cv2.face.EigenFaceRecognizer_create()
def getImagesAndLabels(path):

    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    faceSamples=[]
    ids=[]
    for imagePath in imagePaths:
        PIL_img=Image.open(imagePath).convert('L')
        img_numpy = np.array(PIL_img,'uint8')
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        faceSamples.append(img_numpy)
        ids.append(id)
    return faceSamples,ids

print("\n [INFO] Training faces. It will take a few seconds,Wait ...")
faces, ids = getImagesAndLabels(path)
recognizer.train(faces,np.array(ids))
recognizer.write('trainer.yml')

print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))