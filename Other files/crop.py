import cv2
img = cv2.imread("barcode.png")
crop_img = img[0:209,0:1379]
cv2.imwrite("cropped_bar.png", crop_img)
