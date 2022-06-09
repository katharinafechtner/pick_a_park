import cv2
import numpy as np
import matplotlib.image as img

'''
Filters colors and masks them according to
https://www.geeksforgeeks.org/filter-color-with-opencv/
'''

def colorfilter(dirname):

    path = dirname + "\\static\\screenshots\\screenshot.jpg"

    # Load picture and convert RGB color space of image to HSV color space
    pic = img.imread(r"{}".format(path))
    hsv = cv2.cvtColor(pic, cv2.COLOR_RGB2HSV)

    # Define threshold values for color detection
    lower_green = np.array([40, 0, 0])
    upper_green = np.array([70, 255, 255])

    # preparing the mask to overlay
    mask = cv2.inRange(hsv, lower_green, upper_green)
        
    # The black region in the mask has the value of 0,
    # so when multiplied with original image removes all regions for specified color
    result = cv2.bitwise_and(pic, pic, mask = mask)

    # Store number of pixels that match masked area
    pixels = cv2.countNonZero(mask)
    # pixels = len(np.column_stack(np.where(thresh > 0)))

    # Compute area for mask and ratio in relation to total picture
    image_area = pic.shape[0] * pic.shape[1]
    area_ratio = (pixels / image_area) * 100


    ''' Blob detection
    https://learnopencv.com/blob-detection-using-opencv-python-c/
    '''
    #im = cv2.cvtColor(result, cv2.COLOR_RGB2GRAY)
    im = cv2.bitwise_not(mask)

    # Setup SimpleBlobDetector parameters.
    params = cv2.SimpleBlobDetector_Params()

    # Filter by Area
    params.filterByArea = True
    params.minArea = 500
    params.maxArea = 100000000

    # Turn off unused parameters explicitly
    params.filterByCircularity = False
    params.filterByColor = False
    params.filterByConvexity = False
    params.filterByInertia = False

    # Create a detector with the parameters
    ver = (cv2.__version__).split('.')
    if int(ver[0]) < 3:
        detector = cv2.SimpleBlobDetector(params)
    else :
        detector = cv2.SimpleBlobDetector_create(params)

    # Set up the detector with default parameters.
    #detector = cv2.SimpleBlobDetector_create()

    # Detect blobs.
    keypoints = detector.detect(im)

    # Draw detected blobs as red circles.
    # cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS ensures the size of the circle corresponds to the size of blob
    im_with_keypoints = cv2.drawKeypoints(pic, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    mask_with_keypoints = cv2.drawKeypoints(mask, keypoints, np.array([]), (0,0,255), cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

    ''' Save image '''
    filename = dirname + "\\static\\screenshots\\analysis.jpg"
    filename2 = dirname + "\\static\\screenshots\\mask.jpg"
    cv2.imwrite(filename, im_with_keypoints)
    cv2.imwrite(filename2, mask_with_keypoints)

    ''' Plot images '''

    # Show keypoints
    #cv2.imshow("Keypoints", im_with_keypoints)
    #cv2.imshow("image", im)

    # Show original, mask and result
    #cv2.imshow('picture', pic)
    #cv2.imshow('mask', mask)
    # cv2.imshow('result', result)

    #cv2.waitKey(0)
    #cv2.destroyAllWindows()