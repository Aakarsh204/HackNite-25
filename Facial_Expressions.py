import cv2
from deepface import DeepFace

# Initialize webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not access webcam.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error: Could not capture frame.")
        break

    # Perform emotion analysis
    try:
        analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
        emotion = analysis[0]['dominant_emotion']

        # Display emotion on screen
        cv2.putText(frame, f"Emotion: {emotion}", (20, 50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    except Exception as e:
        print(f"Error in analysis: {e}")
    
    # Show the frame
    cv2.imshow("Facial Emotion Recognition", frame)

    # Press 'q' to exit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
