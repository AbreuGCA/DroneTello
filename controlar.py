from djitellopy import Tello
import pygame
import cv2
import numpy as np
import time


tello = Tello()
tello.connect()

tello.streamon()
frame_read = tello.get_frame_read()

pygame.init()
screen = pygame.display.set_mode((800, 600))

def controlar_drone(key):
    match event.key:
        case pygame.K_w:
            # Frente
            print("frente")
            tello.move_forward(50)
        case pygame.K_s:
            # Tras
            print("Frente")
            tello.move_back(50)
        case pygame.K_d:
            # Direita
            print("Direita")
            tello.move_right(50)
        case pygame.K_a:
            # Esquerda
            print("Esquerda")
            tello.move_left(50)
        case pygame.K_UP:
            # Sobe
            print("Sobe")
            tello.takeoff()
        case pygame.K_DOWN:
            # Desce
            print("Desce")
            tello.land()
        case pygame.K_c:
            print("Girando")
            tello.rotate_clockwise(360)
        case pygame.K_f:
            print("Mortal")
            tello.flip_forward()
        case pygame.K_b:
            print(tello.get_battery())

should_stop = False
while not should_stop:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            controlar_drone(event.key)
        elif event.type == pygame.QUIT:
            should_stop = True
            pygame.quit()


    if frame_read.stopped:
        should_stop = True
        pygame.quit()

    frame = frame_read.frame
    frame = pygame.surfarray.make_surface(frame)
    screen.blit(frame, (0, 0))

    screen.fill((0, 0, 0))
    pygame.display.update()

    time.sleep(1 / 120)

tello.end()
