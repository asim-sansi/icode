import numpy as np
import cv2
from operator import itemgetter
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class HTMLComponent:
    def __init__(self, img, x, y, h, w, cnt):
        self.tag = "div"
        self.value = ""
        self.img = img
        # noinspection PyDictCreation
        self.styles = {}
        self.styles['left'] = str(x) + "px"
        self.styles['top'] = str(y) + "px"
        self.styles['width'] = str(w) + "px"
        self.styles['height'] = str(h) + "px"
        self.styles['display'] = "block"
        self.styles['position'] = "absolute"
        self.styles['text-align'] = "center"
        self.styles['border'] = "solid black 1px"
        self.styles['color'] = "rgb(0, 0, 0)"
        self.styles['background-color'] = "rgb(255, 255, 255)"
        self.styles['font-size'] = "16px"
        self.styles['font-family'] = "Arial, Helvetica, sans-serif"
        self.styles['padding'] = "0%"
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.bgcolor = (255, 255, 255)
        self.color = (0, 0, 0)
        self.cnt = cnt
        self.path = ""
        self.sub = []  # sub elements
        self.setDominantColor()

    def setImage(self, img):
        self.img = img

    def getStyle(self):
        return self.styles

    def setCoordinates(self, x, y):
        self.x = x
        self.y = y

    def AddSubElement(self, e):
        self.sub.append(e)

    def getSubElements(self):
        return self.sub

    def getImage(self):
        return self.img

    def getCoordinates(self):
        return self.x, self.y

    def getAttributes(self):
        return self.x, self.y, self.w, self.h

    def setPath(self, p):
        self.path = p

    def getColors(self):
        return (self.bgcolor[2], self.bgcolor[1], self.bgcolor[0]), (self.color[2], self.color[1], self.color[0]);

    def setDominantColor(self):
        # You may need to convert the color.
        my_img = np.array(self.img, dtype=np.uint8)
        my_img = cv2.cvtColor(my_img, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(my_img)
        # For reversing the operation:
        # im_np = np.asarray(im_pil)
        my_colours = pil_image.getcolors(100000)
        if my_colours:
            self.styles['background-color'] = "rgb" + str(max(my_colours, key=itemgetter(0))[1])
            self.bgcolor = max(my_colours, key=itemgetter(0))[1];
            my_colours.remove(max(my_colours, key=itemgetter(0)))
            if my_colours:
                self.styles['color'] = "rgb" + str(max(my_colours, key=itemgetter(0))[1])
                self.color = max(my_colours, key=itemgetter(0))[1];
            else:
                self.styles['color'] = "rgb(255,255,255)"
        else:
            self.styles['background-color'] = "red"

        return

    def set_shape(self, approx):
        if len(approx) == 3:
            # self.styles['shape'] = "triangle"
            self.styles['border-radius'] = str(len(approx) * 0) + "px"
        elif len(approx) == 4:
            # self.styles['shape'] = "rectangle"
            self.styles['border-radius'] = str(len(approx) * 0) + "px"
        else:
            # self.styles['shape'] = "round"
            self.styles['border-radius'] = str(len(approx) * 5) + "px"
        return

    def translate_text(self):
        if self.styles['color'] == "rgb(255, 255, 255)":
            self.img = cv2.bitwise_not(self.img)
        #  cv2.imshow("h",self.img)
        #   cv2.waitKey()
        self.txt = (pytesseract.image_to_string(self.getImage()))
        if len(self.txt) == 0:
            return "<img src=" + self.path + ">"
        return self.txt

    def Code(self):
        code = "<" + \
               self.tag + \
               " STYLE='"
        for key, value in self.styles.items():
            code += key + ": " + value + ";"

        code += "'>"
        code += self.translate_text()
        if self.tag != 'input' and self.tag != 'img':
            code += '</' + self.tag + '>\n'

        return code
