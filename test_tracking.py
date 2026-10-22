import cv2
import mediapipe as mp
import numpy as np
import math

# Emulate globals
YAW_DEGREES = 70
PITCH_DEGREES = 50
SCREEN_W = 1470
SCREEN_H = 956

INVERT_X = False
INVERT_Y = False

cap = cv2.VideoCapture(0)
face_landmarker = mp.tasks.vision.FaceLandmarker.create_from_options(
    mp.tasks.vision.FaceLandmarkerOptions(
        base_options=mp.tasks.BaseOptions(model_asset_path='face_landmarker.task'),
        running_mode=mp.tasks.vision.RunningMode.IMAGE
    )
)

LANDMARKS = {
    "left": 234,
    "right": 454,
    "top": 10,
    "bottom": 152,
    "front": 1,
}

auto_calibrated = False
calibration_offset_yaw = 0
calibration_offset_pitch = 0

print("Testing tracking...")
frame_count = 0
while frame_count < 30:
    success, frame = cap.read()
    if not success: continue
    
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_landmarker.detect(mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb))
    
    if results.face_landmarks:
        face = results.face_landmarks[0]
        pts = {}
        for name, idx in LANDMARKS.items():
            landmark = face[idx]
            pts[name] = np.array([landmark.x * w, landmark.y * h, landmark.z * w])
            
        left, right = pts["left"], pts["right"]
        top, bottom = pts["top"], pts["bottom"]
        front = pts["front"]
        
        right_axis = right - left
        right_axis /= np.linalg.norm(right_axis)
        up_axis = top - bottom
        up_axis /= np.linalg.norm(up_axis)
        forward_axis = -np.cross(right_axis, up_axis)
        forward_axis /= np.linalg.norm(forward_axis)
        
        xz_proj = np.array([forward_axis[0], 0, forward_axis[2]])
        xz_proj /= np.linalg.norm(xz_proj)
        yaw_rad = math.acos(np.clip(np.dot([0,0,-1], xz_proj), -1.0, 1.0))
        if forward_axis[0] < 0: yaw_rad = -yaw_rad
        
        yz_proj = np.array([0, forward_axis[1], forward_axis[2]])
        yz_proj /= np.linalg.norm(yz_proj)
        pitch_rad = math.acos(np.clip(np.dot([0,0,-1], yz_proj), -1.0, 1.0))
        if forward_axis[1] > 0: pitch_rad = -pitch_rad
        
        yaw_deg = np.degrees(yaw_rad)
        pitch_deg = np.degrees(pitch_rad)
        
        if not auto_calibrated:
            calibration_offset_yaw = -yaw_deg
            calibration_offset_pitch = -pitch_deg
            auto_calibrated = True
            
        centered_yaw = yaw_deg + calibration_offset_yaw
        centered_pitch = pitch_deg + calibration_offset_pitch
        
        screen_x = int(((centered_yaw + YAW_DEGREES) / (2 * YAW_DEGREES)) * SCREEN_W)
        screen_y = int(((centered_pitch + PITCH_DEGREES) / (2 * PITCH_DEGREES)) * SCREEN_H)
        
        print(f"Yaw: {centered_yaw:5.1f} | Pitch: {centered_pitch:5.1f} | Cursor: X={screen_x}, Y={screen_y}")
        frame_count += 1

cap.release()
print("Done.")
