import cv2
import numpy as np
import utils


curveList = []
avgVal = 10
cap = cv2.VideoCapture('vid1.mp4')
if not cap.isOpened():
    print("Error: Camera not found or unable to open")
    exit()

def getLaneCurve(img, display=2):
    timer = cv2.getTickCount()
    imgCopy = img.copy()
    imgResult = img.copy()

    # Thresholding and warping to get the lane area
    imgThres = utils.thresholding(img)
    hT, wT, c = img.shape
    points = utils.valTrackbars()
    imgWarp = utils.warpImg(imgThres, points, wT, hT)
    imgWarpPoints = utils.drawPoints(imgCopy, points)
    

    # Get the histogram and curve average points
    middlePoint, imgHist = utils.getHistogram(imgWarp, display=True, minPer=0.5, region=4)
    curveAveragePoint, imgHist = utils.getHistogram(imgWarp, display=True, minPer=0.9)

    # Debugging: Print the values of middlePoint and curveAveragePoint
    print(f"MiddlePoint: {middlePoint}, CurveAveragePoint: {curveAveragePoint}")

    # Calculate the curveRaw (difference between curve average and middle point)
    curveRaw = curveAveragePoint - middlePoint
    print(f"curveRaw: {curveRaw}")  # Ensure this is being printed

    curveList.append(curveRaw)
    if len(curveList) > avgVal:
        curveList.pop(0)

    # Smooth the curve by averaging the past few curve values
    curve = int(sum(curveList) / len(curveList))

    # Display the result
    if display != 0:
        imgInvWarp = utils.warpImg(imgWarp, points, wT, hT, inv=True)
        imgInvWarp = cv2.cvtColor(imgInvWarp, cv2.COLOR_GRAY2BGR)
        imgInvWarp[0:hT//3, 0:wT] = 0, 0, 0

        imgLaneColor = np.zeros_like(img)
        imgLaneColor[:] = 0, 255, 0
        imgLaneColor = cv2.bitwise_and(imgInvWarp, imgLaneColor)
        imgResult = cv2.addWeighted(imgResult, 1, imgLaneColor, 1, 0)

        midY = 450
        cv2.putText(imgResult, str(curve), (wT // 2 - 80, 85), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 255), 3)
        cv2.line(imgResult, (wT // 2, midY), (wT // 2 + (curve * 3), midY), (255, 0, 255), 5)
        cv2.line(imgResult, ((wT // 2 + (curve * 3)), midY - 25), (wT // 2 + (curve * 3), midY + 25), (0, 255, 0), 5)

        # Add visual cues for lane direction
        for x in range(-30, 30):
            w = wT // 20
            cv2.line(imgResult, (w * x + int(curve // 50), midY - 10),
                     (w * x + int(curve // 50), midY + 10), (0, 0, 255), 2)

        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        cv2.putText(imgResult, 'FPS ' + str(int(fps)), (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (230, 50, 50), 3)

    if display == 2:
        imgStacked = utils.stackImages(0.7, ([img, imgWarpPoints, imgWarp],
                                            [imgHist, imgLaneColor, imgResult]))
        cv2.imshow('ImageStack', imgStacked)
        cv2.imshow('Thresholded Image', imgThres)
        cv2.imshow('Histogram',imgHist)
    elif display == 1:
        cv2.imshow('Result', imgResult)

    # Normalize the curve value
    curve /= 100
    if curve > 1: curve = 1
    if curve < -1: curve = -1

    return curve

def getFrame():
    success, img = cap.read()
    if not success:
        print("Error: Failed to capture image from webcam.")
        return None
    img = cv2.resize(img, (480, 240))  # Resize if needed
    return img


'''
if __name__ == '__main__':
    cap = cv2.VideoCapture(0)
    initialTrackBarVals = [102, 80, 20, 214]
    utils.initializeTrackbars(initialTrackBarVals)
    frameCounter = 0

    while True:
        frameCounter += 1
        if cap.get(cv2.CAP_PROP_FRAME_COUNT) == frameCounter:
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            frameCounter = 0
        success, img = cap.read()
        img = cv2.resize(img, (480, 240))
        curve = getLaneCurve(img, display=2)
  '''      
if __name__ == '__main__':
    initialTrackBarVals = [102, 80, 20, 214]
    utils.initializeTrackbars(initialTrackBarVals)
    
    while True:
        img = getFrame()
        if img is None:
            continue
        success,img=cap.read()
        img=cv2.resize(img,(480,240))
        curve = getLaneCurve(img, display=2)
        cv2.waitKey(1)
        

        # cv2.imshow('vid', img)
        cv2.waitKey(1)
