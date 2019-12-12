from src.htmlComponent import HTMLComponent
import pytesseract
import cv2


class TEXT(HTMLComponent):
    def __init__(self, img, x, y, h, w, p):
        super().__init__(img, x, y, h, w, p)
        self.txt = " "
        self.type = " "
        self.link = False;

        if (h > 30):
            self.type = "p"
        elif (h > 24):
            self.type = "h2"
        # else:
        else:
            self.type = "p"
        # self.LinkCheck()
        # print(self.type)

    def setPath(self, p):
        super().setPath(p)

    def LinkCheck(self):
        if self.styles['color'] == "rgb(0,0,255)":
            self.tag = "a"
            print(self.tag)

    def translateText(self):
        if self.styles['color'] == "rgb(255, 255, 255)":
            self.img = cv2.bitwise_not(self.img)
        #  cv2.imshow("h",self.img)
        #   cv2.waitKey()
        self.txt = (pytesseract.image_to_string(super().getImage()))
        if len(self.txt) == 0:
            return "<img src=" + self.path + ">"
        return self.txt

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

        code += "'>" + self.translateText() + "</div>\n"
        # " SRC='" + self.path + "'>"
        return code
