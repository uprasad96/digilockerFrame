import cv2
background = cv2.imread('digiDocFrame.png')
overlay = cv2.imread('cropped_large_bar.png')
background[105:209,1660:2350] = overlay
cv2.imwrite('combined.png', background)
