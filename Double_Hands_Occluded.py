import cv2
import freenect
import numpy as np

# Getting Depth data
def get_depth(): 
    array,_ = freenect.sync_get_depth()
    #array = array.astype(np.uint8)
    return array
#Getting RGB data
def get_rgb():
    array,_ = freenect.sync_get_video()
    return array
while(True):
    raw_depth = get_depth()
    [m,n] = raw_depth.shape
    th_hand = np.ones((1,m*n))
    th_hand1 = np.ones((1,m*n))
    var1 = np.reshape(raw_depth,(1,m*n))
    var1 = np.asarray(var1)
    low_ind = var1 < 300 #Eliminating Depth Values below 300
    high_ind = var1 > 700 #Eliminating Depth Values below 700
    var1[low_ind] = 1000 #Changind Detth values below 300 to 1000 to get minimum depth in range 300-700
    min_depth_ind = np.argmin(var1)
    min_depth = var1[0,min_depth_ind] #Getting minimum depth in range 300-700
    th_hand[low_ind] = 0
    th_hand[high_ind] = 0
    th_hand = np.reshape(th_hand,(m,n))
    th_hand = th_hand.astype('uint8')
    if(min_depth > 650):
        min_depth = 650

    low2_ind = var1 < min_depth
    high2_ind = var1 > min_depth + 50
    th_hand1[low2_ind] = 0 #Eliminating depth values below min_depth
    th_hand1[high2_ind] = 0 #Taking range of 50 to remove occlusions
    th_hand1 = np.reshape(th_hand1,(m,n))
    th_hand1 = th_hand1.astype('uint8')
    
    if(np.int(th_hand.sum()) <= 100):
        print 'NONE'
        continue

    B = np.zeros((m,n))
    contours,hierarchy = cv2.findContours(th_hand, 1, 2) 
    contours1,hierarchy = cv2.findContours(th_hand1, 1, 2) 
    areas = [cv2.contourArea(cnt) for cnt in contours]
    areas1 = [cv2.contourArea(vcnt) for vcnt in contours1]

    th = 7500
    count1 = 0
    count2 = 0
    ind1 = []
    ind2 = []
    
    if(len(contours1) > 0):
       
        max_index = np.argmax(areas1) #Maximum Area
        #max_index1 = np.argmax(areas1)
        cnt1 = contours1[max_index] #Finding first hand
        if(cv2.contourArea(cnt1) > 500):
            
            cv2.drawContours(B,[cnt1],0,1,2)

            hull1 = cv2.convexHull(cnt1,returnPoints = False) #Convex hull
            [mm,nn] = hull1.shape 
            if(mm >= 3):
                defects1 = cv2.convexityDefects(cnt1,hull1) #Convex Defects
                [m1,n1,l1] = defects1.shape



                for k in range(0,m1):
                    if(defects1[k,0,3] > th):
                        count1 = count1 + 1
                        ind1.append(k)

                ind1 = np.array(ind1)
                #Drawing Extrimities
                for i in range(0,count1): 
                    cv2.circle(B,(cnt1[defects1[ind1[i],0,0],0,0],cnt1[defects1[ind1[i],0,0],0,1]),10,1,-1)
        #print i
                    if ( i == count1-1):
            #print i
                        cv2.circle(B,(cnt1[defects1[ind1[i],0,1],0,0],cnt1[defects1[ind1[i],0,1],0,1]),10,1,-1)
            else:
                continue
    #If Two Hands
    if(len(contours) > 1):
        max_index = np.argmax(areas)
        areas[max_index] = 0
        sec_max_index = np.argmax(areas) #Second large contour
        cnt2 = contours[sec_max_index]
        if(cv2.contourArea(cnt2) > 500):
            cv2.drawContours(B,[cnt2],0,1,2)

            hull2 = cv2.convexHull(cnt2,returnPoints = False) #Convex HUll
            [mmm,nnn] = hull2.shape
            if(mmm >= 3):
                
                defects2 = cv2.convexityDefects(cnt2,hull2) #Convexity Defects
                [m2,n2,l2] = defects2.shape
                for k in range(0,m2):
                    if(defects2[k,0,3] > th):
                        count2 = count2 + 1
                        ind2.append(k)
                ind2 = np.array(ind2)
                #Drawing Extrimities
                for i in range(0,count2):
                    cv2.circle(B,(cnt2[defects2[ind2[i],0,0],0,0],cnt2[defects2[ind2[i],0,0],0,1]),10,1,-1)
                    #print i
                    if ( i == count2-1):
                        #print i
                        cv2.circle(B,(cnt2[defects2[ind2[i],0,1],0,0],cnt2[defects2[ind2[i],0,1],0,1]),10,1,-1)

                print 'TWO'
                cv2.imshow('depth',B)
                k = cv2.waitKey(5) & 0xFF
                if k == 27:
               # print hull2.rows()
                    break
                continue
            else:
                continue
        

    


    print 'ONE'
    cv2.imshow('depth',B)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
       # print hull1.rows()
        break
cv2.destroyAllWindows()









