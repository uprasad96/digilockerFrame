import cv2
background = cv2.imread('combined.png')
overlay = cv2.imread('result.png')
background[319:2518,14:2467] = overlay
cv2.imwrite('final.png', background)
