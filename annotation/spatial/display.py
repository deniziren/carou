##########################################################################
# Copyright 2020 Deniz Iren. All Rights Reserved.

__name__ = 'annotation.spatial.display'
__author__ = 'Deniz Iren (deniziren@gmail.com)'
__version__ = '0.002'
__lastupdate__ = '10.11.2019'

def version():
	return __version__
	
def lastUpdate():
	return __lastupdate__

def name():
	return __name__

def packageInfo():
	return 'Package name: ' + __name__ + ' | ' + 'Version: ' + __version__ + ' | ' + 'Author: ' + __author__
	
##########################################################################

from enum import Enum
class AnnotationDisplayMode(Enum):
    ANNOTATIONS_ONLY = 'ANNOTATIONS_ONLY'
    DOUBLE_AGREEMENT_ONLY = 'DOUBLE_AGREEMENT_ONLY'
    TRIPLE_AGREEMENT_ONLY = 'TRIPLE_AGREEMENT_ONLY'
    ANNOTATIONS_AND_DOUBLE = 'ANNOTATIONS_AND_DOUBLE'
    ANNOTATIONS_AND_TRIPLE = 'ANNOTATIONS_AND_TRIPLE'
    ALL = 'ALL'
    
def displayAnnotationsOnImage(dictAnnotations, imgName, imgDirectory, displayMode='ALL', showfilename=False, displayFigure=True): 
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import numpy as np
    #from PIL import Image
    #img = Image.open(imgDirectory + imgName)
    img = mpimg.imread(imgDirectory + imgName)
    my_dpi = 96
    fig = plt.figure(num=None, figsize=(1024/my_dpi, 768/my_dpi), dpi=my_dpi, tight_layout=True)
    plt.imshow(img)
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')

    if showfilename:
        plt.text(20, 20, imgName, color='white')
    if displayMode == 'ALL' or displayMode == 'ANNOTATIONS_ONLY' or displayMode == 'ANNOTATIONS_AND_DOUBLE' or displayMode == 'ANNOTATIONS_AND_TRIPLE':
        for points in dictAnnotations['../input/' + imgName]['A']:
            plt.scatter(points[0], points[1], s=50, c='red', marker='o')
        for points in dictAnnotations['../input/' + imgName]['B']:
            plt.scatter(points[0], points[1], s=50, c='blue', marker='^')
        for points in dictAnnotations['../input/' + imgName]['C']:
            plt.scatter(points[0], points[1], s=50, c='green', marker='P')
    if displayMode == 'ALL' or displayMode == 'DOUBLE_AGREEMENT_ONLY' or displayMode == 'ANNOTATIONS_AND_DOUBLE':
        for points in dictAnnotations['../input/' + imgName]['doubleAgreement']:
            plt.scatter(points[0], points[1], s=50, c='yellow', marker='p')
    if displayMode == 'ALL' or displayMode == 'TRIPLE_AGREEMENT_ONLY' or displayMode == 'ANNOTATIONS_AND_TRIPLE':
        for points in dictAnnotations['../input/' + imgName]['tripleAgreement']:
            plt.scatter(points[0], points[1], s=50, c='purple', marker='p')
    if not displayFigure:
        plt.close(fig)
    return fig
	
def displayImageWithAnnotations(img, pointList=[], polygonList=[], title='', displayFigure=False):
    import matplotlib.pyplot as plt
    import matplotlib.image as mpimg
    import numpy as np
    import matplotlib.patches as patches
    from matplotlib.patches import Polygon
   
    my_dpi = 96
    
    # Create figure and axes
    fig,ax = plt.subplots(figsize=(1024/my_dpi, 768/my_dpi), dpi=my_dpi, tight_layout=True)
    
    #fig = plt.figure(num=None, figsize=(1024/my_dpi, 768/my_dpi), dpi=my_dpi, tight_layout=True)
    #plt.imshow(img)
    plt.xticks([])
    plt.yticks([])
    plt.axis('off')

    
    # Display the image
    ax.imshow(img)

    # Create a Rectangle patch
    #rect = patches.Rectangle((50,100),40,30,linewidth=1,edgecolor='r',facecolor='none')

    # Add the patch to the Axes
    #ax.add_patch(rect)

    plt.text(20, 20, title, color='white')
    for points in pointList:
        plt.scatter(int(points[0]), int(points[1]), s=50, c='red', marker='o')
    for polygon in polygonList:
        ax.add_patch(Polygon(polygon,  alpha=0.4))
    if not displayFigure:
        plt.close(fig)
    return fig
	
def getPaintedCanvas(fig):
    from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
    from matplotlib.figure import Figure
    import numpy as np

    
    canvas = FigureCanvas(fig)
    #ax = fig.gca()
    width, height = fig.get_size_inches() * fig.get_dpi()
    #ax.text(0.0,0.0,"Test", fontsize=45)
    #ax.axis('off')
    #print(int(width),int(height))
    canvas.draw()       # draw the canvas, cache the renderer
    return np.frombuffer(canvas.tostring_rgb(), dtype='uint8').reshape(int(height), int(width), 3)
	
