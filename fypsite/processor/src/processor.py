import os
import pytesseract
import cv2
import sys
import numpy as np
from .htmlmapper import HtmlMapper

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


def main(arg):
    ocr_integration = arg[1]  # set true to use OCR

    path = "../generated_resources/"

    # Path of image used to instantiate image object
    img_name = "../processor/"  # path of image
    i = cv2.cvtColor(np.array(arg[0]), cv2.COLOR_BGR2RGB)

    # HTML Mapper Instantiated
    h = HtmlMapper()

    code = h.ImgToHtml(i, path, ocr_integration)
    file = open(path + "webpages/" + "webpage.html", "w+")
    file.write(code)
    file.close()
    os.system("start \"\" " + path + "webpages/" + "webpage.html\"")
    cv2.waitKey()
