""" Camera Obscura - Post-processing
AUTHOR: VISHWA MUDIGONDA
CLASS: COMPUTATIONAL PHOTOGRAPHY
DATE: 1/28/2020

This file has a number of functions that you need to fill out in order to
complete the assignment. Please write the appropriate code, following the
instructions on which functions you may or may not use.

Notes
-----
You are only allowed to use cv2.imread, c2.imwrite and cv2.copyMakeBorder from 
cv2 library. You should implement convolution on your own.
GENERAL RULES:
    1. DO NOT INCLUDE code that saves, shows, displays, writes the image that
    you are being passed in. Do that on your own if you need to save the images
    but these functions should NOT save the image to disk.
    2. DO NOT import any other libraries aside from those that we provide.
    You should be able to complete the assignment with the given libraries
    (and in many cases without them).
    3. DO NOT change the format of this file. You may NOT change function
    type signatures (not even named parameters with defaults). You may add
    additional code to this file at your discretion, however it is your
    responsibility to ensure that the autograder accepts your submission.
    4. This file has only been tested in the course virtual environment.
    You are responsible for ensuring that your code executes properly in the
    virtual machine environment, and that any changes you make outside the
    areas annotated for student code do not impact your performance on the
    autograder system.
"""
import numpy as np
import cv2

def applyConvolution(image, filter):
    """Apply convolution operation on image with the filter provided. 
    Pad the image with cv2.copyMakeBorder and cv2.BORDER_REPLICATE to get an output image of the right size
    Parameters
    ----------
    image : numpy.ndarray
        A numpy array of dimensions (HxWx3) and type np.uint8
    filter: numpy.ndarray
        A numpy array of dimensions (N,M) and type np.float64
    Returns
    -------
    output : numpy.ndarray
        A numpy array of dimensions (HxWx3) and type np.uint8
    """
    # WRITE YOUR CODE HERE.
    #https://books.google.com/books?id=bQ4dGTfo8-sC&pg=PA117&lpg=PA117&dq=%5B%5B0,-1,0%5D,%5B-1,5,-1%5D,%5B0,-1,0%5D%5D+sharpen+image&source=bl&ots=YxTBmisy_Y&sig=ACfU3U10v1dp24xHHTjBH5jGudhb1_qwSA&hl=en&sa=X&ved=2ahUKEwiN-vG15Z_oAhVkmeAKHd5dBukQ6AEwA3oECAYQAQ#v=onepage&q=%5B%5B0%2C-1%2C0%5D%2C%5B-1%2C5%2C-1%5D%2C%5B0%2C-1%2C0%5D%5D%20sharpen%20image&f=false
    background_color = [0,0,0]
    image = cv2.copyMakeBorder(image,15,15,15,15,cv2.BORDER_REPLICATE, value=background_color)

    imgWidth, imgHeight = image.shape[1], image.shape[0]
    filterW, filterH = filter.shape[1], filter.shape[0]
    imgShape = image.shape[2]
    completeImage = np.zeros((imgHeight,imgWidth,imgShape), dtype=np.uint8)
    
    for y in range(imgHeight):
        for x in range(imgWidth):
            for color in range(imgShape):
                if(x == 0 or y == 0 or y >= imgHeight-1 or x >= imgWidth-1):
                    r = 0
                elif ((x < (imgWidth-2)) and (y < (imgHeight-2))):
                    focusedMatrix = [[image[y-1,x-1,color], image[y-1,x,color], image[y-1,x+1,color]], 
                                    [image[y,x-1,color], image[y,x,color], image[y,x+1,color]], 
                                    [image[y+1,x-1,color], image[y+1,x,color], image[y+1,x+1,color]]]
                    pixelValue = ((focusedMatrix*filter).sum())
                    if(pixelValue > 255):
                        pixelValue = 255
                    completeImage[y][x][color] = pixelValue
    return completeImage
                
    raise NotImplementedError

def applyMedianFilter(image, filterdimensions):
    """Apply median filter on image after padding it with zeros around the edges using cv2.copyMakeBorder
    Parameters
    ----------
    image : numpy.ndarray
        A numpy array of dimensions (HxWx3) and type np.uint8
    filterdimensions: list<int>
        List of length 2 that represents the filter size M x N
    Returns
    -------
    output : numpy.ndarray
        A numpy array of dimensions (HxWx3) and type np.uint8
    """
    M, N = filterdimensions

