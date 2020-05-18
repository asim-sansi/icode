import os
from zipfile import ZipFile
import pytesseract
import cv2
import sys
import numpy as np
#Zip file download option added
from .componentclassifier import ComponentClassifier
from .htmlmapper import HtmlMapper
from keras.models import load_model
import threading

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
loaded_model = load_model(r"E:\ICode\icode\fypsite\processor\CNN_model\third_CNN_model")

def getZipFile(another_path):
    zipObj = ZipFile(another_path+'webpage.zip', 'w')
    zipObj.write(another_path+"webpage.html","webpage.html");
    zipObj.write(another_path + "styles.css","styles.css");
    zipObj.close()
def main(arg):
    # COMMENTED CODE#####################
    # p=arg[0]
    # imgname=arg[1]
    # flush()
    # COMMENTED CODE LIMIT END###########

    # arg[1]['comm-channel'] = comm_channel
    path = "../generated_resources/"
    another_path = "processor/static/generated_resources/"

    # Path of image used to instantiate image object
    img_name = "../processor/"  # path of image
    i = cv2.cvtColor(np.array(arg[0]), cv2.COLOR_BGR2RGB) #cv2.COLOR_BGR2RxGB

    # HTML Mapper Instantiated
    cc = ComponentClassifier(loaded_model)
    h = HtmlMapper(cc)
    # print(type(i[0][0]))
    arg[1]['comm-channel'].put(2)
    code,css = h.ImgToHtml(i, path, arg[1])
    file = open(path + "webpages/" + "webpage.html", "w+", encoding="utf-8")
    file.write(code)
    file = open(another_path + "webpage.html", "w+", encoding="utf-8")
    file.write(code)
    file.close()
    file = open(another_path + "styles.css", "w+", encoding="utf-8")
    file.write(css)
    file.close()
    getZipFile(another_path)
    arg[1]['comm-channel'].put(100)
    return 1
    # cv2.waitKey()
