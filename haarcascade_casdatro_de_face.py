import cv2
import pygame
import os

def capture_face(cascade_path):
    face_cascade = cv2.CascadeClassifier(cascade_path)
    capture = cv2.VideoCapture(0)

    if not os.path.exists("face_images"):
        os.makedirs("face_images")

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Capture Face', frame)

        if cv2.waitKey(1) & 0xFF == ord('c'):
            # Salvar a imagem do rosto
            face_img = gray[y:y+h, x:x+w]
            cv2.imwrite("face_images/face_{}.jpg".format(len(os.listdir("face_images")) + 1), face_img)
            print("Face captured and saved!")
            #break

    capture.release()
    cv2.destroyAllWindows()

def detect_face(cascade_path):
    face_cascade = cv2.CascadeClassifier(cascade_path)
    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            # Aqui você adicionaria a lógica para comparar os rostos detectados com os rostos cadastrados
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    cascade_path = 'haarcascade_frontalface_alt2.xml'
    pygame.init()
    pygame.display.set_mode((300, 100))
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    capture_face(cascade_path)
                elif event.key == pygame.K_q:
                    detect_face(cascade_path)
                    pygame.quit()
                    quit()
