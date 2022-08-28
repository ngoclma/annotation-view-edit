import cv2
import pandas as pd
import csv
import numpy as np

# INPUT
m = 0
n = 0
img1_dir = ""
img2_dir = ""
vid1 = ""
vid2 = ""
img1_csv = ""
img2_csv = ""

# IMAGE color list
list_ch1 = []
with open(img1_csv) as file:
    reader_obj = csv.reader(file)
    for row in reader_obj:
        m = m + 1
        n = len(row)
        list_ch1 = list_ch1 + row
list_ch2 = []
with open(img2_csv) as file:
    reader_obj = csv.reader(file)
    for row in reader_obj:
        list_ch2 = list_ch2 + row

# VIDEO import
cap = cv2.VideoCapture(vid1)
cap_ch2 = cv2.VideoCapture(vid2)

frame_width = int((cap.get(3)))
frame_height = int((cap.get(4)))

resize_factor = 0.4
display_dim = (int(frame_width * resize_factor), int(frame_height * resize_factor))

# FUNCTIONS
coor = {"x_st": 0, "y_st": 0, "x_ed": 0, "y_ed": 0}


def countRectangles():
    return m * n


def initCoor(coor):
    coor["x_st"] = 0
    coor["y_st"] = 0
    coor["x_ed"] = frame_width / n
    coor["y_ed"] = frame_height / m
    return coor


def changeCoor(coor):
    if int(coor["x_ed"]) >= frame_width:
        coor["x_st"] = 0
        coor["x_ed"] = frame_width / n
        coor["y_st"] = coor["y_st"] + frame_height / m
        coor["y_ed"] = coor["y_ed"] + frame_height / m
    else:
        coor["x_st"] = coor["x_st"] + frame_width / n
        coor["x_ed"] = coor["x_ed"] + frame_width / n
    return coor


# ------------------------------------------------------------------------------------

# IMAGE create
pixel_array1 = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)
pixel_array2 = np.zeros((frame_height, frame_width, 1), dtype=np.uint8)

# IMAGE draw
coor = initCoor(coor)
no = countRectangles()
for i in range(no):
    start_point = (int(coor["x_st"]), int(coor["y_st"]))
    end_point = (int(coor["x_ed"]), int(coor["y_ed"]))
    pixel_array1 = cv2.rectangle(
        pixel_array1, start_point, end_point, int(list_ch1[i]), -1
    )
    pixel_array2 = cv2.rectangle(
        pixel_array2, start_point, end_point, int(list_ch2[i]), -1
    )
    # set up next point
    coor = changeCoor(coor)

# IMAGE show
pixel_array1_display = cv2.resize(pixel_array1, display_dim)
pixel_array2_display = cv2.resize(pixel_array2, display_dim)
cv2.imshow("roi_ch1", pixel_array1_display)
cv2.imshow("roi_ch2", pixel_array2_display)

# IMAGE export
cv2.imwrite(img1_dir, pixel_array1)
cv2.imwrite(img2_dir, pixel_array2)
# ------------------------------------------------------------------------------------

# VIDEO check
if cap.isOpened() == False:
    print("Error opening video stream or file")
if cap_ch2.isOpened() == False:
    print("Error opening video stream or file")

# VIDEO run
while cap.isOpened() and cap_ch2.isOpened():
    # Capture frame-by-frame
    ret, frame = cap.read()
    ret_ch2, frame_ch2 = cap_ch2.read()

    # VIDEO draw
    coor = initCoor(coor)
    no = countRectangles()
    for i in range(no):
        # draw rectangle
        start_point = (int(coor["x_st"]), int(coor["y_st"]))
        end_point = (int(coor["x_ed"]), int(coor["y_ed"]))
        color = (0, 0, 0)

        frame = cv2.rectangle(frame, start_point, end_point, color, 1)
        frame_ch2 = cv2.rectangle(frame_ch2, start_point, end_point, color, 1)

        # write text
        org = (int(coor["x_st"]), int(coor["y_st"]) + 70)
        frame = cv2.putText(frame, str(i), org, cv2.FONT_HERSHEY_SIMPLEX, 2, color, 1)
        frame_ch2 = cv2.putText(
            frame_ch2, str(i), org, cv2.FONT_HERSHEY_SIMPLEX, 2, color, 1
        )

        # set up next point
        coor = changeCoor(coor)

    # VIDEO resize
    frame_ch1_display = cv2.resize(frame, display_dim)
    frame_ch2_display = cv2.resize(frame_ch2, display_dim)
    concat_h = cv2.hconcat([frame_ch1_display, frame_ch2_display])

    # VIDEO display
    cv2.imshow("ch1-ch2", concat_h)

    # Press Q on keyboard to  exit
    if cv2.waitKey(0) & 0xFF == ord("q"):
        break

# When everything done, release the video capture object
cap.release()
cap_ch2.release()

# Closes all the frames
cv2.destroyAllWindows()
