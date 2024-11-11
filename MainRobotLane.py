import cv2
from MotorModule import MotorController
import LaneDetectionModule
from LaneDetectionModule import getLaneCurve
import utils
import time
import threading

motor = MotorController(2, 3, 4, 17, 27, 22)
def motor_control(curveVal):
    sen = 1.3  # SENSITIVITY
    maxVal = 0.3  # MAX SPEED
    if curveVal > maxVal:
        curveVal = maxVal
    if curveVal < -maxVal:
        curveVal = -maxVal

    if curveVal > 0:
        sen = 1.7
        if curveVal < 0.05:
            curveVal = 0
    else:
        if curveVal > -0.08:
            curveVal = 0

    motor.move(0.20, -curveVal * sen, 0.05)

def main():
    initialTrackBarVals = [102, 80, 20, 214]  
    start_time = time.time()
    img = LaneDetectionModule.getFrame()  # Get the frame from LaneDetectionModule
    processing_time=time.time() - start_time
    print(f"Processing time: {processing_time}")
    # Check if the image is valid (not None) before processing
    if img is None:
        print("Error: Failed to capture image from webcam.")
        return  # Exit or handle the error gracefully

    curveVal = LaneDetectionModule.getLaneCurve(img, 2)
    threading.Thread(target=motor_control(curveVal)).start()

if __name__ == '__main__':
    while True:
        main()
