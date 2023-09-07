import cv2
import os
from  cvzone.HandTrackingModule import HandDetector
import numpy as np
from tkinter import filedialog
# from save import save_image
from PIL import Image
from pdf_to_image import pdf_converter
from notification import notification
import time


    
def draw_on_file():
    #variables``
    width=500
    height=400
    folderpath=filedialog.askopenfilename()

    #converting a pdf into images and storing them into a folder
    pdf_converter(folderpath)

    #camera setup
    cap=cv2.VideoCapture(0)

    cap.set(3,width)
    cap.set(4,height)

    #get the list of images in folder
    pathImages=os.listdir('input')

    #variable
    imageNumber=1
    hs,ws=int(120*1),int(213*1)
    buttonpressed=False
    buttonCounter=0
    buttonDelay= 10
    red_annotations=[[]]
    red_index=-1
    purple_annotations=[[]]
    purple_index=-1
    annotation_Start=False


    # Hand Detector
    detector=HandDetector(detectionCon=0.8, maxHands=1)
    screen_width = 1280
    screen_height = 720
    color=(0,0,255)

    while True:
        success,imgg=cap.read()
        imgg=cv2.flip(imgg,1)
        pathfulimage= os.path.join('input',pathImages[imageNumber])
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
            xVal=int(np.interp(lmList[8][0],[0,width],[0,w]))
            yVal=int(np.interp(lmList[8][1],[0,height],[0,h]))
            indexfinger=xVal,yVal


            # left side accessing pics
            if(fingers==[1,0,0,0,0]):
                if(imageNumber>0):
                    red_annotations=[[]]
                    red_index=-1
                    purple_annotations=[[]]
                    purple_index=-1
                    annotation_Start=False
                    buttonpressed=True
                    imageNumber-=1


            # accessing images from folder     
            elif(fingers==[0,0,0,0,1]):  
                if(imageNumber<len(pathImages)-1):
                    red_annotations=[[]]
                    red_index=-1
                    purple_annotations=[[]]
                    purple_index=-1
                    annotation_Start=False
                    buttonpressed=True
                    imageNumber+=1


            # selection mode
            if(fingers==[0,1,1,0,0]):
                cv2.circle(img,indexfinger,20,color,cv2.FILLED)
                annotation_Start=False


            #gesture 4 draw on pointer
            if(fingers==[0,1,0,0,0]):
                if annotation_Start is False:
                    annotation_Start=True
                    red_index+=1
                    red_annotations.append([])
                    purple_index+=1
                    purple_annotations.append([])
                cv2.circle(img,indexfinger,15,color,cv2.FILLED)
                if color == (128,0,128):
                    purple_annotations[purple_index].append(indexfinger)
                else:
                    red_annotations[red_index].append(indexfinger)

            else:
                annotation_Start=False 
                

            #gesture 5 -Eraser last drawn line
            if fingers==[0,1,1,1,0]:
                if red_annotations:
                    red_annotations.pop(-1)
                    red_index-=1
                    buttonpressed=True


            # gesture 6-complete erase        
            if fingers==[0,1,1,1,1]:
                red_annotations=[[]]
                red_index=-1
                purple_annotations=[[]]
                purple_index=-1
                buttonpressed=True

            # gesture 7-save image in a particular file
            if fingers==[0,1,0,0,1]:
                for i in range (len(red_annotations)):
                    for j in range(len(red_annotations[i])):
                        if j!=0:
                            cv2.line(img,red_annotations[i][j-1],red_annotations[i][j],(200,0,0),8)
                #save purple color lines            
                overlay=img.copy()
                img1=img
                for i in range (len(purple_annotations)):
                    for j in range(len(purple_annotations[i])):
                        if j!=0:
                            start=purple_annotations[i][j-1]
                            end= purple_annotations[i][j]
                            cv2.line(overlay,start,end,(128,0,128),20)
                            img1=cv2.addWeighted(overlay,0.5,img,0.5,0.0)


                file_path = os.path.join("output", pathImages[imageNumber])
                image_to_save=Image.fromarray(img1)
                image_to_save.save(file_path)
                notification()

           
            #gesture 8 -change mode from drawing to highlighting    
            if fingers==[0,0,1,1,1]:
                if color==(128,0,128):
                    color=(0,0,255)
                    time.sleep(0.5)
                elif color==(0,0,255):
                    color=(128,0,128)
                    time.sleep(0.5)
                    
                cv2.circle(img,indexfinger,20,color,cv2.FILLED)
                annotation_Start=False



        #button pressed iterations
        if buttonpressed:
            buttonCounter+=1
            if(buttonDelay<buttonCounter):
                buttonCounter=0
                buttonpressed=False
        # print(buttonCounter)


        for i in range (len(red_annotations)):
            for j in range(len(red_annotations[i])):
                if j!=0:
                    # cv2.line(img,red_annotations[i][j-1],red_annotations[i][j],(0,0,200),3)
                    cv2.polylines(img,[ np.array([red_annotations[i][j-1], red_annotations[i][j]])],False,(0,0,200),4,cv2.LINE_AA)

        # overlay = np.zeros_like(img)+255
        overlay=img.copy()
        img1=img
        for i in range (len(purple_annotations)):
            for j in range(len(purple_annotations[i])):
                if j!=0:
                    start=purple_annotations[i][j-1]
                    end= purple_annotations[i][j]
                    cv2.line(overlay,start,end,(128,0,128),20)
                    img1=cv2.addWeighted(overlay,0.5,img,0.5,0.0)

        # img[0:hs,w-ws:w]=imgsmall
        cv2.imshow("image",imgg)
        cv2.imshow("slide",img1)


        key=cv2.waitKey(1)
        if key==ord('q'):
            break
    cv2.destroyAllWindows()  
      
def prevent_unnecesay():
    print("do not run the method unncessrly")

