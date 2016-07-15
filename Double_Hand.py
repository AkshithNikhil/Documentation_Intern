import cv2
import numpy as np
import freenect
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
    var1 = np.reshape(raw_depth,(1,m*n))
    var1 = np.asarray(var1)
    low_ind = var1 < 300 #Eliminating Depth Values below 300
    high_ind = var1 > 700 #Eliminating Depth Values below 700
    th_hand[low_ind] = 0
    th_hand[high_ind] = 0
    th_hand = np.reshape(th_hand,(m,n))
    #print th_hand.dtype
    th_hand = th_hand.astype('uint8')
    if(np.int(th_hand.sum()) <= 50):
        continue

    B = np.zeros((m,n))
    contours,hierarchy = cv2.findContours(th_hand, 1, 2)
    areas = [cv2.contourArea(cnt) for cnt in contours]
    #print areas.dtype
    max_index = np.argmax(areas) #Maximum Area
    #max_index = max(areas)
    areas[max_index] = 0  
    sec_max_index = np.argmax(areas) #Second Maximum Area 
    cnt1 = contours[max_index] #Finding first hand
    cnt2 = contours[sec_max_index] #Second Hand
    #print cv2.contourArea(cnt2)
    #max_area = cv2.contourArea(cnt)
    #sec_max_area = 0
    #sec_max_area = 0
    #var_area = 0
    #if(len(contours) > 1):
    #    for i in range(0,len(contours)):
    #        var_area = cv2.contourArea(contours[i])
    #        if(var_area > sec_max_area and var_area < max_area):
    #            sec_max_area = var_area
    #            sec_max_ind = i
    #            #print i
    #    cnt2 = contours[sec_max_ind]          
    #    cv2.drawContours(B,[cnt2],0,1,2)

    cv2.drawContours(B,[cnt1],0,1,2)
    cv2.drawContours(B,[cnt2],0,1,2)
    
    hull1 = cv2.convexHull(cnt1,returnPoints = False) #Convex Hull for First Hand
    defects1 = cv2.convexityDefects(cnt1,hull1) #Convex Defects
    [m1,n1,l1] = defects1.shape

    th = 7500
    count1 = 0
    count2 = 0
    ind1 = []
    ind2 = []

    for k in range(0,m1):
        if(defects1[k,0,3] > th):
            count1 = count1 + 1
            ind1.append(k)

    ind1 = np.array(ind1)

    for i in range(0,count1):
        cv2.circle(B,(cnt1[defects1[ind1[i],0,0],0,0],cnt1[defects1[ind1[i],0,0],0,1]),10,1,-1)
        #print i
        if ( i == count1-1):
            #print i
            cv2.circle(B,(cnt1[defects1[ind1[i],0,1],0,0],cnt1[defects1[ind1[i],0,1],0,1]),10,1,-1)
            
    if(cv2.contourArea(cnt2) > 100):
        hull2 = cv2.convexHull(cnt2,returnPoints = False) #Hull for Second Hand
        defects2 = cv2.convexityDefects(cnt2,hull2) #Defects for Second Hand
        [m2,n2,l2] = defects2.shape
        for k in range(0,m2):
            if(defects2[k,0,3] > th):
                count2 = count2 + 1
                ind2.append(k)

        ind2 = np.array(ind2)

        for i in range(0,count2):
            cv2.circle(B,(cnt2[defects2[ind2[i],0,0],0,0],cnt2[defects2[ind2[i],0,0],0,1]),10,1,-1)
            #print i
            if ( i == count2-1):
                #print i
                cv2.circle(B,(cnt2[defects2[ind2[i],0,1],0,0],cnt2[defects2[ind2[i],0,1],0,1]),10,1,-1)
    
    
    cv2.imshow('depth',B)
    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        #print B.dtype
        break
cv2.destroyAllWindows()
