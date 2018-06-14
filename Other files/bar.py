import barcode
from barcode.writer import ImageWriter
import cv2
writer = ImageWriter()
writer.dpi = 100
CODE = barcode.get_barcode_class('code39')
code = CODE(u'in.org.bseh-HSCER-12345678902018', writer)
bar = code.save('barcode')

img = cv2.imread("barcode.png")
crop_img = img[0:69,0:460]
# cv2.imwrite("cropped_bar.png", crop_img)

large = cv2.resize(crop_img, (0,0), fx=1.5, fy=1.5)

cv2.imwrite("cropped_large_bar.png", large)
