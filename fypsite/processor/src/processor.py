import os

import pytesseract
import cv2
import sys
import numpy as np

from .componentclassifier import ComponentClassifier
from .htmlmapper import HtmlMapper
from keras.models import load_model
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'
loaded_model = load_model("A:\SEMESTER_6\Software_Engineering\icode\\fypsite\processor\CNN_model\CNNmodel")


#
# def main(arg):
#     ocr_integration = arg[1]  # set true to use OCR
#
#     path = "../generated_resources/"
#
#     # Path of image used to instantiate image object
#     img_name = "../processor/"  # path of image
#     i = cv2.cvtColor(np.array(arg[0]), cv2.COLOR_BGR2RGB)
#
#     # HTML Mapper Instantiated
#     h = HtmlMapper()
#
#     code = h.ImgToHtml(i, path, ocr_integration)
#     file = open(path + "webpages/" + "webpage.html", "w+", encoding="utf-8")
#     file.write(code)
#     file.close()
#     os.system("start \"\" " + path + "webpages/" + "webpage.html\"")
#     cv2.waitKey()


def main(arg):
    # COMMENTED CODE#####################
    # p=arg[0]
    # imgname=arg[1]
    # flush()
    # COMMENTED CODE LIMIT END###########
    # loaded_model = pickle.load(open("fypsite/processor/CNN_model/first_CNN_model", 'rb'))
    ocr_integration = arg[1]  # set true to use OCR

    path = "../generated_resources/"
    # p = "../generated_resources/webpages/"

    # Path of image used to instantiate image object
    img_name = "../processor/"  # path of image
    i = cv2.cvtColor(np.array(arg[0]), cv2.COLOR_BGR2RGB) #cv2.COLOR_BGR2RxGB

    # HTML Mapper Instantiated
    c = ComponentClassifier(loaded_model)
    h = HtmlMapper(c)
    # print(type(i[0][0]))


    code = h.ImgToHtml(i, path, ocr_integration)
    file = open(path + "webpages/" + "webpage.html", "w+", encoding="utf-8")
    file.write(code)
    file.close()
    os.system("start \"\" " + path + "webpages/" + "webpage.html\"")
    # cv2.waitKey()
