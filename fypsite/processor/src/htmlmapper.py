import cv2
from .webpage import Webpage
from .htmlcomponent import HTMLComponent
from .text import TEXT
import numpy as np


class HtmlMapper:
    def __init__(self, classifier):
        self.classifier = classifier;

    def remove_white(self, img):
        # cv2_imshow(img)
        h, w = img.shape[:2]
        whitespace_found = True
        white = np.array([255, 255, 255]);
        # print(white)
        while True:
            h, w = img.shape[:2]
            for i in range(w):
                if np.array_equal(img[0][i], white) == False or np.array_equal(img[h - 1][i], white) == False:
                    # print("True")
                    whitespace_found = False
            if whitespace_found == False:
                break
            else:
                # print("removing white");
                img = img[1:h - 2, 0:w]
        whitespace_found = True
        while True:
            h, w = img.shape[:2]
            # print(h,w)
            for i in range(h):
                if np.array_equal(img[i][0], white) == False or np.array_equal(img[i][w - 1], white) == False:
                    whitespace_found = False
            if whitespace_found == False:
                return img
            else:
                # print("removing white");
                img = img[0:h, 1:w - 2]
        return img

    def ImgToWebpage(self, image, text):

        # Creating instance of Webpage Class
        webpage = Webpage()

        # Storing height and width of image
        hhh, www = image.shape[:2]

        # Creating initial boundary around image
        cv2.rectangle(image, (0, 0), (www, hhh), (255, 255, 255), 10)

        img = self.getBoundariesEnchanced(image.copy())
        img = self.EnhanceInnerSurface(img.copy(), image)

        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(img, 10, 20)
        # cv2.imshow("canny2nd", edged)
        edged = img
        (cnts, h) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        idx = 0
        parentElement = HTMLComponent(-1, -1, -1, -1, -1, 0, '')
        for c, h1 in zip(cnts, h[0]):
            x, y, w, h = cv2.boundingRect(c)
            approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
            if w > 15 and h > 15:  # and len(approx)==4:# and x+w<700 and y+h<700:#15
                idx += 1
                new_img = image[y:y + h, x:x + w]
                # if text:  # and h < 50 and h1[2] == -1 and isText(new_img)):  # has no child
                #     element = TEXT(new_img, x, y, h, w, 0)
                # else:
                #     element = HTMLComponent(new_img, x, y, h, w, 0)
                new_img = self.remove_white(new_img)
                etype = self.classifier.Classify(new_img)

                # -->asim sansi (edit)
                # if(etype=="text"):
                element = HTMLComponent(new_img, x, y, h, w, 0, etype, text)

                # elif(etype=="button"):
                #   element=Button(new_img,x,y,h,w,0)
                # elif(etype=="textbox"):
                #   element=TextBox(new_img,x,y,h,w,0)

                element.set_shape(approx)
                if h1[3] != -1:
                    # if new image is less than 80% of parent image
                    # pshape=parentElement.getImage().shape
                    # newshape=new_img.shape
                    # if(0.4*pshape[0]*pshape[1]>newshape[0]*newshape[1]):
                    parentElement.AddSubElement(element)
                else:
                    parentElement = element;
                    webpage.addElement(element)

        # cv2.imshow('final', minus_img)
        # cv2.waitKey()
        # self.g(image.copy(), webpage)
        return webpage

    def MapHtml(self, webpage, path):
        code = ""
        index = 0
        save_path = path + "images/"  # path provided for saving images
        access_path = "../images/"  # path provided to webpage for later access
        for e in webpage.getelements():
            imname = str(index) + ".png"
            cv2.imwrite(save_path + imname, e.getImage())
            e.setPath(access_path + imname)

            x, y, w, h = e.getAttributes()
            if (len(e.getSubElements()) > 0):
                code += e.StartTag();
                for (i, e1) in enumerate(e.getSubElements()):
                    if (e.tag == "ul"):
                        code += "<li>"
                    imname2 = str(index) + "-" + str(i) + ".png"
                    cv2.imwrite(save_path + imname2, e1.getImage())
                    # x1,y1,w1,h1=e1.getAttributes()
                    e1.setPath(access_path + imname2)
                    code += e1.Code();
                    if (e.tag == "ul"):
                        code += "</li>"
                code += e.CloseTag();
            else:
                code += e.Code()
                # code+="<IMG STYLE=\"position:absolute; TOP:"+str(y1)+"px;LEFT:"+str(x1)+"px; WIDTH:"+str(w1)+"px; HEIGHT:"+str(h1)+"px\" SRC=\""+path1+"\">"

            # code+="<IMG STYLE=\"position:absolute; TOP:"+str(y)+"px;LEFT:"+str(x)+"px; WIDTH:"+str(w)+"px; HEIGHT:"+str(h)+"px\" SRC=\""+ipath+"\">"
            index += 1

        return code

    def getBoundariesEnchanced(self, img):
        # image = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)  # Not Being Used

        edges = cv2.Canny(img.copy(), 10, 20)
        # cv2.imshow("canny", edges)
        #         cv2.waitKey();
        # ret,edges = cv2.threshold(image.copy(), 0, 255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)

        # writing canny results to disk
        cv2.imwrite("fypsite/processor/src/canny.png", edges)  # output file
        # ab = cv2.imread('canny.png')
        # ab = cv2.cvtColor(ab,cv2.COLOR_BGR2GRAY)

        # extracting contours
        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # print ('no of shapes {0}'.format(len(contours)))
        # for cnt in contours:
        #     rect = cv2.minAreaRect(cnt)
        #     box = cv2.boxPoints(rect)
        #     box = np.int0(box)
        #     img = cv2.drawContours(img, [box], 0, (0,255,0), 3)

        for cnt, h1 in zip(contours, hierarchy[0]):
            # epsilon = 0.01*cv2.arcLength(cnt, True)
            # approx = cv2.approxPolyDP(cnt, epsilon, True)
            x, y, w, h = cv2.boundingRect(cnt)
            # if w>10 and h>10:# and h1[3]!=-1:# and w<width and h<height:
            # if(h<20 or w<20):
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
            # img[y:y+h,x:x+w]=255
            # img = cv2.drawContours(img, [approx], 0, (0,255,0),1)
        cv2.imwrite("canny.png", img)
        return img

    # Function accepts Image and returns HTML Code
    def ImgToHtml(self, image, path, text):

        w = self.ImgToWebpage(image, text)
        s = self.MapHtml(w, path)
        return s

    def EnhanceInnerSurface(self, img, omg):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 3))
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
        # cv2.imshow("otsu", thresh1);
        # cv2.imshow("dilation", dilation);
        #         cv2.waitKey();
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        im2 = omg.copy()
        # print(type(contours))
        # return;
        # contours=self.InsersectionCheck(im2,contours)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            # if(h>10 and w>10):
            # fg=img[y:y+h,x:x+w]
            # cv2.imshow("A",fg)
            # cv2.waitKey()
            cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.putText(im2, "component", (x, y), cv2.FONT_HERSHEY_SIMPLEX,0.1, (255,0,0), 1)
        # return thresh1
        cv2.imwrite("otso.png", im2)
        return dilation  # im2
