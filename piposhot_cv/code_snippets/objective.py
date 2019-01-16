import cv2
from time import sleep
#vidcap = cv2.VideoCapture('shooting.h264')
#success,image = vidcap.read()
#count = 0
#while  success:
  #cv2.imwrite("frame%d.jpg" % count, image)     # save frame as JPEG file      
  #success,image = vidcap.read()
  #print('Read a new frame: ', success)
  #count +=1
  #if count > 0:
  #	break
  #else:
	#continue
  #break

img = cv2.imread('./image0.jpg')
cv2.imshow('Original',img)
# convert image to grayscale image
gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imshow('Gray', gray_image)
# convert the grayscale image to binary image

ret,thresh = cv2.threshold(gray_image,65,255,cv2.THRESH_BINARY)
thresh = cv2.erode(thresh,None,iterations=5)
cv2.imshow("bin",thresh)
cv2.waitKey(0)
thresh, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img, contours, 1, (0,255,0), 3)
# calculate moments of binary image
M = cv2.moments(contours[1])
 
# calculate x,y coordinate of center
cX = int(M["m10"] / M["m00"])
cY = int(M["m01"] / M["m00"])
 
# put text and highlight the center
cv2.circle(img, (cX, cY), 5, (0, 255, 0), -1)
cv2.putText(img, "Objective", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
cv2.imwrite("target.jpg",img) 
# display the image
cv2.imshow("Image", img)
cv2.waitKey(0)

