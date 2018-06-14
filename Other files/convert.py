from wand.image import Image
from wand.color import Color
import base64

data = open("pdfto64.txt", "rb").read()
f = open("64topdf.pdf", "w")
f.write(data.decode('base64'))
f.close()

with Image(filename="64topdf.pdf", resolution=100) as img:
  with Image(width=img.width, height=img.height, background=Color("white")) as bg:
    bg.composite(img,0,0)
    bg.save(filename="pdftojpg.jpg")

data = open("pdftojpg.jpg", "rb").read().encode("base64")
f = open("jpgto64.txt", "w")
f.write(data)
f.close()
