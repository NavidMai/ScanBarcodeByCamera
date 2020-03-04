# -*- coding: utf-8 -*-
import os
import cv2
import csv
import time
import zxing
import threading


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

# Create .csv File
def create_csv():
  with open(csv_file, 'w', newline='') as csvfile:
     writer = csv.writer(csvfile)
     writer.writerow(["Time", "Barcode Content", "Image"])

# Write .csv File
def write_csv(time, barcode_content, image):
  with open(csv_file, 'a+') as f:
    csv_write = csv.writer(f)
    data_row = [time, barcode_content, image]
    csv_write.writerow(data_row)

# Camera RTSP
URL = "rtsp://admin:admin@172.16.12.240:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"
# URL = "rtsp://172.16.22.100:554/live01/ss-Tunnel/media?stream=5&channel=1"
image_file = "Barcode_Tag"
csv_file = image_file + "/Record.csv"
image_tmp = "output.png"

# Check the file path of the image of Tag which has a barcode or QR code appear.
if os.path.isdir(image_file):
    print("The image file exists!")
else:
    print("The image file does not exist!")
    print("Create a new image file......")
    os.mkdir(image_file)

if os.path.isfile(csv_file):
    print("The Record file exists!")
else:
    print("The Record file does not exist!")
    print("Create a new Record file......")
    create_csv()

# Use a loop to capture images until the user click the Esc key
ipcam = ipcamCapture(URL)
ipcam.start()
time.sleep(1)
print(" ")
print("Start analysis:")
print("========================================================================")

while True:
    # Get the latest image
    I = ipcam.getframe()
    cv2.imshow('Camera Viewer', I) # Show the image
    cv2.imwrite(image_tmp, I)
    # Scan Barcode and QR code
    reader = zxing.BarCodeReader()
    barcode = reader.decode(image_tmp)

    if barcode != None:
        print(barcode.parsed)
        nowTime = time.strftime("%Y%m%d%H%M%S")
        image_of_tag = image_file + "/Tag_" + nowTime + ".png"
        print("Image Saved: " + image_of_tag)
        cv2.imwrite(image_of_tag, I)
        write_csv(nowTime, barcode.parsed, image_of_tag)
    else:
        print("No QR code or Barcode")

    if cv2.waitKey(1000) == 27:
        cv2.destroyAllWindows()
        ipcam.stop()
        os.remove('output.png')
        break