import cv2
import dlib
import numpy as np
import time
import av
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase
from streamlit.components.v1 import html

# Initialize dlib components
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Constants
LEFT_EYE_INDICES = list(range(36, 42))
RIGHT_EYE_INDICES = list(range(42, 48))

class EyeProcessor(VideoProcessorBase):
    def __init__(self):
        super().__init__()
        self.prev_left_pupil = None
        self.prev_right_pupil = None
        self.reading_status = False
        self.last_update = time.time()
        self.status_log = []
        self.last_face_time = time.time()

    def get_eye_center(self, eye_points):
        x = sum([p[0] for p in eye_points]) // len(eye_points)
        y = sum([p[1] for p in eye_points]) // len(eye_points)
        return (x, y)

    def get_pupil_position(self, eye_region, eye_center):
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
        return eye_center

    def is_reading(self, left_pupil, right_pupil, frame_width):
        if not self.prev_left_pupil or not self.prev_right_pupil:
            return False

        left_h = abs(left_pupil[0] - self.prev_left_pupil[0])
        left_v = abs(left_pupil[1] - self.prev_left_pupil[1])
        right_h = abs(right_pupil[0] - self.prev_right_pupil[0])
        right_v = abs(right_pupil[1] - self.prev_right_pupil[1])

        avg_h = (left_h + right_h) / 2
        avg_v = (left_v + right_v) / 2

        return (2 <= avg_h <= frame_width // 10) and (avg_v <= 5)

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = detector(gray)
        
        if len(faces) > 0:
            self.last_face_time = time.time()

        current_left_pupil = None
        current_right_pupil = None

        for face in faces:
            landmarks = predictor(gray, face)
            
            # Left eye processing
            left_eye_points = [(landmarks.part(i).x, landmarks.part(i).y) 
                             for i in LEFT_EYE_INDICES]
            left_center = self.get_eye_center(left_eye_points)
            left_region = img[
                max(0, left_center[1]-10):min(img.shape[0], left_center[1]+10),
                max(0, left_center[0]-10):min(img.shape[1], left_center[0]+10)
            ]
            if left_region.size > 0:
                left_pupil = self.get_pupil_position(left_region, left_center)
                current_left_pupil = left_pupil
                cv2.circle(img, left_center, 5, (0, 255, 0), -1)
                cv2.circle(img, left_pupil, 3, (0, 0, 255), -1)

            # Right eye processing
            right_eye_points = [(landmarks.part(i).x, landmarks.part(i).y) 
                              for i in RIGHT_EYE_INDICES]
            right_center = self.get_eye_center(right_eye_points)
            right_region = img[
                max(0, right_center[1]-10):min(img.shape[0], right_center[1]+10),
                max(0, right_center[0]-10):min(img.shape[1], right_center[0]+10)
            ]
            if right_region.size > 0:
                right_pupil = self.get_pupil_position(right_region, right_center)
                current_right_pupil = right_pupil
                cv2.circle(img, right_center, 5, (0, 255, 0), -1)
                cv2.circle(img, right_pupil, 3, (0, 0, 255), -1)

        if current_left_pupil and current_right_pupil:
            self.reading_status = self.is_reading(current_left_pupil, 
                                                current_right_pupil, 
                                                img.shape[1])
            self.prev_left_pupil = current_left_pupil
            self.prev_right_pupil = current_right_pupil

            if time.time() - self.last_update >= 1:
                self.status_log.append(
                    ("Reading" if self.reading_status else "Not reading", 
                     time.strftime("%H:%M:%S")))
                self.last_update = time.time()

        color = (0, 255, 0) if self.reading_status else (0, 0, 255)
        cv2.putText(img, f"Reading: {'YES' if self.reading_status else 'NO'}", 
                   (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        
        return av.VideoFrame.from_ndarray(img, format="bgr24")

def main():
    st.title("Real-time Reading Detection 👁️")
    st.markdown("""
    ## This app detects reading behavior using eye movement analysis
    - Uses dlib's facial landmark detection
    - Tracks pupil movements
    - Identifies characteristic reading patterns
    """)
    
    # Initialize session state
    if 'alert_shown' not in st.session_state:
        st.session_state.alert_shown = False

    ctx = webrtc_streamer(
        key="eye-tracker",
        video_processor_factory=EyeProcessor,
        frontend_rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )
    
    if ctx.video_processor:
        st.subheader("Reading Status Log")
        if st.button("Clear Log"):
            ctx.video_processor.status_log = []
        
        if ctx.video_processor.status_log:
            log_text = "\n".join(
                [f"{status[1]} - {status[0]}" 
                 for status in ctx.video_processor.status_log[-10:]]
            )
            st.text_area("Log", value=log_text, height=200, key="log_display")
        
        # Alert system
        absence_duration = time.time() - ctx.video_processor.last_face_time
        if absence_duration > 10 and not st.session_state.alert_shown:
            # Inject JavaScript alert
            html_code = """
            <script>
            window.alert("⚠️ Please look back at the screen! You haven't been looking for 10 seconds.");
            </script>
            """
            html(html_code, width=0, height=0)
            st.session_state.alert_shown = True  # Corrected typo from alert_shown
            
        # Reset alert when user returns
        if absence_duration < 2 and st.session_state.alert_shown:
            st.session_state.alert_shown = False

if __name__ == "__main__":
    main()