import cv2
import os
import random

# -----
# INPUT
# folder direction (contains images and annotation in YOLO format)
dir = ""

dir = dir + "/"
origins = os.listdir(dir)
# random: 0 || in-order: 1
mode = 0
# -----

palette = [
    (178, 34, 34),
    (0, 0, 0),
    (255, 215, 0),
    (34, 139, 34),
    (0, 201, 87),
    (0, 191, 255),
    (16, 78, 139),
    (72, 61, 139),
    (191, 62, 255),
    (255, 20, 147),
    (139, 69, 0),
    (220, 20, 60),
    (131, 139, 139),
]
labels = ["1", "2", "3", "4", "5", "6"]

# Annotate
def annotate(Img, x1, y1, x2, y2, label):
    # draw box
    coor = {"x_st": x1, "y_st": y1, "x_ed": x2, "y_ed": y2}
    start_point = (int(coor["x_st"]), int(coor["y_st"]))
    end_point = (int(coor["x_ed"]), int(coor["y_ed"]))
    color = palette[int(label)]
    Img = cv2.rectangle(Img, start_point, end_point, color, 1)

    # write text
    org = (int(coor["x_st"]), int(coor["y_st"]) + 20)
    Img = cv2.putText(
        Img, labels[int(label)], org, cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1
    )
    cv2.imshow("test", Img)


# Draw an image
def drawOneImg(fileTxt, Img):
    imgcv = cv2.imread(dir + Img)
    dimensions = imgcv.shape
    width, height = dimensions[1], dimensions[0]

    f = open(dir + fileTxt, "r")
    annos = f.readlines()
    for anno in annos:
        staff = anno.split()
        label = staff[0]

        x_center, y_center, w, h = (
            float(staff[1]) * width,
            float(staff[2]) * height,
            float(staff[3]) * width,
            float(staff[4]) * height,
        )
        x1 = round(x_center - w / 2)
        y1 = round(y_center - h / 2)
        x2 = round(x_center + w / 2)
        y2 = round(y_center + h / 2)

        annotate(imgcv, x1, y1, x2, y2, label)


# Loop through folder
if mode == 1:
    origins.sort()
else:
    random.shuffle(origins)
for origin in origins:
    if origin.endswith(".txt"):
        img = origin[0 : origin.find(".")] + ".PNG"
        drawOneImg(origin, img)

    # Press Q on keyboard to  exit
    if cv2.waitKey(0) & 0xFF == ord("q"):
        break
