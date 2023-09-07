import cv2
import os
from  cvzone.HandTrackingModule import HandDetector
import numpy as np
from tkinter import filedialog
from save import save_image
from PIL import Image
# from pdf_to_image import pdf_converter
from notification import notification


def prevent_unnecesay():
    print("do not run the method unncessrly")

    
def draw_on_image():
    #variables``
    width=500
    height=400
    folderpath=filedialog.askdirectory()

    #converting a pdf into images and storing them into a folder
    # pdf_converter(folderpath)

    #camera setup
    cap=cv2.VideoCapture(0)

    cap.set(3,width)
    cap.set(4,height)

    #get the list of images in folder
    pathImages=os.listdir(folderpath)

    #variable
    imageNumber=1
    hs,ws=int(120*1),int(213*1)
    buttonpressed=False
    buttonCounter=0
    buttonDelay= 10
    annotations=[[]]
    annotation_number=-1
    annotation_Start=False


    # Hand Detector
    detector=HandDetector(detectionCon=0.8, maxHands=1)
    screen_width = 1280
    screen_height = 720

    while True:
        success,imgg=cap.read()
        imgg=cv2.flip(imgg,1)
        pathfulimage= os.path.join(folderpath,pathImages[imageNumber])
        img= cv2.imread(pathfulimage)

        #resizing image to get proper size
        img_height, img_width = img.shape[:2]
        scale = min(screen_width/img_width, screen_height/img_height)
        img = cv2.resize(img, None, fx=scale, fy=scale)
        # imgg=cv2.resize(imgg,None,fx=scale,fy=scale)
        h,w,_=img.shape 

        # adding webcam image to slide
        imgsmall=cv2.resize(imgg,(ws,hs))

        #detect hand on live frame
        hands,imgg=detector.findHands(imgg)

        if hands and buttonpressed is False:
            hand=hands[0]
            fingers=detector.fingersUp(hand)
            lmList=hand['lmList']
            xVal=int(np.interp(lmList[8][0],[0,width//2],[0,w]))
            yVal=int(np.interp(lmList[8][1],[0,height//2],[0,h]))
            indexfinger=xVal,yVal


            # left side accessing pics
            if(fingers==[1,0,0,0,0]):
                if(imageNumber>0):
                    annotations=[[]]
                    annotation_number=-1
                    annotation_Start=False
                    buttonpressed=True
                    imageNumber-=1


            # accessing images from folder     
            elif(fingers==[0,0,0,0,1]):  
                if(imageNumber<len(pathImages)-1):
                    annotations=[[]]
                    annotation_number=-1
                    annotation_Start=False
                    buttonpressed=True
                    imageNumber+=1


            # selection mode
            if(fingers==[0,1,1,0,0]):
                cv2.circle(img,indexfinger,20,(0,0,225),cv2.FILLED)
                annotation_Start=False


            #gesture 4 draw on pointer
            if(fingers==[0,1,0,0,0]):
                if annotation_Start is False:
                    annotation_Start=True
                    annotation_number+=1
                    annotations.append([])
                cv2.circle(img,indexfinger,15,(0,0,225),cv2.FILLED)
                annotations[annotation_number].append(indexfinger)
            else:
                annotation_Start=False 
                

            #gesture 5 -Eraser last drawn line
            if fingers==[0,1,1,1,0]:
                if annotations:
                    annotations.pop(-1)
                    annotation_number-=1
                    buttonpressed=True


            # gesture 6-complete erase        
            if fingers==[0,1,1,1,1]:
                annotations=[[]]
                annotation_number=-1
                buttonpressed=True

            # gesture 7-save image in a particular file
            if fingers==[0,1,0,0,1]:
                for i in range (len(annotations)):
                    for j in range(len(annotations[i])):
                        if j!=0:
                            cv2.line(img,annotations[i][j-1],annotations[i][j],(200,0,0),8)
                file_path = os.path.join("output", pathImages[imageNumber])
                image_to_save=Image.fromarray(img)
                image_to_save.save(file_path)
                notification()



        #button pressed iterations
        if buttonpressed:
            buttonCounter+=1
            if(buttonDelay<buttonCounter):
                buttonCounter=0
                buttonpressed=False
        # print(buttonCounter)


        for i in range (len(annotations)):
            for j in range(len(annotations[i])):
                if j!=0:
                    cv2.line(img,annotations[i][j-1],annotations[i][j],(0,0,200),8)


        # img[0:hs,w-ws:w]=imgsmall
        cv2.imshow("image",imgg)
        cv2.imshow("slide",img)


        key=cv2.waitKey(1)
        if key==ord('q'):
            break
    cv2.destroyAllWindows()    
    
draw_on_image()