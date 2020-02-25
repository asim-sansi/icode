from .htmlcomponent import HTMLComponent
import pytesseract
import cv2

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class TEXT(HTMLComponent):
    def __init__(self, img, x, y, h, w, p):
        super().__init__(img, x, y, h, w, p)
        self.txt = " "
        self.type = " "
        self.link = False

        self.SpecifyType()
        # self.LinkCheck()
        # print(self.type)

    def setPath(self, p):
        super().setPath(p)

    def LinkCheck(self):
        if self.styles['color'] == "rgb(0,0,255)":
            self.tag = "a"
            print(self.tag)

    def SpecifyType(self):
        fontsize = self.getFontSize()
        # if (fontsize >= 32):
        #     self.type = 'h1'
        # elif (fontsize >= 24):
        #     self.type = 'h2'
        # elif (fontsize >= 20):
        #     self.type = 'h3'
        # elif(fontsize>=16):
        #     self.type='h4'
        # elif(fontsize>=12):
        #     self.type='h5'
        # elif(fontsize>=11):
        #     self.type='h6'
        # else:
        #     self.type = 'p'
        self.type = 'p'
        # self.styles['font-size'] = str(fontsize)+'px'


    def translateText(self):
        if self.styles['color'] == "rgb(255, 255, 255)":
            self.img = cv2.bitwise_not(self.img)
        #  cv2.imshow("h",self.img)
        #   cv2.waitKey()
        self.txt = (pytesseract.image_to_string(super().getImage()))
        if len(self.txt) == 0:
            return "<img src=" + self.path + ">"
        return self.txt

    def getFontSize(self):
        boxes = pytesseract.image_to_boxes(self.img)
        line = boxes.split("\n")
        line = line[0]
        l = line.split(' ')
        if (len(l) > 4):
            return (int(l[4]) - int(l[2]))
        else:
            return 0;

    def Code(self):
        # x, y = super().getCoordinates()
        # code = "<" + self.type
        # code += r' STYLE="position:absolute; TOP:' + str(y) + "px;LEFT:" + str(x) + "px;\""
        # if (self.link):
        #     code += "href=\"a.html\""
        # code += ">";
        # code += self.translateText();
        # code += "</" + self.type + ">";
        # return code

        code = "<" + \
               "div" + \
               " STYLE='"
        for key, value in self.styles.items():
            code += key + ": " + value + ";"

        code += "'>" + \
                "<" + self.type + ">" + \
                self.translateText() + \
                "</" + self.type + ">" + \
                "</div>\n"
        # " SRC='" + self.path + "'>"
        return code
