import cv2
import dlib
import numpy as np
import time

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

def is_reading(left_pupil, right_pupil, prev_left_pupil, prev_right_pupil, frame_width):
    """
    Determine if the user is likely reading based on eye movements.
    Reading typically involves horizontal eye movements with minimal vertical change.
    """
    if prev_left_pupil is None or prev_right_pupil is None:
        return False
    
    # Calculate horizontal and vertical movement for both eyes
    left_h_movement = abs(left_pupil[0] - prev_left_pupil[0])
    left_v_movement = abs(left_pupil[1] - prev_left_pupil[1])
    right_h_movement = abs(right_pupil[0] - prev_right_pupil[0])
    right_v_movement = abs(right_pupil[1] - prev_right_pupil[1])
    
    # Reading patterns typically show:
    # 1. Some horizontal movement (saccades)
    # 2. Minimal vertical movement
    # 3. Both eyes move in coordinated way
    
    avg_h_movement = (left_h_movement + right_h_movement) / 2
    avg_v_movement = (left_v_movement + right_v_movement) / 2
    
    # Thresholds for reading detection
    min_h_movement = 2  # Minimum horizontal movement to detect reading
    max_h_movement = frame_width // 10  # Maximum reasonable horizontal movement
    max_v_movement = 5  # Maximum vertical movement (should be small during reading)
    
    return (min_h_movement <= avg_h_movement <= max_h_movement) and (avg_v_movement <= max_v_movement)

# Variables for reading detection
prev_left_pupil = None
prev_right_pupil = None
last_print_time = time.time()
reading_status = False

cap = cv2.VideoCapture(0)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame_width = frame.shape[1]
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector(gray)
    
    current_left_pupil = None
    current_right_pupil = None
    
    for face in faces:
        landmarks = predictor(gray, face)
        # Extract eye landmarks
        left_eye_points = [(landmarks.part(i).x, landmarks.part(i).y) for i in LEFT_EYE_INDICES]
        right_eye_points = [(landmarks.part(i).x, landmarks.part(i).y) for i in RIGHT_EYE_INDICES]
        left_center = get_eye_center(left_eye_points)
        right_center = get_eye_center(right_eye_points)
        
        # Get region around eye centers
        left_eye_region = frame[
            max(0, left_center[1]-10):min(frame.shape[0], left_center[1]+10), 
            max(0, left_center[0]-10):min(frame.shape[1], left_center[0]+10)
        ]
        right_eye_region = frame[
            max(0, right_center[1]-10):min(frame.shape[0], right_center[1]+10), 
            max(0, right_center[0]-10):min(frame.shape[1], right_center[0]+10)
        ]
        
        # Skip if regions are too small
        if left_eye_region.size == 0 or right_eye_region.size == 0:
            continue
            
        # Get pupil positions
        left_pupil = get_pupil_position(left_eye_region, left_center)
        right_pupil = get_pupil_position(right_eye_region, right_center)
        
        current_left_pupil = left_pupil
        current_right_pupil = right_pupil
        
        # Draw eyes and pupils
        cv2.circle(frame, left_center, 5, (0, 255, 0), -1)
        cv2.circle(frame, right_center, 5, (0, 255, 0), -1)
        cv2.circle(frame, left_pupil, 3, (0, 0, 255), -1)
        cv2.circle(frame, right_pupil, 3, (0, 0, 255), -1)
    
    # Check reading status and print every second
    current_time = time.time()
    if current_time - last_print_time >= 1.0:  # Print every second
        if current_left_pupil and current_right_pupil and prev_left_pupil and prev_right_pupil:
            reading_status = is_reading(current_left_pupil, current_right_pupil, 
                                        prev_left_pupil, prev_right_pupil, frame_width)
            
            if reading_status:
                print("yes")
            else:
                print("no")
                
        last_print_time = current_time
    
    # Store current pupil positions for next frame
    if current_left_pupil and current_right_pupil:
        prev_left_pupil = current_left_pupil
        prev_right_pupil = current_right_pupil
    
    # Display reading status on frame
    if reading_status:
        cv2.putText(frame, "Reading: YES", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    else:
        cv2.putText(frame, "Reading: NO", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
    
    cv2.imshow("Eye Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()