from imutils import paths
import face_recognition
import argparse
import pickle
import cv2
import time
import os


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--datasets", required=False,
	help="path to input directory of faces + images")
ap.add_argument("-e", "--encodings", required=False,
	help="path to serialized db of facial encodings")
ap.add_argument("-d", "--detection-method", type=str, default="hog",
	help="face detection model to use: either `hog` or `cnn`")
args = vars(ap.parse_args())


args["encodings"] = "encodings.pickle"
data = {"encodings":[],"names":[]}
haar_file = 'haarcascade_frontalface_default.xml'
(width, height) = (130, 100)
(x,y) = (10,10)

try:
	data = pickle.loads(open(args["encodings"], "rb").read())
except:
	print("file created")


knownEncodings = []
knownNames = []

name = input("Enter your name to be recognised as\n")


face_cascade = cv2.CascadeClassifier(haar_file) 
webcam = cv2.VideoCapture(0)  
  

count = 1
while True:  
    (_, im) = webcam.read()
    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY) 
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces: 
        cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2) 
        face = gray[y:y + h, x:x + w] 
        image = cv2.resize(face, (width, height))
        rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		
        boxes = face_recognition.face_locations(rgb,
			model=args["detection_method"])

		
        if count % 10 == 0:
            encodings = face_recognition.face_encodings(rgb, boxes)
	        
            for encoding in encodings:
                knownEncodings.append(encoding)
                knownNames.append(name)
        count += 1    
    cv2.putText(im, str(count)+"%",(x-10, y-10), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 0)) 
    cv2.imshow('OpenCV', im)
    time.sleep(0.001)
    key = cv2.waitKey(10) 
    if key == 27 or count == 100: 
        break
    

print("[INFO] Memproses serialize encoding...")
data = {"encodings": data["encodings"]+knownEncodings, "names": data["names"]+knownNames}
f = open(args["encodings"], "wb")
f.write(pickle.dumps(data))
f.close()
