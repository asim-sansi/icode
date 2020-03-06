import os

import pytesseract
import cv2
import sys
import numpy as np

from .componentclassifier import ComponentClassifier
from .htmlmapper import HtmlMapper
from keras.models import load_model
import threading

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
loaded_model = load_model("C:\\Users\i1602\Desktop\iCode\\fypsite\processor\CNN_model\\third_CNN_model")


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
    code = h.ImgToHtml(i, path, arg[1])
    file = open(path + "webpages/" + "webpage.html", "w+", encoding="utf-8")
    file.write(code)
    file = open(another_path + "webpage.html", "w+", encoding="utf-8")
    file.write(code)
    file.close()
    arg[1]['comm-channel'].put(100)
    return 1
    # cv2.waitKey()
