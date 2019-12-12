

import os
import pytesseract
import cv2
import sys
import numpy as np
from src.htmlmapper import HtmlMapper


import shutil

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'







def main(arg):

    # COMMENTED CODE#####################
    # p=arg[0]
    # imgname=arg[1]
    # flush()
    # COMMENTED CODE LIMIT END###########

    ocr_integration = True;  # set true to use OCR

    path = "../generated_resources/"
    # p = "../generated_resources/webpages/"

    # Path of image used to instantiate image object
    img_name = "../resources/flex.png"  # path of image
    i = cv2.imread(img_name)

    # HTML Mapper Instantiated
    h = HtmlMapper()

    code = h.ImgToHtml(i, path, ocr_integration)
    file = open(path + "webpages/" + "webpage.html", "w+")
    file.write(code)
    file.close()
    os.system("start \"\" " + path + "webpages/" + "webpage.html\"")
    cv2.waitKey();


if __name__ == "__main__":
    main(sys.argv[1:])

