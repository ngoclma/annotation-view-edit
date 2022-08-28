import cv2
import os
import random

# ----- INPUT -----
# folder direction (contains images and annotation in YOLO format)
dir = ""
dir_out = ''

dir = dir + '/'
dir_out = dir_out + '/'
origins = os.listdir(dir)
#-----

def cropImg(fileTxt, Img):
    # read files
    imgcv = cv2.imread(dir+Img)
    dimensions = imgcv.shape
    width, height = dimensions[1], dimensions[0]
    
    f = open(dir + fileTxt, "r")
    annos = f.readlines()
    
    # find coordinates
    minL, minT, maxR, maxB = width, height, 0, 0   
    for anno in annos:
        staff = anno.split()
        label = staff[0]
       
        x_center, y_center, w, h = float(staff[1])*width, float(staff[2])*height, float(staff[3])*width, float(staff[4])*height
        x1 = round(x_center-w/2)
        y1 = round(y_center-h/2)
        x2 = round(x_center+w/2)
        y2 = round(y_center+h/2) 

        minL = x1 if x1<minL else minL
        minT = y1 if y1<minT else minT
        maxR = x2 if x2>maxR else maxR
        maxB = y2 if y2>maxB else maxB

    # crop img
    buffer = (random.randint(0, 10)) / 100
    buffer_x = int(buffer*width)
    buffer_y = int(buffer*height)
    L, T, R, B = minL-buffer_x, minT-buffer_y, maxR+buffer_x, maxB+buffer_y
    L = 0 if L < 0 else L
    T = 0 if T < 0 else T
    R = width if R > width else R
    B = height if B > height else B
    newImg = imgcv[T:B, L:R]

    # export img
    os.chdir(dir_out)
    cv2.imwrite(Img, newImg)

    # return bounding coor
    coor = {'x_st':L, 'y_st':T, 'x_ed':R, 'y_ed':B}
    return coor


def editAnno(fileTxt, oriImg, coor):
    # read files
    imgcv = cv2.imread(dir+oriImg)
    dimensions = imgcv.shape
    width, height = dimensions[1], dimensions[0]
      
    f = open(dir + fileTxt, "r")
    annos = f.readlines()

    height_new = coor['y_ed'] - coor['y_st']
    width_new = coor['x_ed'] - coor['x_st']  
    
    # find coordinates
    for anno in annos:
        staff = anno.split()
        label = staff[0]
       
        x_center, y_center, w, h = float(staff[1])*width, float(staff[2])*height, float(staff[3])*width, float(staff[4])*height

        x_new = (x_center - coor['x_st']) / width_new
        y_new = (y_center - coor['y_st']) / height_new
        w_new = w / width_new
        h_new = h / height_new

        f = open(dir_out + fileTxt, "a")
        f.write(label+' '+str(x_new)+' '+str(y_new)+' '+str(w_new)+' '+str(h_new)+'\n')


def convertImg(fileTxt, Img):
    coor = cropImg(fileTxt, Img)
    editAnno(fileTxt, Img, coor)


# Loop through folder
for origin in origins:
    if origin.endswith('.txt'):
        img = origin[0:origin.find('.')]+'.PNG'
        convertImg(origin, img)