# import the necessary packages
from imutils.video import VideoStream
from pyzbar import pyzbar
import imutils
import time
import cv2
import os
import csv


# initialize the video stream and allow the camera sensor to warm up

# rtsp = "rtsp://admin:admin@172.16.12.240:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"

# rtsp = "rtsp://root:camera@172.16.26.86:554/stream/profile0=u"

# Dahua Test Camera
rtsp = "rtsp://admin:admin@172.16.12.240:554/cam/realmonitor?channel=1&subtype=0&unicast=true&proto=Onvif"

# IronYun Right Front Door
# rtsp = "rtsp://Admin:1234@172.16.12.213/h264"

# IronYun Corridor
# rtsp = "rtsp://admin:admin888@172.16.22.142/axis-media/media.amp"

# IronYun Left Front Door
# rtsp = "rtsp://172.16.22.100:554/live01/ss-Tunnel/media?stream=6&channel=1"

# Office Corridor
# rtsp = "rtsp://user:ironyun168@172.16.22.132/h264"

# iPhon 6
# rtsp = "rtsp://172.16.26.91:8554/live.sdp"
# rtsp = "rtsp://192.168.100.143:8554/live.sdp"



image_file = "Barcode"
csv_file = image_file + "/Record.csv"

# found = set()

if not os.path.isdir(image_file):
    os.mkdir(image_file)

if not os.path.isfile(csv_file):
    with open(csv_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Time", "Barcode Type", "Barcode Content", "Image"])

print("[INFO] starting video stream...")
print("====================================================================")
vs = VideoStream(rtsp).start()
time.sleep(2.0)

# loop over the frames from the video stream
while True:
    startTime = time.time()
    # grab the frame from the threaded video stream and resize it to have a maximum width of 400 pixels
    frame = vs.read()

    # frame = imutils.resize(frame, width=800)

    # find the barcodes in the frame and decode each of the barcodes
    barcodes = pyzbar.decode(frame)

    # loop over the detected barcodes
    for barcode in barcodes:
        # extract the bounding box location of the barcode and draw the bounding box surrounding the barcode on the
        # image
        (x, y, w, h) = barcode.rect
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)


        # the barcode data is a bytes object so if we want to draw it on our output image we need to convert it to a
        # string first
        barcodeData = barcode.data.decode("utf-8")
        barcodeType = barcode.type

        # draw the barcode data and barcode type on the image
        text = "{} ({})".format(barcodeData, barcodeType)
        cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)


        # # if the barcode text is currently not in our CSV file, write the timestamp + barcode to disk and update the set
        # if barcodeData not in found:
        #     with open(csv_file, 'a+') as f:
        #         csv_write = csv.writer(f)
        #         nowDate = time.strftime("%Y-%m-%d_%H%M%S")
        #         nowTime = time.strftime("%Y-%m-%d %H:%M:%S")
        #         image_of_tag = image_file + "/" + nowDate + ".png"
        #         cv2.imwrite(image_of_tag, frame)
        #         data_row = [nowTime, barcodeType, barcodeData, image_of_tag]
        #         csv_write.writerow(data_row)
        #         found.add(barcodeData)
        #         print(" ")
        #         print("Time: " + nowTime)
        #         print("Barcode Detected: " + barcodeData + " (Type: " + barcodeType + ")")
        #         print("Image Saved: " + image_of_tag)


        with open(csv_file, 'a+') as f:
                csv_write = csv.writer(f)
                nowDate = time.strftime("%Y-%m-%d_%H%M%S")
                nowTime = time.strftime("%Y-%m-%d %H:%M:%S")
                image_of_tag = image_file + "/" + nowDate + ".png"
                cv2.imwrite(image_of_tag, frame)
                data_row = [nowTime, barcodeType, barcodeData, image_of_tag]
                csv_write.writerow(data_row)
                # found.add(barcodeData)

                endTime = time.time()
                print(" ")
                print("Time: " + nowTime)
                print("Barcode Detected: " + barcodeData + " (Type: " + barcodeType + ")")
                print("Pixel(W * H): " + str(w) + " * " + str(h))
                print("Image Saved: " + image_of_tag)
                print("Time Elapsed: " + str(endTime - startTime) + " seconds")

    # show the output frame
    cv2.imshow("Barcode Scanner", frame)
    key = cv2.waitKey(1) & 0xFF

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break

# close the output CSV file do a bit of cleanup
print("====================================================================")
print("[INFO] cleaning up...")
cv2.destroyAllWindows()
vs.stop()
