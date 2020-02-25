# Import libraries
import argparse
import cv2
import imutils
import numpy as np
import time


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required=True,
	help="path to input video")
ap.add_argument("-o", "--output", required=True,
	help="path to output video")
args = vars(ap.parse_args())


# initialize the video stream, pointer to output video file, and frame dimensions
vs = cv2.VideoCapture(args["input"])
writer = None
(W, H) = (None, None)

# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video stream or file")


# try to determine the total number of frames in the video file
try:
	prop = cv2.cv.CV_CAP_PROP_FRAME_COUNT if imutils.is_cv2() \
		else cv2.CAP_PROP_FRAME_COUNT
	total = int(vs.get(prop))
	print("[INFO] {} total frames in video".format(total))

# an error occurred while trying to determine the total
# number of frames in the video file
except:
	print("[INFO] could not determine # of frames in video")
	print("[INFO] no approx. completion time can be provided")
	total = -1

# loop over frames from the video file stream
#while(cap.isOpened()):
while True:	

	# read the next frame from the file
	(grabbed, frame) = vs.read()

	# if the frame was not grabbed, then we have reached the end of the stream
	if not grabbed:
		break
    
	# if the frame dimensions are empty, grab them
	if W is None or H is None:
		(H, W) = frame.shape[:2]    
    
	# Load the Logo image with Alpha channel
	LogoPNG = cv2.imread("Logo.png",-1)
  
	# Resize the image to fit over the region of interes
	LogoPNG = cv2.resize(LogoPNG, (300,100))
	
	# Separate the Color and alpha channels
	LogoBGR = LogoPNG[:,:,0:3]
	LogoMask1 = LogosPNG[:,:,3]
	
	# Make the dimensions of the mask same as the input image.
	# Since Video Image is a 3-channel image, we create a 3 channel image for the mask
	LogoMask = cv2.merge((LogoMask1,LogoMask1,LogoMask1))
	
	# Make the values [0,1] since we are using arithmetic operations
	LogoMask = np.uint8(LogoMask/255)
	
	# Make a copy
	FrameWithLogoArithmetic = frame.copy()
	
	# Get the space region for logo in the video-frame
	spaceROI= FrameWithLogoArithmetic[20:120,20:320]
	
	# Use the mask to create the masked space region
	maskedSpace = cv2.multiply(spaceROI,(1-  LogoMask ))
	
	# Use the mask to create the masked Logo region
	maskedLogo = cv2.multiply(LogoBGR,LogoMask)
	
	# Combine the LOgo in the Space Region to get the augmented image
	spaceRoiFinal = cv2.add(maskedSpace, maskedLogo)
	
	# Replace the space ROI with the output from the previous section
	frameWithLogoArithmetic[20:120,20:320]=spaceRoiFinal
	
	#Return to the original variable
	frame = frameWithLogoArithmetic
	
	# check if the video writer is None
	if writer is None:
		# initialize our video writer
		fourcc = cv2.VideoWriter_fourcc(*"MJPG")
		writer = cv2.VideoWriter(args["output"], fourcc, 30,
					 (frame.shape[1], frame.shape[0]), True)
		
		# some information on processing single frame
		if total > 0:
			elap = (end - start)
			print("[INFO] single frame took {:.4f} seconds".format(elap))
			print("[INFO] estimated total time to finish: {:.4f}".format(elap * total))
			
	# write the output frame to disk
	writer.write(frame)
	
	# Identify if 'ESC' is pressed or not
	if(0xFF == 27):
		break

# release the file pointers
print("[INFO] cleaning up...")
writer.release()
vs.release()
