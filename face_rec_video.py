from imutils.video import VideoStream
from imutils.video import FPS
import face_recognition
import argparse
import imutils
import pickle
import time
import cv2
import pyttsx3
import random
from gtts import gTTS
from playsound import playsound
    
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--cascade", required=False,
	help = "path to where the face cascade resides")
ap.add_argument("-e", "--encodings", required=False,
	help="path to serialized db of facial encodings")

args = vars(ap.parse_args())
args["cascade"] = "haarcascade_frontalface_default.xml"
args["encodings"] = "encodings.pickle"
print("[INFO] loading encodings + face detector...")
data = pickle.loads(open(args["encodings"], "rb").read())
detector = cv2.CascadeClassifier(args["cascade"])

print(data)


print("[INFO] Memulai Stream dari Pi Camera...")
vs = VideoStream(src=0).start()
time.sleep(2.0)

fps = FPS().start()
name1="unknown"

while True:

	frame = vs.read()
	frame = imutils.resize(frame, width=500)
	

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)


	rects = detector.detectMultiScale(gray, scaleFactor=1.1, 
		minNeighbors=5, minSize=(30, 30),
		flags=cv2.CASCADE_SCALE_IMAGE)


	boxes = [(y, x + w, y + h, x) for (x, y, w, h) in rects]

	encodings = face_recognition.face_encodings(rgb, boxes)
	names = []
	name = "Unknown"

	for encoding in encodings:
		matches = face_recognition.compare_faces(data["encodings"],
			encoding,tolerance=0.5)
		
		

		if True in matches:
			matchedIdxs = [i for (i, b) in enumerate(matches) if b]
			counts = {}
			for i in matchedIdxs:
				name = data["names"][i]
				
				if(name!=name1 and name!="unknown"):
				   wish=["hey hii","hey you look beautiful today","hey whats up","good to see you again","hey how are you","how can I help you","How can I assist you"]
				   message=random.choice(wish)
				   v=gTTS(text=message+name,lang="en",slow=False)
				   v.save("name.mp3")
				   playsound("name.mp3")			   				   
				   name1=name			  
							
				counts[name] = counts.get(name, 0) + 1
			name = max(counts, key=counts.get)
		names.append(name)


	for ((top, right, bottom, left), name) in zip(boxes, names):

		cv2.rectangle(frame, (left, top), (right, bottom),
			(0, 255, 0), 2)
		y = top - 15 if top - 15 > 15 else top + 15
		cv2.putText(frame, name, (left, y), cv2.FONT_HERSHEY_SIMPLEX,
			0.75, (0, 255, 0), 2)


	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF


	if key == ord("q"):
		break


	fps.update()


fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))


cv2.destroyAllWindows()
vs.stop()