def processImage(img_cv, histogramEqualization='NONE', GaussianBlur=True, GaussianBlurKernelSize=(11,11), erodeIterations=4, dilateIterations=2):
    import cv2
    import numpy as np
    from matplotlib import pyplot as plt
    import matplotlib.image as mpimg
    
    ### HIST QUALIZATION
    if histogramEqualization == 'NONE':
        print('No histogram equalization applied.')
        equ_img = img_cv.copy()
    if histogramEqualization == 'EQUALIZE':
        print('cv2.equalizeHist function applied.')
        equ_img = cv2.equalizeHist(img_cv.copy())
    if histogramEqualization == 'CLAHE':
        print('CLAHE  applied.')
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        equ_img = clahe.apply(img_cv.copy())

    ###### GAUSSIAN BLUR AND THRESHOLDING
    # Otsu's thresholding after Gaussian filtering
    if GaussianBlur:
        blur = cv2.GaussianBlur(equ_img, GaussianBlurKernelSize, 0)
        ret3,th_gaussian_blur = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    else:
        th_gaussian_blur = equ_img
    
    ###### ERODE + DILATE
    kernel = np.ones((3,3), np.uint8)
    if erodeIterations>0:
        gaus_erode = cv2.erode(th_gaussian_blur, kernel, iterations=erodeIterations)
    else: 
        gaus_erode = th_gaussian_blur
    
    if dilateIterations>0:
        gaus_erode_dilate = cv2.dilate(gaus_erode, kernel, iterations=dilateIterations)
    else: 
        gaus_erode_dilate=gaus_erode
        
    return gaus_erode_dilate
        
def plotImageMatrix(imageList, titleList=[]):
    from matplotlib import pyplot as plt
    import math

    
    cols = 3
    rows = math.ceil(len(imageList)/cols)
    
    fig = plt.figure(num=None, figsize=(16, 16), dpi=80, facecolor='w', edgecolor='k')

    cnt = 0
    for im in imageList:
        cnt = cnt + 1
        plt.subplot(rows,cols,cnt),plt.imshow(im,'gray'), plt.title(titleList[cnt-1]), plt.xticks([]), plt.yticks([])
    
    return fig    

#def contourFind(dir, img_name, hayStackImage, dictPolyPoiAnnotations):
def findContours(base_image, hayStackImage, imageName, dictPolyPoiAnnotations):
    from shapely.geometry import Polygon, Point
    import cv2
    import numpy as np
    dictPointsAndPolygons = dict()
    
    
    for pts in dictPolyPoiAnnotations[imageName]['poi']:
        pts_tuple = (int(pts[0]), int(pts[1]))
        pts_Point_shapely = Point(pts_tuple)
        k = imageName + '_' + str(pts[0]) + '_' + str(pts[1])
        if k not in dictPointsAndPolygons:
            dictPointsAndPolygons[k] = dict()
            dictPointsAndPolygons[k]['point_shapely'] = pts_Point_shapely
        else:
            dictPointsAndPolygons[k]['point_shapely'] = pts_Point_shapely
            
        for pItemDict in dictPolyPoiAnnotations[imageName]['poly']:
            polyFromDict_shapely = Polygon(pItemDict)
            if pts_Point_shapely.within(polyFromDict_shapely):
                if polyFromDict_shapely.is_valid:
                    dictPointsAndPolygons[k]['gold_polygon_shapely'] = polyFromDict_shapely
                else:
                    dictPointsAndPolygons[k]['gold_polygon_shapely'] = polyFromDict_shapely.buffer(0)
                    
        ## At this point points and gold polygons are in the dictionary.
            
    
    listColor = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(255,0,255),(0,255,255)]
    contours, hierarchy = cv2.findContours(hayStackImage,cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    
    print(len(contours), ' found on the haystack image.')
    
    ret_img = base_image.copy()
    #img_name = list(dictPolyPoiAnnotations.keys())[30]
    #dir = 'D:/Aachen Steel Image/PNG/TIFF/'
    #im3 = cv2.imread(dir + img_name)
    
    #height, width, channels = ret_img.shape
    height, width = ret_img.shape

    color = 0
    for cx in contours:
        #print(getContourArea(cx))
        #if getContourArea(cx) > 100: 
        for pts in dictPolyPoiAnnotations[imageName]['poi']:
            k = imageName + '_' + str(pts[0]) + '_' + str(pts[1])
            pts_tuple = (int(pts[0]), int(pts[1]))
            
            dist= cv2.pointPolygonTest(cx, pts_tuple, False)
            if dist > 0:
                color = color + 1
                if color == 6:
                    color = 0
                ret_img = cv2.drawContours(ret_img, [cx], 0, listColor[color], 2)

                myCont = np.squeeze(cx)
                myPoly = Polygon(myCont)
                #print(myPoly.area)
                if myPoly.is_valid:
                    dictPointsAndPolygons[k]['contour_polygon_shapely'] = myPoly
                else:
                    dictPointsAndPolygons[k]['contour_polygon_shapely'] = myPoly.buffer(0)

                

                #print(cx)
                #x,y,w,h = cv2.boundingRect(cx)
                #ret_img = cv2.rectangle(ret_img,(x,y),(x+w,y+h),(0,255,0),2)
                    
    return ret_img, dictPointsAndPolygons
