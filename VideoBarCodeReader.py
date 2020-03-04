import os
import cv2
import zxing


def get_images_from_video(video_name, time_F):
    video_images = []
    vc = cv2.VideoCapture(video_name)
    c = 1
    if vc.isOpened():
        rval, video_frame = vc.read()
    else:
        rval = False

    while rval:
        rval, video_frame = vc.read()

        if (c % time_F == 0):  # Capture every few frames
            video_images.append(video_frame)
        c = c + 1
    vc.release()

    return video_images

time_F = 5 #The smaller time_F, the more frames
video_name = 'navid.mov' #Video name
video_images = get_images_from_video(video_name, time_F)

for i in range(0, len(video_images)): #Show the images
    cv2.imshow('windows', video_images[i])
    cv2.waitKey(100)

    image = "output.jpg"
    cv2.imwrite(image, video_images[i])
    cv2.waitKey(100)

    reader = zxing.BarCodeReader()
    barcode = reader.decode(image)
    if barcode != None:
        print(barcode.parsed)
    else:
        print("No QR code or Barcode")

cv2.destroyAllWindows()
os.remove('output.jpg')

