import cv2
from  cvzone.HandTrackingModule import HandDetector
import numpy as np
from save import save_image
from PIL import Image
import time
from notification import notification

def avoid():
    pass


#variables
# folderpath="testImages"

width=500
height=400

#camera setup
cap=cv2.VideoCapture(0)
cap.set(3,width)
cap.set(4,height)

#get the list of images in folder
# pathImages=os.listdir(folderpath)

#variable
# imageNumber=1
# hs,ws=int(120*1),int(213*1)
buttonpressed=False
buttonCounter=0
buttonDelay= 10
annotations=[[]]
annotation_number=-1
annotation_Start=False


# Hand Detector
detector=HandDetector(detectionCon=0.8, maxHands=1)
# paintWindow = np.zeros((720,1280,3), dtype=np.uint8) + 255

check=True
#used in gesture 7 to keep a check on creating new folder

while True:
    success,imgg=cap.read()
    imgg=cv2.flip(imgg,1)
    # pathfulimage= os.path.join(folderpath,pathImages[imageNumber])
    # img= cv2.imread(pathfulimage)
    paintWindow=np.zeros((720,1280, 3),dtype=np.uint8)+255
    # cv2.rectangle(paintWindow, (40,1), (140,65), (0,0,0), 2)

    
    hands,imgg=detector.findHands(imgg)

    if hands :
        hand=hands[0]
        fingers=detector.fingersUp(hand)
        lmList=hand['lmList']
        xVal=int(np.interp(lmList[8][0],[0,width//2],[0,w]))
        yVal=int(np.interp(lmList[8][1],[150,height-150],[0,h]))
        indexfinger=xVal,yVal


        # Gesture 1
        if(fingers==[1,0,0,0,0]):
                annotations=[[]]
                annotation_number=-1
                annotation_Start=False
                buttonpressed=True


        # Gesture 2        
        elif(fingers==[0,0,0,0,1]):  
                annotations=[[]]
                annotation_number=-1
                annotation_Start=False
                buttonpressed=True


        # Gesture 3
        if(fingers==[0,1,1,0,0]):
            cv2.circle(paintWindow,indexfinger,20,(0,0,225),cv2.FILLED)
            annotation_Start=False


        #gesture 4 draw on pointer
        if(fingers==[0,1,0,0,0]):
            if annotation_Start is False:
                annotation_Start=True
                annotation_number+=1
                annotations.append([])
            cv2.circle(paintWindow,indexfinger,20,(0,0,225),cv2.FILLED)
            annotations[annotation_number].append(indexfinger)
        else:
            annotation_Start=False 
            

        #gesture 5 -Eraser last drawn line
        if fingers==[0,1,1,1,0]:
            if annotations:
                annotations.pop(-1)
                annotation_number-=1
                buttonpressed=True
                time.sleep(0.2)


        # gesture 6-complete erase        
        if fingers==[0,1,1,1,1]:
            annotations=[[]]
            annotation_number=-1
            buttonpressed=True

        # gesture 7-to same image in same folder /replace original image with current image
        if fingers==[0,1,0,0,1]:
            #  image_to_save=Image.fromarray(paintWindow)
            for i in range (len(annotations)):
                for j in range(len(annotations[i])):
                    if j!=0:
                        cv2.line(paintWindow,annotations[i][j-1],annotations[i][j],(200,0,0),12)
            image_to_save=Image.fromarray(paintWindow)
            # if(check==True):
            #  fol=val()
            #  check=False
            save_image(image_to_save)
            notification()
            
            


    for i in range (len(annotations)):
        for j in range(len(annotations[i])):
            if j!=0:
                cv2.line(paintWindow,annotations[i][j-1],annotations[i][j],(0,0,200),12)





    screen_width = 1280
    screen_height = 720

    h,w,_=paintWindow.shape 
    # img[0:hs,w-ws:w]=imgsmall
    cv2.imshow("image",imgg)
    cv2.imshow("slide",paintWindow)


    key=cv2.waitKey(1)
    if key==ord('q'):
        break
cv2.destroyAllWindows()    



