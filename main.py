import glob

import cv2
import time

import emailer

video = cv2.VideoCapture(0)
time.sleep(1)
first_frame = None
status_list = []
count = 1
while True:
    status = 0
    success, frame = video.read()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_frame_gau = cv2.GaussianBlur(gray_frame, (3, 3), 0)

    if first_frame is None:
        first_frame = gray_frame_gau
    delta = cv2.absdiff(first_frame, gray_frame_gau)

    thresh_frame = cv2.threshold(delta, 30, 255, cv2.THRESH_BINARY)[1]

    dil_frame = cv2.dilate(thresh_frame, None, iterations=2)
    cv2.imshow("Frame_dilate", dil_frame)

    contours, check = cv2.findContours(dil_frame, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour in contours:
        if cv2.contourArea(contour) < 10000:
            continue
        else:
            x, y, w, h = cv2.boundingRect(contour)
            rectangles = cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            if rectangles.any():
                status = 1
                cv2.imwrite(f"./images/{count}.png", frame)
                print(f"images/{count}.png")
                count += 1
                all_images = glob.glob(f"images/*.png")


    status_list.append(status)
    status_list = status_list[-2:]
    print(status_list)
    if status_list[0] == 1 and status_list[1] == 0:
        index = int(len(all_images) / 2)
        emailer.send_email(all_images[index])
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1)

    if key == ord('q'):
        break

video.release()