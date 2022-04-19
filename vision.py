import cv2
import serial
import numpy as np
import time


def clamp(x, min, max):
    if x < min:
        return min
    if x > max:
        return max
    return x


# Load the cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# To capture video from webcam.
cap = cv2.VideoCapture(0)

ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
ser.reset_input_buffer()

x_angle = 90
y_angle = 90

x_max = 180
y_max = 135
x_min = 0
y_min = 60

while True:

    _, img = cap.read()

    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray)

    center_x = -1
    center_y = -1
    # Draw the rectangle around each face
    size = 0
    index = 0
    for i, (x, y, w, h) in enumerate(faces):
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

        s = w * h
        if s > size:
            size = s
            center_x = x + w / 2
            center_y = y + h / 2

    # Display
    cv2.imshow('img', img)
    k = cv2.waitKey(30)

    imsize = img.shape
    image_center_x = imsize[1] / 2
    image_center_y = imsize[0] / 2

    speed = 3

    if abs(center_x - image_center_x) < 50:
        x_angle += 0
    elif center_x > image_center_x:
        x_angle += speed
    elif center_x < image_center_x:
        x_angle -= speed

    if abs(center_y - image_center_y) < 50:
        print('just right')
        y_angle += 0
    elif center_y > image_center_y:
        print('below')
        y_angle -= speed
    elif center_y < image_center_y:
        print('above')
        y_angle += speed

    x_angle = clamp(x_angle, x_min, x_max)
    y_angle = clamp(y_angle, y_min, y_max)

    ser.write(bytes(str(x_angle) + "\n", 'utf-8'))
    time.sleep(0.001)
    ser.write(bytes(str(y_angle) + "\n", 'utf-8'))
    time.sleep(0.001)