# WRITE YOUR CODE HERE.
    background_color = [0,0,0]
    image = cv2.copyMakeBorder(image,15,15,15,15,cv2.BORDER_CONSTANT,value=background_color)
    #switch height and width
    imgHeight, imgWidth = image.shape[0], image.shape[1]
    imgShape = image.shape[2]
    completeImage = np.zeros((imgHeight, imgWidth, imgShape), dtype=np.uint8)
    
    for y in range(imgHeight):
        for x in range(imgWidth):
            for color in range(imgShape):
                #y == imgHeight and x == imgWidth
                if(x == 0 or y == 0 or y == imgHeight or x == imgWidth):
                    r = 0
                elif ((x < (imgWidth-2)) and (y < (imgHeight-2))):
                    #Mask and Image Pixels
                    focusedMatrix = [image[y-1, x-1, color], image[y-1, x, color], image[y-1, x+1, color],
                                    image[y, x-1, color], image[y, x, color], image[y, x+1, color],
                                    image[y+1, x-1, color], image[y+1, x, color], image[y+1, x+1, color]]
                    sortedMatrix = sorted(focusedMatrix)
                    completeImage[y][x][color] = sortedMatrix[4]
    
    completeImage = completeImage.astype(int)

    return completeImage

    raise NotImplementedError

def applyFilter1(image):
    """Filter noise from the image by using applyConvolution() and an averaging filter
    Parameters
    ----------
    image : numpy.ndarray
        A numpy array of dimensions (HxWx3) and type np.uint8
    
    Returns
    -------
    output : numpy.ndarray
        A numpy array of dimensions (HxWx3) and type np.uint8
    """
    # WRITE YOUR CODE HERE.
    #Takes the average of all 9 pixels in the 3x3 grid. 
    avgMatrix = np.array(([[1,1,1],
                         [1,1,1], 
                         [1,1,1]]), dtype=np.float64)
    returnarray = applyConvolution(image, avgMatrix)
    completeImage = np.divide(returnarray,9)
    completeImage = completeImage.astype(int)

    return completeImage

    raise NotImplementedError

def applyFilter2(image):
    """Filter noise from the image by using applyConvolution() and a gaussian filter
    Parameters
    ----------
    image : numpy.ndarray
        A numpy array of dimensions (HxWx3) and type np.uint8
    
    Returns
    -------
    output : numpy.ndarray
        A numpy array of dimensions (HxWx3) and type np.uint8
    """
    # WRITE YOUR CODE HERE.

    gaussianMatrix = np.array([[.0625,.125,.0625], 
                                [.125,.25,.125], 
                                [.0625,.125,.0625]], dtype=np.float64)
    
    completeImage = applyConvolution(image, gaussianMatrix)
    completeImage = completeImage.astype(int)
    completeImage.dtype
    
    return completeImage

    raise NotImplementedError
    
def sharpenImage(image):
    """Sharpen the image. Call applyConvolution with an image sharpening kernel
    Parameters
    ----------
    image : numpy.ndarray
        A numpy array of dimensions (HxWx3) and type np.uint8
    
    Returns
    -------
    output : numpy.ndarray
        A numpy array of dimensions (HxWx3) and type np.uint8
    """
    # WRITE YOUR CODE HERE.
    # construct a sharpening filter
    #Laplacian uses the following matrix operator (Digital Image Processing and Pattern Recognition)
    sharpenedArr = np.array([[0,-1,0], 
                            [-1,5,-1], 
                            [0,-1,0]], dtype=np.float64)
    completeImage = applyConvolution(image, sharpenedArr)
    completeImage = completeImage.astype(int)

    return completeImage

    raise NotImplementedError

if __name__ == "__main__":
    
    # Reading an image in default mode 
    img = cv2.imread('co_image_0.jpg') 
    imS = cv2.resize(img, (960, 540))
    matrix = [3,3]
    
# MEDIAN
#     print("MEDIAN TEST")
#     medianArray = applyMedianFilter(imS,matrix)
#     cv2.imwrite('medianPic.jpg', medianArray)
    applyMedianFilter(imS, matrix)

# ApplyFilter1 - AVERAGE
#     print("AVERAGE TEST")
#     averageArray = applyFilter1(imS)
#     cv2.imwrite('averagePic.jpg', averageArray)
    applyFilter1(imS)
    
# ApplyFilter2 - GAUSSIAN
#     print("GAUSSIAN")
#     gausArray = applyFilter2(imS)
#     cv2.imwrite('gaussianPic.jpg', gausArray)
    applyFilter2(imS)
    
# SHARPEN IMAGE
#     print("SHARPEN IMAGE")
#     sharpenArray = sharpenImage(imS)
#     cv2.imwrite('sharpenPic.jpg', sharpenArray)
    sharpenImage(imS)
    
    pass