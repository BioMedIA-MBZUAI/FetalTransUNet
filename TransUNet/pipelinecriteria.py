# python3
# -*- coding: utf-8 -*-
# Author: Sevim Cengiz
# All calculations are double checked.
# June 7, Asmus2022, Transunet
# Credit: https://doi.org/10.1007/978-3-031-16902-1_17
# ASMUS 2022: Cengiz, S., Hamdi, I., Yaqub, M. (2022).
# Automatic Quality Assessment of First Trimester Crown-Rump-Length Ultrasound Images. 
# In: Aylward, S., Noble, J.A., Hu, Y., Lee, SL., Baum, Z., Min, Z. (eds) 
# Simplifying Medical Ultrasound. ASMUS 2022. Lecture Notes in Computer Science, vol 13565. Springer, Cham.
  
import sys
predictionpath = sys.argv[1]  

def pipelinecriteria(predictionpath):

    import glob, os
    import nibabel as nib
    import matplotlib.pyplot as plt
    import numpy as np
    import cv2
    import math
    import pandas as pd

    L_filename=[]
    L_CRLdistance=[]
    L_neutralpositionangle=[]
    L_fetalpalateexist=[]
    L_magnification=[]
    L_CRLhorizontalangle=[]
    L_rightcaliperblackpixels=[]
    L_leftcaliperblackpixels=[]
    L_fetalfacedirection=[]
    L_gap=[]


    os.chdir(predictionpath)
    #predictionpath='/Users/sevim/Downloads/predictions/'

    for file in sorted(glob.glob("*pred.nii.gz")):
        L_filename.append(file)
        #print(file)
        img= nib.load(file)
        img_np = img.get_data()
        slice = np.squeeze(img_np)
        #plt.imshow(slice[:,:,1])
        
        image_rotat = cv2.rotate(slice[:,:,1], cv2.ROTATE_90_CLOCKWISE) #Only our images are rotated 
        image_rotate = cv2.flip(image_rotat, 1) #
       # plt.imshow(image_rotate)
        
        dim = (925, 663)
      
    # resize image
        image_rotated = cv2.resize(image_rotate, dim, interpolation = cv2.INTER_NEAREST) #it is for the resize from 512,512 to 925,625.
      
        
        head = (image_rotated==1)
        plt.imshow(head)
        
        body = (image_rotated==2)
        plt.imshow(body)
        
        gap = (image_rotated==4)
        valnonzero_gap=np.count_nonzero(gap)
                     
        L_gap.append(valnonzero_gap)
        
        
    #CRL Measurement
        
        CRLseg= (1*head)+(1*body)
        CRLseg = np.array(CRLseg).astype('uint16')
        plt.imshow(CRLseg)
        kernel = np.ones((3,3),np.uint8)
        borderall = cv2.morphologyEx(CRLseg, cv2.MORPH_GRADIENT, kernel)
        plt.imshow(borderall)
        yall , xall = borderall.shape
       
        maxdistance=np.zeros((1,1))
        
        coordx=[]
        coordy=[]
        for y in range(borderall.shape[0]):
            for x in range(borderall.shape[1]):

               
                if (borderall[y,x]==1) or (borderall[y,x]==2):
                    coordx.append(x)
                    coordy.append(y)
                    
        
        for i in range(1,len(coordx)):
            x1=coordx[i]
            y1=coordy[i]
            
            for m in range(i,len(coordx)):
                x2=coordx[m]
                y2=coordy[m]
                distanc=((x2-x1)**2)+((y2-y1)**2)
                distance=math.sqrt(distanc)
                
                if distance > maxdistance:
                    maxdistance = distance
                    mmy2 = y1
                    mmy1 = y2
                    mmx2 = x1
                    mmx1 = x2
       # print([maxdistance, mmx1, mmy1, mmx2, mmy2])
        
        if mmx2<mmx1:
            my2 = mmy2
            my1 = mmy1
            mx2 = mmx2
            mx1 = mmx1
        else:
            my2 = mmy1
            my1 = mmy2
            mx1 = mmx2
            mx2 = mmx1
        
        L_CRLdistance.append(maxdistance)
       
       # the coord mx1 should be on the right side, which represents right caliper
       # the coord mx2 should be on the left side, which represents left caliper
       


                      
    # Find fetal palate existence
        fetalpalate = (image_rotated==3)
        #plt.imshow(fetalpalate)
        palateexist=0
        
        for k in range(fetalpalate.shape[0]):
            for l in range(fetalpalate.shape[1]):

               
                if (fetalpalate[k,l]*1)==1: 
                    
                    palateexist=1
                    break
        
        #print(palateexist)
        
        L_fetalpalateexist.append(palateexist)

    # Magnificaion
     
        if abs(mx1-mx2) > (xall*0.6):
            magnification = 1
            #print('1')
        else: 
            magnification = 0
            #print('o')
            
        L_magnification.append(magnification)


    # CRL axis to the horizontal

        CRLanglepos = (abs(my1-my2))/(abs(mx1-mx2))
        CRLposrad = math.atan(CRLanglepos) 
        CRLangleposdegree = math.degrees(CRLposrad)
        
        L_CRLhorizontalangle.append(CRLangleposdegree)
        
        
        
    # Right and left caliper definition
        gtfn=file.split("_pred")[0]
        gtpath=predictionpath+gtfn+'_img.nii.gz'
        gimg= nib.load(gtpath)
        gimg_np = gimg.get_data()
        gtim = np.squeeze(gimg_np)
        gtimg=gtim[:,:,1]
        
        
        
        gtimage_rotat = cv2.rotate(gtimg, cv2.ROTATE_90_CLOCKWISE) #
        gtimage_rotate = cv2.flip(gtimage_rotat, 1) #

        gtimage_rotatedd = cv2.resize(gtimage_rotate, dim, interpolation = cv2.INTER_NEAREST) #it is for the resize from 512,512 to 925,625.

        #plt.imshow(gtimage_rotatedd)       
         
                
    # Right caliper definition
                
        if (mx1+20)>xall and (my1+10)>yall: 
            #print('r-111')
            rect_area_r=gtimage_rotatedd[(my1-10):yall,mx1:xall]
                                  
        else: 
            #print('r-222')
        
            rect_area_r=gtimage_rotatedd[(my1-10):(my1+10),mx1:(mx1+20)]
        
        plt.imshow(rect_area_r)
                     
        
        valnonzero_r=np.count_nonzero(rect_area_r)
                     
        L_rightcaliperblackpixels.append(valnonzero_r)

                    
    # Left caliper definition
                
        if mx2>10 and my2>10: 
            #print('l-111')
            rect_area_l=gtimage_rotatedd[(my2-10):(my2+10),mx2:(mx2+20)]
           
        else: 
            #print('l-222')
            rect_area_l=gtimage_rotatedd[(my2-10):my2+10,mx2:mx2+20]
        
        plt.imshow(rect_area_l)                            
        valnonzero_l=np.count_nonzero(rect_area_l)
                     
        L_leftcaliperblackpixels.append(valnonzero_l)    

        
    # Middle point finder between head and body

        headbor = np.array(head).astype('uint16')
        headborderall = cv2.morphologyEx(headbor, cv2.MORPH_GRADIENT, kernel)
        plt.imshow(headborderall)
        
        locationsx = []
        locationsy = []
        for y in range(headborderall.shape[0]):
            for x in range(headborderall.shape[1]):

               
                if (headborderall[y,x]==1):
                    locationsx.append(x)
                    locationsy.append(y)
                    
        keepheadlocx =[]
        keepheadlocy = []
        for count, value in enumerate(locationsx):
            pixval = (body[locationsy[count],locationsx[count]+1])*1
            if  pixval == 1:
                keepheadlocx.append(locationsx[count])
                keepheadlocy.append(locationsy[count])
                
        if keepheadlocx:
                
                mx3 = int((min(keepheadlocx)+max(keepheadlocx))/2)
                my3 = int((min(keepheadlocy)+max(keepheadlocy))/2)
        
                image=image_rotated
                window_name = 'Image'
                start_point1 = (mx2,my2)
                end_point1 = (mx3, my3)
                color= (0, 255, 0)
                thickness = 1
                image = cv2.line(image, start_point1, end_point1, color, thickness)
                
                start_point2 = (mx3,my3)
                end_point2 = (mx1, my1)
                image = cv2.line(image, start_point2, end_point2, color, thickness)
                
                start_point3 = (mx2,my2)
                end_point3 = (mx1, my1)
                image = cv2.line(image, start_point3, end_point3, color, thickness)
                
    # Displaying the image 
                plt.imshow(image)
                vis_im = cv2.addWeighted(gtimage_rotatedd[:,:], 0.7, image, 0.6,0)

    # Angle finder between head and body using middle point

                a=math.sqrt((my1-my2)**2+(mx1-mx2)**2) 
                b=math.sqrt((my2-my3)**2+(mx2-mx3)**2)
                c=math.sqrt((my1-my3)**2+(mx1-mx3)**2)

                def angle (a, b, c):
                    return math.degrees(math.acos((c**2 - b**2 - a**2)/(-2.0 * a * b)))

                #angA = angle(a,b,c)
                Final_angle= angle(b,c,a)
                #angC = angle(c,a,b)
                
                L_neutralpositionangle.append(str(round(Final_angle,2)))
                
                savefolder=predictionpath+'/segs_w_lines'
                isExist = os.path.exists(savefolder)
                if not isExist:
                    os.makedirs(savefolder)
                fnsave= savefolder+'/'+gtfn+'_'+str(round(Final_angle,2))+'.png'
                plt.imsave(fnsave,np.array(vis_im))
                

                
                           
    # Fetal face direction (up/down)
                
                #Shifting middle point between head and body to (0,0) at the coordinate system, and shifting x1, x2, y1, y2 points to their respective location at the coordinate system
                shifted_mx3 = mx3-mx3
                shifted_my3 = (yall-my3)-(yall-my3)
                
                shifted_mx1 = mx1-mx3
                shifted_my1 = (yall-my1)-(yall-my3)
                
                shifted_mx2 = mx2-mx3
                shifted_my2 = (yall-my2)-(yall-my3)#yall-my2
                
                slope = (shifted_my1-shifted_my2)/(shifted_mx1-shifted_mx2)
                
                #The equation of a line  (y-y1)=m*(x-x1)
                
                eqq_y=shifted_my1-(slope*shifted_mx1)
                #eq_y=0
                #eq_x=0
                if eqq_y>0:#(eq_y - shifted_my2 + (slope*shifted_mx2))/slope>eq_x:
                    facedirec='up' #it means the face direction is up
                else:
                    facedirec='down' #it means the face direction is down
                    
                L_fetalfacedirection.append(facedirec)
            
        else:
            L_neutralpositionangle.append('NotDefined')
            L_fetalfacedirection.append('NotDefined')
                
                

                    
    # Creating a list to keep criteria 

    df = pd.DataFrame(list(zip(L_filename,L_CRLdistance,L_neutralpositionangle,L_gap,L_fetalpalateexist,L_magnification,
                                           L_CRLhorizontalangle,L_rightcaliperblackpixels,L_leftcaliperblackpixels,L_fetalfacedirection)),columns=['Filename','CRLDistance','NeutralpositionAngle','GapBheadBody','Fetalpalateexist','Magnification','CRLhorizontalAngle','RightCaliperBlackpixels','LeftCaliperBlackpixels','FetalFacedirection'])
                
    df.to_csv(predictionpath+'/AllCriteriaList.csv')
                
                
              

pipelinecriteria(predictionpath)                
                
                
        
                


                

        



                
        
                       
        
        

