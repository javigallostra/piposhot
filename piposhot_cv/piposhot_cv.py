# CV
import cv2
# Pi Camera
from picamera import PiCamera
# Video analysis libraries
from numpy import sqrt
from imutils import resize
from imutils import is_cv2
# Time
from time import sleep

class piposhot_cv:

	def __init__(self, display=True):
		# Initialize variables
		self.cam = PiCamera()
		self.pic_count = 0
		self.vid_count = 0
		self.display = display
		self.found_hp = []

	def setup(self):
		# Take picture
		pic_name = self._takePicture()
		# Find target data
		x_pix,y_pix,size_pix = self._findTarget(pic_name)

	def _takePicture(self):
		if (self.display):
			print("[CAM]: Taking picture...")
		self.cam.start_preview()
		sleep(5)
		pic_name = 'image' + str(self.pic_count)
		self.cam.capture('./' + pic_name + '.jpg')
		self.cam.stop_preview()
		if (self.display):
			print("[CAM]: " + pic_name + ".jpg saved.")
		#self.pic_count += 1
		return pic_name

	def _findTarget(self, th, pic_name='image0'):
		if (self.display):
			print("[CAM]: Loading " + pic_name + ".jpg...")
		# Load image and convert to grayscale
		img = cv2.imread('./' + pic_name + '.jpg')
		if (self.display):
			print("[CAM]: Analyzing picture...")
		gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		# Binarize image
		ret,thresh = cv2.threshold(gray_img,th,255,cv2.THRESH_BINARY)
		# Find shapes
		thresh,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
		# Calculate moments of target
		M = cv2.moments(contours[1])
		# Get target center coordinates
		cX = int(M["m10"]/M["m00"])
		cY = int(M["m01"]/M["m00"])
		if (self.display):
			print("[CAM]: Found target center (" + str(cX) + "," + str(cY) + ").")
		# Get target size
		x,y,w,h = cv2.boundingRect(contours[1])
		size = (w + h)/2
		if (self.display):
			print("[CAM]: Found target size " + str(size) + ".")
		# Display results
		cv2.drawContours(img,contours,1,(0,255,0),3)
		cv2.circle(img,(cX,cY),5,(255,0,0),-1)
		cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
		cv2.imwrite("target.jpg",img)
		cv2.imshow("Image",img)
		# Wait for termination
		cv2.waitKey(0)

	def _recordVideo(self,t=2):
		if (self.display):
			print("[CAM]: Recording video for " + str(t) + "seconds ...")
		self.cam.start_preview()
		vid_name = "vid" + str(self.vid_count)
		self.cam.start_recording("./" + vid_name + ".h264")
		sleep(t)
		self.cam.stop_recording()
		self.cam.stop_preview()
		if (self.display):
			print("[CAM]: " + vid_name +".h264 saved.")
		#self.vid_count += 1
		return vid_name

	def _findHitPoint(self,vid_name='vid0'):
		if (self.display):
			print("[CAM]: Loading video " + vid_name + ".h264...")
		# Load video
		vs = cv2.VideoCapture(vid_name + ".h264")
		sleep(2)
		# Initialize loop variables
		min_radius = 1000
		hitpoint = (0,0)
		orangeLower = (10,114,102)
		orangeUpper = (17,255,255)
		points = []
		line_buffer = 10
		im = 0
		if (self.display):
			print("[CAM]: Analyzing video...")
		# Frame loop
		while True:
			# Grab next frame
			frame = vs.read()
			frame = frame[1]
			# Check for end of video
			if (frame is None):
				break
			else:
				# Resize the frame, blur it and convert to HSV
				frame = resize(frame,width=600)
				frame_blurred = cv2.GaussianBlur(frame,(5,5),0)
				frame_hsv = cv2.cvtColor(frame_blurred,cv2.COLOR_BGR2HSV)
				# Create a mask for the color orange and perform
				# a series of erotions and dilations to remove
				# small noisy blobs in the mask
				mask = cv2.inRange(frame_hsv,orangeLower,orangeUpper)
				mask = cv2.erode(mask,None,iterations=2)
				mask = cv2.dilate(mask,None,iterations=2)
				# Find contours in the mask and initialize
				# the value of the ball center
				contours = cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
				contours = contours [0] if is_cv2() else contours[1]
				center = None
				# Proceed if at least one contour was found
				if (len(contours) > 0):
					# Find the largest contour
					contour = max(contours,key=cv2.contourArea)
					# Find the contour center and enclosing circle
					((x,y),radius) = cv2.minEnclosingCircle(contour)
					M = cv2.moments(contour)
					center = (int(M["m10"]/M["m00"]),int(M["m01"]/M["m00"]))
					# Proceed if the radius is larger than 2
					if (radius > 2):
						# Add the circle and center to the current frame
						if (self.display):
							cv2.circle(frame,(int(x),int(y)),int(radius),(0,255,255),2)
							cv2.circle(frame,center,5,(0,0,255),-1)
							# Update the hitpoint
							if (radius < min_radius):
								min_radius = radius
								hitpoint = center
				# Add current hitpoint to frame
				if (self.display):
					cv2.circle(frame,hitpoint,10,(0,0,0),-1)
				# Add found center to trajectory points
				points.append(center)
				# Draw the trajectory on the frame
				if (self.display):
					for i in range(len(points)-1,0,-1):
						# Ignore non-valid points
						if (points[i] == None or points[i-1] == None):
							continue
						# Draw each segment with decreasing thickness
						else:
							thickness = int(sqrt(line_buffer/float(i+1)) * 2.5)
							cv2.line(frame,points[i-1],points[i],(0,0,255),thickness)
				# Show the current frame
				if (self.display):
					cv2.imshow("Frame",frame)
					# Check for keypress
					key = cv2.waitKey(1) & 0xFF
					cv2.imwrite("frame"+str(im)+".jpg",frame)
					im += 1
					# If 'q' has been pressed, stop the loop
					if (key == ord('q')):
						break
		# Loop ended, release the video
		vs.release()
		# Close windows
		if (self.display):
			cv2.destroyAllWindows()
			print("[CAM]: Found hitpoint (" + str(hitpoint[0]) + "," + str(hitpoint[1]) + ").")
		# Return the found hitpoint
		self.found_hp.append(hitpoint)
		return hitpoint
