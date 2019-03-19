# Author: Caroline Pacheco do E. Silva
# Date: 15/03/2018
# E-mail: lolyne.pacheco@gmail.com

from led_emotions import *
import curses
from neopixel import *
import _rpi_ws281x as ws
import time
import curses
import os
import math
import cv2
import numpy as np
import sys
import imutils
import time
from keras.models import load_model

# load our serialized model from disk
print("Loading face model...")
net = cv2.dnn.readNetFromCaffe('caffe_model/deploy.prototxt.txt', 'caffe_model/res10_300x300_ssd_iter_140000.caffemodel')

# load our face expression model
print("Loading face expression model...")
model = load_model('keras_model/model_5-49-0.62.hdf5')

# initialize the video stream and allow the cammera sensor to warmup
print("Starting video stream...")

video_capture = cv2.VideoCapture(0)
time.sleep(2.0)

target = ['angry','disgust','fear','happy','sad','surprise','neutral']
font = cv2.FONT_HERSHEY_SIMPLEX

# creation of an element allowing to "manipulate" the leds screen
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, CHANNEL, STRIP_TYPE)
     
# initializing the screen
strip.begin()

# initializing the black leds
leds = [Color(0, 0, 0)] * 64
              
try:
	# loop over the frames from the video stream
	while True:
         # capture frame-by-frame
		ret, frame = video_capture.read()        
		frame = imutils.resize(frame, width=400)
 
		# grab the frame dimensions and convert it to a blob
		(h, w) = frame.shape[:2]
		blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0,
			(300, 300), (104.0, 177.0, 123.0))
 
		# pass the blob through the network and obtain the detections and predictions
		net.setInput(blob)
		detections = net.forward()

		# loop over the detections
		for i in range(0, detections.shape[2]):
			# extract the confidence (i.e., probability) associated with the prediction
			confidence = detections[0, 0, i, 2]

			# filter out weak detections by ensuring the `confidence` is greater than the minimum confidence
			if confidence < 0.5:
				continue

			# compute the (x, y)-coordinates of the bounding box for the object
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
 
			# draw the bounding box of the face along with the associated  probability
			y = startY - 10 if startY - 10 > 10 else startY + 10
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				(0, 0, 255), 2)
			face_crop = frame[startY:endY,startX:endX]
			face_crop = cv2.resize(face_crop,(48,48))
			face_crop = cv2.cvtColor(face_crop, cv2.COLOR_BGR2GRAY)
			face_crop = face_crop.astype('float32')/255
			face_crop = np.asarray(face_crop)
			face_crop = face_crop.reshape(1, 1,face_crop.shape[0],face_crop.shape[1])
			result = target[np.argmax(model.predict(face_crop))]	    
                        # play LED emotions
                        #led_emotions(strip, leds, result)
                        led_emotions(result)
			cv2.putText(frame,result,(startX,startY), font, 1, (200,0,0), 3, cv2.LINE_AA)

		# show the output frame
		cv2.imshow("Frame", frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
              
except ValueError:
	print("[ERROR] An error has occurred.  Try again..")

# when everything is done, release the capture
video_capture.release()
cv2.destroyAllWindows()