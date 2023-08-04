# Import required libraries
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import math
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Set webcam resolution

wCAm, hCam = 640, 480



# Initialize webcam and set resolution
cap = cv2.VideoCapture(0)
cap.set(3,wCAm)
cap.set(4,hCam)
pTime = 0

# Initialize the hand detector object
detector = htm.handDetector(detectionCon=0.7)


# Get the audio output device and volume control interface
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# volume.GetMute()
# volume.GetMasterVolumeLevel()
# Get the volume range
volRange = volume.GetVolumeRange()
# print(volRange)
# volume.SetMasterVolumeLevel(0, None)
minVol = volRange[0]
maxVol = volRange[1]
vol = 0
volBar = 400
volPer = 0

###############################



while True:
    # Read a frame from the webcam
    success, img = cap.read()
    # Find hands in the frame
    img = detector.findHands(img)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:

######## Steps For Advance #####################
        # Filter based on size
        # Find Distance between index and thumb
        # Convert Volume
        # Reduce Rsolution to make it smoother
        #  Check fingers up
        # if pinky is down set volume
        # Drawings
        # Frame Rate
#############################################


        # print(lmList[4], lmList[8])
# Get the positions of the thumb and index finger
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2) // 2, (y1 + y2) //2 # for center of line

# Draw circles at the thumb and index finger tips and a line between them
        cv2.circle(img, (x1,y1), 10,(255,0,255), cv2.FILLED)
        cv2.circle(img, (x2,y2), 10,(255,0,255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2,y2), (255,0,255),3)
        cv2.circle(img, (cx,cy), 10,(255,0,255), cv2.FILLED)

# Calculate the distance between the thumb and index finger (length of the line)
        length = math.hypot(x2-x1, y2-y1)
        # print(length)

        # Hand range 20 - 200
        # volume range -65 to 0
        # Convert the distance (length) to volume
        vol = np.interp(length,[20,200],[minVol, maxVol])
        volBar = np.interp(length,[20,200],[400, 150])
        volPer = np.interp(length,[20,200],[0, 100])

        print(int(length),vol)
        volume.SetMasterVolumeLevel(vol, None)

        if length < 20:
            cv2.circle(img, (cx,cy), 10,(0,255,0), cv2.FILLED)
            
 # Draw the volume bar and percentage on the frame
    cv2.rectangle(img, (50,150),(85,400),(0,255,0),3)
    cv2.rectangle(img, (50,int(volBar)),(85,400),(0,255,0),cv2.FILLED)
    cv2.putText(img, f'{int(volPer)}%', (40,450),cv2.FONT_HERSHEY_COMPLEX,1,(0,250,0), 2)

# Calculate and display the frame rate
    cTime = time.time()
    fps = 1/(cTime-pTime)
    pTime = cTime

    cv2.putText(img, f'FPS: {int(fps)}', (40,50),cv2.FONT_HERSHEY_COMPLEX,1,(255,0,0), 2)

    cv2.imshow("Img", img)
    cv2.waitKey(1)