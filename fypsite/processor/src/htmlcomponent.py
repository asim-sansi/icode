import numpy as np
import cv2
from operator import itemgetter
from PIL import Image
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class HTMLComponent:
    def __init__(self, img, x, y, h, w, attributes, parent=None, text=0):
        self.value = ""
        self.img = img
        # noinspection PyDictCreation
        self.styles = {}
        self.attributes = attributes
        self.classes = []
        self.parent = parent
        self.styles['left'] = str(x) + "px"
        self.styles['top'] = str(y) + "px"
        self.styles['width'] = str(w) + "px"
        self.styles['height'] = str(h) + "px"
        self.styles['display'] = "block"
        self.styles['position'] = "absolute"
        # self.styles['text-align'] = "center"
        # self.styles['border'] = "solid black 1px"
        self.styles['color'] = "rgb(0, 0, 0)"
        self.styles['background-color'] = "rgb(255, 255, 255)"
        self.styles['font-size'] = "12px"
        # if self.attributes['tag'] == 'a':
        #     self.styles['font-size'] = str(h) + "px"
        self.styles['font-family'] = "Arial, Helvetica, sans-serif"
        # self.styles['padding'] = "0%"
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.bgcolor = (255, 255, 255)
        self.color = (0, 0, 0)
        # self.cnt = cnt
        self.path = ""
        self.sub = []  # sub elements
        self.innerHTML = ""
        self.setDominantColor()
        if self.attributes['tag'] in ['a', 'button', 'p']:
            self.innerHTML = self.get_inner_html(text)
            if self.attributes['tag'] == "p":
                self.styles['white-space'] = "wrap"
                self.styles['color'] = 'black'
        elif self.attributes['tag'] == "input" and self.attributes['type'] == "text":
            self.attributes['placeholder'] = self.get_inner_html(text)
            if(self.attributes['placeholder'] in ["Password", "password", "ssword", "pass"]):
                self.attributes['type'] = "password"
            self.styles['color'] = "#111"


    def setImage(self, img):
        self.img = img

    def getStyle(self):
        return self.styles

    def get_inner_html(self, ocr=1):
        s = pytesseract.image_to_string(self.img);
        if ocr == 0:
            return self.getRandomText(len(s))
        elif ocr == 1:
            return s
        else:
            return "{" + self.attributes['tag'] + "}"

    def setCoordinates(self, x, y):
        self.x = x
        self.y = y

    def getRandomText(self, n):
        text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec pretium mauris enim, at congue lacus " \
               "accumsan at. Integer vel suscipit neque. Integer eu dolor in mi consequat tincidunt sed non augue. " \
               "Nullam condimentum mi tempus leo maximus, vel bibendum odio tempor. Nunc convallis dignissim ex, " \
               "a aliquam orci commodo non. Integer lacinia fringilla est ut mollis. Aenean dignissim metus eget " \
               "augue pulvinar, ac vulputate nisl mattis. Ut non elementum dolor. Aliquam dictum finibus gravida. " \
               "Quisque elementum mauris felis, ac facilisis enim porta ac.";
        while n > len(text):
            text *= 2
        return text[0:n]

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
                self.styles['color'] = "white"
        else:
            self.styles['background-color'] = "white"

        return

    def set_shape(self, approx):
        if len(approx) <= 5:
            # self.styles['shape'] = "rectangle"
            self.styles['border-radius'] = str(len(approx) * 0) + "px"
        else:
            # self.styles['shape'] = "round"
            self.styles['border-radius'] = str(len(approx) * 3) + "px"
        return


    def StartTag(self):
        code = "<"
        for key, value in self.attributes.items():
            if key == "tag":
                code += value + " "
            else:
                code += key + "='" + value + "' "

        code += "STYLE='"
        for key, value in self.styles.items():
            code += key + ": " + str(value) + ";"
        return code + "'>\n";

    def CloseTag(self):
        if self.attributes['tag'] != "input" and self.attributes['tag'] != "img":
            return "</" + self.attributes['tag'] + ">\n"
        else:
            return "\n"

    def Code(self):
        #      self.styles[]
        code = "<" + \
               self.attributes['tag'] + \
               " style='"
        for key, value in self.styles.items():
            code += key + ": " + value + ";"
        if self.attributes['tag'] != "input" and self.attributes['tag'] != "img":
            code += "'>" + self.innerHTML + "</" + self.attributes['tag'] + ">\n"
        elif self.attributes['tag'] == 'img':
            code += "' src='../images/default_image.png'>"
        else:
            code += "'>"
        return code
