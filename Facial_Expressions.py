import cv2
from deepface import DeepFace
import av
import time
from streamlit_webrtc import VideoProcessorBase

class EmotionProcessor(VideoProcessorBase):
    def __init__(self):
        super().__init__()
        self.emotion_log = []
        self.last_update = time.time()

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        
        # Perform emotion analysis
        try:
            analysis = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False)
            emotion = analysis[0]['dominant_emotion']
            
            # Update emotion log every second
            if time.time() - self.last_update >= 1:
                self.emotion_log.append((emotion, time.strftime("%H:%M:%S")))
                self.last_update = time.time()
            
            # Display emotion on screen
            cv2.putText(img, f"Emotion: {emotion}", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
        except Exception as e:
            print(f"Error in analysis: {e}")
            cv2.putText(img, "No face detected", (20, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")
