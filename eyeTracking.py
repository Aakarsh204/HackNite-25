import cv2
import dlib
import numpy as np

# Initialize dlib's face detector and facial landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")  # Download from dlib repo

# Indices for eye landmarks (from dlib's 68 landmark model)
LEFT_EYE_INDICES = list(range(36, 42))
RIGHT_EYE_INDICES = list(range(42, 48))

def get_eye_center(eye_points):
    """Calculate the center of the eye by averaging landmark points."""
    x = sum([p[0] for p in eye_points]) // len(eye_points)
    y = sum([p[1] for p in eye_points]) // len(eye_points)
    return (x, y)

def get_pupil_position(eye_region, eye_center):
    """Find the darkest region (likely pupil) in the eye."""
    gray_eye = cv2.cvtColor(eye_region, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_eye, 50, 255, cv2.THRESH_BINARY_INV)
    
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        M = cv2.moments(max_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            return (eye_center[0] + cx, eye_center[1] + cy)
    return eye_center  # Fallback to center if no pupil found

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)

    for face in faces:
        landmarks = predictor(gray, face)

        # Extract eye landmarks
        left_eye_points = [(landmarks.part(i).x, landmarks.part(i).y) for i in LEFT_EYE_INDICES]
        right_eye_points = [(landmarks.part(i).x, landmarks.part(i).y) for i in RIGHT_EYE_INDICES]

        left_center = get_eye_center(left_eye_points)
        right_center = get_eye_center(right_eye_points)

        # Get pupil positions
        left_pupil = get_pupil_position(frame[left_center[1]-10:left_center[1]+10, left_center[0]-10:left_center[0]+10], left_center)
        right_pupil = get_pupil_position(frame[right_center[1]-10:right_center[1]+10, right_center[0]-10:right_center[0]+10], right_center)

        # Draw eyes and pupils
        cv2.circle(frame, left_center, 5, (0, 255, 0), -1)
        cv2.circle(frame, right_center, 5, (0, 255, 0), -1)
        cv2.circle(frame, left_pupil, 3, (0, 0, 255), -1)
        cv2.circle(frame, right_pupil, 3, (0, 0, 255), -1)

    cv2.imshow("Eye Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
