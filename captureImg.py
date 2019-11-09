import cv2
import time 

webcam = cv2.VideoCapture(0)

while True:
	check, frame = webcam.read()
	cv2.imshow("Capturing", frame)
	time.sleep(5)
	cv2.imwrite(filename='saved_img.jpg', img=frame)