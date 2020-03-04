# -*- coding: utf-8 -*-
import os
import cv2
import zxing


def get_images_from_video(video_name, time_frames):
    video_images = []
    vc = cv2.VideoCapture(video_name)
    c = 1
    if vc.isOpened():
        rval, video_frame = vc.read()
    else:
        rval = False

    while rval:
        rval, video_frame = vc.read()

        if c % time_frames == 0:  # Capture every few frames
            video_images.append(video_frame)
        c = c + 1
    vc.release()

    return video_images


frames = 5  # The smaller time_f, the more frames
video = 'test_video.mov'  # Video name
images = get_images_from_video(video, frames)

# Show the images
for i in range(0, len(images)):
    cv2.imshow('windows', images[i])
    cv2.waitKey(100)

    image = "output.jpg"
    cv2.imwrite(image, images[i])
    cv2.waitKey(100)

    reader = zxing.BarCodeReader()
    barcode = reader.decode(image)
    if barcode is not None:
        print(barcode.parsed)
    else:
        print("No QR code or Barcode")

    if cv2.waitKey(1000) == 27:
        cv2.destroyAllWindows()
        os.remove('output.jpg')
        break
