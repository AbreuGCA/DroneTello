import cv2
import os

def load_registered_faces(directory):
    registered_faces = []
    for filename in os.listdir(directory):
        if filename.endswith(".jpg"):
            face_img = cv2.imread(os.path.join(directory, filename), cv2.IMREAD_GRAYSCALE)
            registered_faces.append(face_img)
    return registered_faces

def detect_and_compare_face(cascade_path, registered_faces):
    face_cascade = cv2.CascadeClassifier(cascade_path)
    capture = cv2.VideoCapture(0)

    while True:
        ret, frame = capture.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        for (x, y, w, h) in faces:
            face_roi = gray[y:y+h, x:x+w]
            matched = False
            for registered_face in registered_faces:
                # Compare o rosto detectado com os rostos cadastrados
                similarity = cv2.matchTemplate(face_roi, registered_face, cv2.TM_CCOEFF_NORMED)
                if cv2.minMaxLoc(similarity)[1] >= 0.8:  # Defina um limiar de similaridade adequado
                    matched = True
                    break
            if matched:
                cv2.putText(frame, "Usuario cadastrado", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
            else:
                cv2.putText(frame, "Usuario nao cadastrado", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        cv2.imshow('Face Detection', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    cascade_path = 'haarcascade_frontalface_alt2.xml'
    registered_faces_directory = 'face_images'
    
    registered_faces = load_registered_faces(registered_faces_directory)
    detect_and_compare_face(cascade_path, registered_faces)
