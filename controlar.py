from djitellopy import Tello
import pygame
import cv2
import numpy as np
from os import path
import time


tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

pygame.init()
screen = pygame.display.set_mode([960, 720])

project_path = path.dirname(path.abspath(__file__))
xml_path = path.join(project_path, 'haarcascade_frontalface_alt2.xml')

clf = cv2.CascadeClassifier(xml_path)
cap = cv2.VideoCapture(0)

should_stop = False
left_right = 0
up_down = 0
forward_backward = 0
yaw = 0

velocity = 50
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
    frame = np.rot90(frame)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = clf.detectMultiScale(gray)


    frame = pygame.surfarray.make_surface(frame)

    tello.send_rc_control(left_right, forward_backward, up_down, yaw)

    screen.blit(frame, (0, 0))

    for x, y, w, h in faces:
        pygame.draw.rect(screen, (0, 0, 255), (x, y, w, h))

    pygame.display.update()

    time.sleep(1 / 120)

tello.end()
