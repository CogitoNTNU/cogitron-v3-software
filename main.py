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
ret, fram = cap.read()

print(ret)

#ser = serial.Serial('COM3', 9600, timeout=1)
#ser.reset_input_buffer()
ser2 = serial.Serial('COM5', 9600, timeout=1)
ser2.reset_input_buffer()

x_initial, x_angle = 81, 81
y_initial, y_angle = 75, 75

x_max = 180
y_max = 135
x_min = 0
y_min = 60

threshhold_size = 100
preferred_size_min = 200
preferred_size_max = 230


while True:

    _, img = cap.read()

    cv2.flip(img, 1, img)

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
    k = cv2.waitKey(15)

    imsize = img.shape
    image_center_x = imsize[1] / 2
    image_center_y = imsize[0] / 2

    speed = 1
    wheel_speed = 3 #Kjøre frem eller tilbake

    size = np.sqrt(size)
    

    # if size er stor nok
    if size > threshhold_size:
        
        if size > preferred_size_max:
            wheel_speed = 2
        elif size < preferred_size_min:
            wheel_speed = 1

        if abs(center_x - image_center_x) < 50:
            x_angle += 0
        elif center_x > image_center_x:
            x_angle += speed
        elif center_x < image_center_x:
            x_angle -= speed

        if abs(center_y - image_center_y) < 50:
            #print('just right')
            y_angle += 0
        elif center_y > image_center_y:
            #print('below')
            y_angle -= speed
        elif center_y < image_center_y:
            #print('above')
            y_angle += speed

    #else, gå mot x_initial, y_initial
    else:
        if x_angle > x_initial:
            x_angle -= speed
        elif x_angle < x_initial:
            x_angle += speed
        if y_angle > y_initial:
            y_angle -= speed
        elif y_angle < y_initial:
            y_angle += speed
    
    


    x_angle = clamp(x_angle, x_min, x_max)
    y_angle = clamp(y_angle, y_min, y_max)

    print(wheel_speed)

    #ser.write(bytes(str(x_angle) + "," + str(y_angle) + '\n', 'utf-8'))
    ser2.write(bytes(str(wheel_speed) + '\n', 'utf-8'))
    #print(str(x_angle) + "," + str(y_angle))
    time.sleep(0.02)
