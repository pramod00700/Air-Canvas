import cv2
import numpy as np
import time
import os
from save import save_image
from  cvzone.HandTrackingModule import HandDetector
# from collections import deque
from PIL import Image
from notification import notification
import random
import math

def point_inside_circle(point, center, radius):
    if len(point)!=0:
        x, y = point
        center_x, center_y = center

        distance = math.sqrt((x - center_x) ** 2 + (y - center_y) ** 2)

        if distance <= radius:
            return True
        else:
            return False
    return False  

def paint():
    # Giving different arrays to handle colour points of different colour
    bpoints = [[]]
    gpoints = [[]]
    rpoints = [[]]
    ypoints = [[]]
    wpoints = [[]]
    allpoints=[[]]

    # These indexes will be used to mark the points in particular arrays of specific colour
    blue_index = 0
    green_index = 0
    red_index = 0
    yellow_index = 0
    white_index=0
    universalindex=0

    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255),(0,0,0)]
    colorIndex = 0





    # folder_path= "header"
    # mylist=os.listdir(folder_path)
    # print(mylist)
    overlayList=[]

    

    #object to capture live frame
    cap=cv2.VideoCapture(0)
    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, )
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 283)


    buttonpressed=False
    buttonCounter=0
    buttonDelay= 10
    # annotations=[[]]
    # annotation_number=-1
    annotation_Start=False
    color=(255,0,0)



    #detect hand gesture
    detector=HandDetector(detectionCon=0.8, maxHands=1)  
    thickness=5

    while True:
        #importing live frame
        success,img=cap.read()
        img=cv2.flip(img,1)

        img = cv2.rectangle(img, (40,1), (140,65), (240,240,240),cv2.FILLED)
        img = cv2.rectangle(img, (160,1), (255,65), (255,0,0),cv2.FILLED)
        img = cv2.rectangle(img, (275,1), (370,65), (0,255,0), cv2.FILLED)
        img = cv2.rectangle(img, (390,1), (485,65), (0,0,255), cv2.FILLED)
        img = cv2.rectangle(img, (505,1), (600,65), (0,255,255), cv2.FILLED)

        cv2.putText(img, "ERASER", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (1,1,1), 2, cv2.LINE_AA)
        cv2.putText(img, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(img, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)

        paintWindow=np.zeros((480,640, 3),dtype=np.uint8)+255
        paintWindow = cv2.rectangle(paintWindow, (40,1), (140,65), (240,240,240),cv2.FILLED)
        paintWindow = cv2.rectangle(paintWindow, (160,1), (255,65), (255,0,0),cv2.FILLED)
        paintWindow = cv2.rectangle(paintWindow, (275,1), (370,65), (0,255,0), cv2.FILLED)
        paintWindow = cv2.rectangle(paintWindow, (390,1), (485,65), (0,0,255), cv2.FILLED)
        paintWindow = cv2.rectangle(paintWindow, (505,1), (600,65), (0,255,255), cv2.FILLED)

        cv2.putText(paintWindow, "ERASER", (49, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (1, 1, 1), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "BLUE", (185, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "GREEN", (298, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "RED", (420, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)
        cv2.putText(paintWindow, "YELLOW", (520, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2, cv2.LINE_AA)


        points = [bpoints, gpoints, rpoints, ypoints,wpoints]

        #find hand gestures
        hands,img=detector.findHands(img)

        if hands:
            hand=hands[0]
            fingers=detector.fingersUp(hand)
            lmList=hand['lmList']

            # if len(lmList)!=0:
                # print(lmList)

            #tip of index finger    
            #x1,y1=lmList[8][1:]
            indexfinger=lmList[8][0],lmList[8][1]
            x2,y2=lmList[12][1:]
            
            #detect fingers that are up
            fingers=detector.fingersUp(hands[0])
            # print(fingers)

            #default thickess of marker

            # selection mode
            if fingers==[0,1,1,0,0]:
                #checking for the click
                annotation_Start=False
                if(indexfinger[1]<65):
                    # print('selection mode')
                    if 40<indexfinger[0]<140:
                        color=(0,0,0)
                        colorIndex=4
                    elif 160<indexfinger[0]<255:
                        # header=overlayList[0]
                        color=(255,0,0)
                        colorIndex=0
                        # cv2.circle(paintWindow,indexfinger,20,(0,0,225),cv2.FILLED) 
                    elif 275<indexfinger[0]<370:
                        # header=overlayList[1]
                        color=(0,255,0)
                        colorIndex=1
                        # cv2.circle(paintWindow,indexfinger,20,(0,255,0),cv2.FILLED) 
                    elif 390<indexfinger[0]<485:
                        color=(0,0,255)
                        colorIndex=2
                        # header=overlayList[2]
                    elif 505<indexfinger[0]<600:
                        color=(0,255,255)
                        colorIndex=3
                        # header=overlayList[3]     
                cv2.circle(paintWindow,indexfinger,20,color,cv2.FILLED) 
                
            if (color==(0,0,0) and fingers==[0,1,0,0,0]):
                # print("inside condition")
                cv2.circle(paintWindow,indexfinger,20,color,cv2.FILLED)                 
                for i in range(len(points)-1):
                    for j in range(len(points[i])):
                        for k in range(1, len(points[i][j])):
                            if points[i][j][k - 1] is None or points[i][j][k] is None:
                                continue
                            # cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i],2,cv2.LINE_AA)
                            if(len(points[i][j][k])!=0 and point_inside_circle(points[i][j][k-1],indexfinger,20)):
                                points[i][j][k-1]=()


            # writing mode
            if fingers==[0,1,0,0,0]:
                # print('writing mode')
                if annotation_Start is False:
                    annotation_Start=True
                    bpoints.append([])
                    blue_index += 1
                    gpoints.append([])
                    green_index += 1
                    rpoints.append([])
                    red_index += 1
                    ypoints.append([])
                    yellow_index += 1     
                    wpoints.append([])
                    white_index += 1     
                    allpoints.append([])
                    universalindex+=1
                cv2.circle(paintWindow,indexfinger,20,color,cv2.FILLED)
                if colorIndex == 0:
                    if blue_index<0:
                        blue_index=0
                    # print("blue"+str(blue_index))    
                    bpoints[blue_index].append(indexfinger)
                    allpoints[universalindex].append(indexfinger)
                elif colorIndex == 1:
                    if green_index<0:
                        green_index=0
                    # print("green"+str(green_index))    
                    gpoints[green_index].append(indexfinger)
                    allpoints[universalindex].append(indexfinger)
                elif colorIndex == 2:
                    if red_index<0:
                        red_index=0
                    # print("red"+str(red_index))    
                    rpoints[red_index].append(indexfinger)
                    allpoints[universalindex].append(indexfinger)
                elif colorIndex == 3:
                    if yellow_index<0:
                        yellow_index=0
                    # print("yellow"+str(yellow_index))    
                    ypoints[yellow_index].append(indexfinger)
                    allpoints[universalindex].append(indexfinger)
                elif colorIndex==4:  
                    if white_index<0:
                        white_index=0
                    # print("white"+ str(white_index))    
                    wpoints[white_index].append(indexfinger)
                    allpoints[universalindex].append(indexfinger)
            else:
                annotation_Start=False        
        

            #selective erase
            if fingers==[0,1,1,1,0]:
                if allpoints:    
                    if(allpoints[-1]==[]):
                        allpoints.pop(-1)
                        universalindex-=1
                    if(bpoints[-1]==[]):
                        bpoints.pop(-1)  
                        blue_index-=1  
                    if(gpoints[-1]==[]):
                        gpoints.pop(-1)    
                        green_index-=1
                    if(rpoints[-1]==[]):
                        rpoints.pop(-1)    
                        red_index-=1
                    if(wpoints[-1]==[]):
                        wpoints.pop(-1)    
                        white_index-=1
                
                    if allpoints:
                        # print("inside all points")
                        point=allpoints[-1]
                        allpoints.pop(-1)
                        universalindex-=1
                        # print(point)
                        if  bpoints and point == bpoints[-1]:
                            # print("inside bluepoints")
                            bp=bpoints.pop(-1)
                            blue_index-=1
                            # print("blue point removed"+str(blue_index))
                            time.sleep(0.5)
                        if gpoints and point == gpoints[-1]:
                            # print("inside greenpoints")
                            gp=gpoints.pop(-1)
                            green_index-=1
                            # print("green point removed"+str(green_index))
                            time.sleep(0.5)
                        if rpoints and point == rpoints[-1]:
                            # print("inside redpoints")
                            rp=rpoints.pop(-1)
                            red_index-=1
                            # print("red point removed"+str(red_index))
                            time.sleep(0.5)
                        if ypoints and point in ypoints:
                            # print("inside yellowpoints")
                            yp=ypoints.pop(-1)
                            # print("yellow point removed"+str(yellow_index))
                            yellow_index-=1
                            time.sleep(0.5)
                        if wpoints and point in wpoints:
                            # print("inside whitepoints")
                            wp=wpoints.pop(-1)
                            # print("white point removed"+str(white_index))
                            white_index-=1
                            time.sleep(0.5)

            #complete erasing mode   
            if fingers==[0,1,1,1,1]:
                bpoints = [[]]
                gpoints = [[]]
                rpoints = [[]]
                ypoints = [[]]
                wpoints=  [[]]
                allpoints=[[]]

                blue_index = 0
                green_index = 0
                red_index = 0
                yellow_index = 0
                white_index=0
                universalindex=0

            #save image file in some folder
            if fingers==[0,1,0,0,1]:
                for i in range(len(points)-1):
                    for j in range(len(points[i])):
                        for k in range(1, len(points[i][j])):
                            if points[i][j][k - 1] is None or points[i][j][k] is None or len(points[i][j][k-1])==0 or len(points[i][j][k])==0:
                                continue
                            cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)
                image_to_save=Image.fromarray(paintWindow)
                file_name = 'image'+str(random.randint(0,1000))+'.jpeg'
                file_path = os.path.join("canvus_images", file_name)
                image_to_save.save(file_path)
                notification()
                # save_image(image_to_save)




            # #change thickness of color marker
            # if fingers==[1,1,0,0,0]:
            #     thickness+=2
            #     time.sleep(0.5)
                
        # points = [bpoints, gpoints, rpoints, ypoints,wpoints]
        for i in range(len(points)-1):
            for j in range(len(points[i])):
                for k in range(1, len(points[i][j])):
                    if points[i][j][k - 1] is None or points[i][j][k] is None or len(points[i][j][k-1])==0 or len(points[i][j][k])==0:
                        continue
                    # cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i],2,cv2.LINE_AA)
                    cv2.polylines(paintWindow,[ np.array([points[i][j][k - 1], points[i][j][k]])],False,colors[i],4,cv2.LINE_AA)
       
        # ksize = 5
        # filtered_canvas = cv2.medianBlur(paintWindow, ksize)



        cv2.imshow("Image",img)
        cv2.imshow("paintwindow",paintWindow)



        key=cv2.waitKey(1)
        if key==ord('q') or key==ord('Q'):
            break
    cv2.destroyAllWindows()     

