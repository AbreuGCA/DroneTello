import cv2 as cv

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("Cannot open camera")
    exit(1)

dictionary = cv.aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_1000)
parametrers = cv.aruco.DetectorParameters()
detector = cv.aruco.ArucoDetector(dictionary, parametrers)

should_stop = False
while not should_stop:
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame")
        exit(1)

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    corners, id, _ = detector.detectMarkers(gray)

    if not id == None:
        print(id)

    cv.imshow("", gray)
    
    if cv.waitKey(1) == ord('q'):
        should_stop = True

cap.release()
cv.destroyAllWindows()