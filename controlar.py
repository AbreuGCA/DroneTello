from djitellopy import Tello
import pygame
import cv2
import numpy as np
from os import path
import time
import math

tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

pygame.init()
window_width = 960
window_height = 720
screen = pygame.display.set_mode([window_width, window_height])

def mesure_distance(rect_size):
    real_life_size = 25  # in cm
    cam_size = 700 # in px

    scale = real_life_size * cam_size
    return (scale / rect_size) # px to cm
    

def text_to_screen(screen, text, x, y, size = 50, color = (200, 000, 000)):
    try:
        text = str(text)
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception as e:
        print ('Font Error, saw it coming')
        raise e

project_path = path.dirname(path.abspath(__file__))
xml_path = path.join(project_path, 'haarcascade_frontalface_alt2.xml')

clf = cv2.CascadeClassifier(xml_path)
cap = cv2.VideoCapture(0)

should_stop = False
left_right = 0
up_down = 0
forward_backward = 0
yaw = 0

velocity = 10
last_x = 0
last_y = 0
last_w = 0
last_h = 0
while not should_stop:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                forward_backward = velocity
            if event.key == pygame.K_s:
                forward_backward = -velocity
            if event.key == pygame.K_a:
                left_right = -velocity
            if event.key == pygame.K_d:
                left_right = velocity
            if event.key == pygame.K_j:
                up_down = -velocity
            if event.key == pygame.K_k:
                up_down = velocity
            if event.key == pygame.K_h:
                yaw = -velocity
            if event.key == pygame.K_l:
                yaw = velocity
            if event.key == pygame.K_UP:
                tello.takeoff()
            if event.key == pygame.K_DOWN:
                tello.land()
#            if event.key == pygame.K_f:
#                tello.flip_back()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_w:
                forward_backward = 0
            if event.key == pygame.K_s:
                forward_backward = 0
            if event.key == pygame.K_a:
                left_right = 0
            if event.key == pygame.K_d:
                left_right = 0
            if event.key == pygame.K_j:
                up_down = 0
            if event.key == pygame.K_k:
                up_down = 0
            if event.key == pygame.K_h:
                yaw = 0
            if event.key == pygame.K_l:
                yaw = 0
        elif event.type == pygame.QUIT:
            should_stop = True
            pygame.quit()


    if frame_read.stopped:
        should_stop = True
        pygame.quit()

    frame = frame_read.frame
    #frame = np.rot90(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = clf.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=12, minSize=(50, 50))
    frame = np.rot90(frame)
    frame = pygame.surfarray.make_surface(frame)


    screen.blit(frame, (0, 0))

    left_line = window_width * 15 / 100
    right_line = window_width * 75 / 100
    pygame.draw.line(screen, (255, 0, 0), (left_line, 0), (left_line, window_height))
    pygame.draw.line(screen, (255, 0, 0), (right_line, 0), (right_line, window_height))

    left_right = 0
    mArea = -1000000
    mAX = -1
    mAY = -1
    rect_size = 0
    for x, y, w, h in faces:
        x = window_width - x - w
        aX = x + w / 2
        aY = y + h / 2

        #pygame.draw.circle(screen, (255, 0, 0), (aX, aY), 10)
        #pygame.draw.rect(screen, (0, 0, 255), (x, y, w, h), 1)

        if (mArea < (w * h)):
            mArea = w*h
            mAX = aX
            mAY = aY
            rect_size = w

    if (mAX != -1):
        dist = window_width/2 - mAX
        left_right = (1 if dist > 0 else -1) * 20
        yaw = (1 if dist > 0 else -1) * 50
        if (abs(dist) < window_width*10/100):
            left_right = 0
            yaw = 0

        pygame.draw.circle(screen, (255, 0, 0), (mAX, mAY), 10)
        dist_to_head = mesure_distance(rect_size)
        text = "%.2f cm" %dist_to_head
        text_to_screen(screen,text,100,100)

        if (dist_to_head > 100):
            forward_backward = velocity
        else:
            forward_backward = 0
            

    tello.send_rc_control(left_right, forward_backward, up_down, yaw)

    print(f"{tello.get_battery()}%")

    pygame.display.update()
    time.sleep(1 / 60)

tello.end()
