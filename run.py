from flask import Flask, render_template, Response, request
from wand.image import Image
from wand.color import Color
import base64
import os
import barcode
from barcode.writer import ImageWriter
import cv2
import json
from flask_basicauth import BasicAuth
app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'Utkarsh'
app.config['BASIC_AUTH_PASSWORD'] = 'Prasad'

basic_auth = BasicAuth(app)

def pdf2Img(pdf64, scale, imType):
    pdf64 = pdf64.replace("PLUSE", "+")
    pdf64 = pdf64.replace("SLASH", "/")
    f = open("tempPDF.pdf", "w")
    f.write(pdf64.decode("base64"))
    f.close()

    with Image(filename="tempPDF.pdf", resolution=100*scale) as img:
      with Image(width=img.width, height=img.height, background=Color("white")) as bg:
        bg.composite(img,0,0)
        bg.save(filename="pdfinImg."+imType)

    img = cv2.imread("pdfinImg."+imType)
    os.remove("tempPDF.pdf")
    os.remove("pdfinImg."+imType)
    return img

def genBar(file, scale, imType):
    writer = ImageWriter()
    writer.dpi = 100*scale
    writer.module_height = 25.0
    writer.format = imType
    CODE = barcode.get_barcode_class('code128')
    code = CODE(unicode(file), writer)
    bar = code.save('barcode')

    img = cv2.imread("barcode."+imType)
    os.remove("barcode."+imType)
    crop_img = img[0:69*scale,0:460*scale]
    large = cv2.resize(crop_img, (0,0), fx=1.5, fy=1.5)

    return large

def mergeBar(bar, scale, imType):
    background = cv2.imread('digiDocFrame.'+imType)
    resized_image = cv2.resize(bar, (690, 122))
    background[84:206,1655:2345] = resized_image
    return background

def mergeDoc(overlay, merged, scale):
    resized_image = cv2.resize(overlay, (2480, 3189))
    merged[319:3508,0:2480] = resized_image
    return merged

@app.route('/test', methods = ['POST'])
@basic_auth.required
def convert():
    err = json.dumps({"status":0, "response": "Error"})
    try:
        filename = request.form['filename']
    except:
        return err
    try:
        imType = request.form['imType']
    except:
        imType = "png"
    try:
        dpi = int(request.form['resolution'])
    except:
        dpi = 300

    scale = dpi/100

    Img = pdf2Img(request.form['pdf64'], scale, imType)
    bar = genBar(filename, scale, imType)
    merged = mergeBar(bar, scale, imType)
    final = mergeDoc(Img, merged, scale)
    cv2.imwrite(filename+"_"+str(dpi)+"dpi."+imType, final)
    data = open(filename+"_"+str(dpi)+"dpi."+imType, "rb").read().encode("base64")
    os.remove(filename+"_"+str(dpi)+"dpi."+imType)
    data = data.replace('\n','')
    ret = json.dumps({"status": 1, "response" : data, "resolution": dpi, "MIME" : imType})
    return Response(ret, mimetype = 'application/json')

if __name__ == '__main__':
    app.run(debug = True)
