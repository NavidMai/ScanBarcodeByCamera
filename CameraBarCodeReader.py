# -*- coding: utf-8 -*-
import os
import cv2
import csv
import time
import zxing
import threading

#Camera RTSP
URL = "rtsp://172.16.22.100:554/live01/ss-Tunnel/media?stream=5&channel=1"

# Receive camera streaming images
class ipcamCapture:
    def __init__(self, URL):
        self.Frame = []
        self.status = False
        self.isstop = False

        # Connect to the camera
        self.capture = cv2.VideoCapture(URL)

    def start(self):
        print('ipcam started!')
        threading.Thread(target=self.queryframe, daemon=True, args=()).start()

    def stop(self):
        self.isstop = True
        print('ipcam stopped!')

    def getframe(self):
        return self.Frame

    def queryframe(self):
        while (not self.isstop):
            self.status, self.Frame = self.capture.read()

        self.capture.release()

# Connect to the camera
ipcam = ipcamCapture(URL)
ipcam.start()
time.sleep(1)

# Check the file path of the image of Tag which has a barcode or QR code appear.
filepath = "Barcode_Tag"
if os.path.isdir(filepath):
    print("The file path exists!")
else:
    print("The file path does not exist!")
    print("Create a new file path......")
    os.mkdir(filepath)

# Use a loop to capture images until the user click the Esc key
print(" ")
print("Start analysis:")
print("========================================================================")
image_tmp = "output.png"

while True:
    # Get the latest image
    I = ipcam.getframe()
    cv2.imshow('Camera Viewer', I) # Show the image
    cv2.imwrite(image_tmp, I)
    reader = zxing.BarCodeReader()
    barcode = reader.decode(image_tmp)

    if barcode != None:
        print(barcode.parsed)
        nowTime = time.strftime("%Y%m%d%H%M%S")
        image_of_tag = filepath + "/Tag_" + nowTime + ".png"
        print("Image Saved: " + image_of_tag)
        cv2.imwrite(image_of_tag, I)
    else:
        print("No QR code or Barcode")

    if cv2.waitKey(1000) == 27:
        cv2.destroyAllWindows()
        ipcam.stop()
        os.remove('output.png')
        break