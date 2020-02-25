import cv2
from .webpage import Webpage
from .htmlcomponent import HTMLComponent
from .text import TEXT
import numpy as np


class HtmlMapper:
    def g(self, image, webpage):
        for e in webpage.getelements():
            x, y, w, h = e.getAttributes()
            cv2.rectangle(image, (x, y), (x + w, y + h), e.getColors()[0], -1)
            cv2.rectangle(image, (x - 1, y - 1), (x + w + 2, y + h + 2), (0, 0, 0), 1)
            cv2.rectangle(image, (x + 5, y + 5), (x + w - 5, y + h - 5), e.getColors()[1], -1)
            for e1 in e.getSubElements():
                x, y, w, h = e1.getAttributes()
                cv2.rectangle(image, (x, y), (x + w, y + h), e1.getColors()[0], -1)
                cv2.rectangle(image, (x - 1, y - 1), (x + w + 2, y + h + 2), (0, 0, 0), 1)
                cv2.rectangle(image, (x + 5, y + 5), (x + w - 5, y + h - 5), e1.getColors()[1], -1)
        cv2.imwrite("Label.png", image)

    def ImageToElements(self, parentElement, text):
        image = parentElement.img

        # Storing height and width of image
        hhh, www = image.shape[:2]

        # Creating initial boundary around image
        cv2.rectangle(image, (0, 0), (www, hhh), (255, 255, 255), www//150)

        img = self.getBoundariesEnchanced(image.copy())
        img = self.EnhanceInnerSurface(img.copy(), image)

        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(img, 10, 20)
        cv2.imshow("canny2nd", edged)
        edged = img
        (cnts, h) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        #h[i] holds info for cnts[i]
        #h[i][0] holds next child in same heiarchy
        #h[i][1] holds previous child in same heiarchy
        #h[i][2] holds first child in next heiarchy
        #h[i][3] holds parent from previous heirarchy
        idx = 0
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
            if w > 15 and h > 15:  # and len(approx)==4:# and x+w<700 and y+h<700:#15
                idx += 1
                new_img = image[y:y + h, x:x + w]
                if text:  # and h < 50 and h1[2] == -1 and isText(new_img)):  # has no child
                    element = TEXT(new_img, x, y, h, w, 0)
                else:
                    element = HTMLComponent(new_img, x, y, h, w, 0)

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


    def ElementFromContour(self, text, image, c):
        x, y, w, h = cv2.boundingRect(c)
        approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
        """w > 15 and h > 15"""
        if 1:
            new_img = image[y:y + h, x:x + w]
            element = HTMLComponent(new_img, x, y, h, w, 0)

            element.set_shape(approx)
            return element
        else:
            return None

    def ImgToWebpage(self, image, text):

        # Creating instance of Webpage Class
        webpage = Webpage()

        # Storing height and width of image
        hhh, www = image.shape[:2]

        # Creating initial boundary around image
        cv2.rectangle(image, (0, 0), (www, hhh), (255, 255, 255), www//150)

        img = self.getBoundariesEnchanced(image.copy())
        img = self.EnhanceInnerSurface(img.copy(), image)

        # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edged = cv2.Canny(img, 10, 20)
        cv2.imshow("canny2nd", edged)
        edged = img
        (cnts, h) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        parentElement = HTMLComponent(image, -1, -1, -1, -1, 0)
        webpage.addElement(parentElement)
        idx = 0
        for c, h1 in zip(cnts, h[0]):
            element = self.ElementFromContour(text, image, c)
            webpage.addElement(element)
            idx += 1
        idx = 1
        for h1 in h[0]:
            if h1[3] == -1:
                parentElement.AddSubElement(webpage.elements[idx])
            else:
                webpage.elements[h1[3]].AddSubElement(webpage.elements[idx])
            idx += 1


        # element_array = webpage.elements.copy()
        # for element in element_array:
        #     if element.w < 15 and element.h < 15:
        #         for sub in element.sub:
        #             webpage.elements.remove(sub)
        #         webpage.elements.remove(element)
        #     else:
        #         print(element.sub)
        # cv2.imshow('final', minus_img)
        # cv2.waitKey()
        self.g(image.copy(), webpage)
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
            code += e.Code()
            x, y, w, h = e.getAttributes()
            for (i, e1) in enumerate(e.getSubElements()):
                imname2 = str(index) + "-" + str(i) + ".png"
                cv2.imwrite(save_path + imname2, e1.getImage())
                # x1,y1,w1,h1=e1.getAttributes()
                e1.setPath(access_path + imname2)
                code += e1.Code();

            index += 1

        return code

    def getBoundariesEnchanced(self, img):
        # image = cv2.cvtColor(img.copy(), cv2.COLOR_BGR2GRAY)  # Not Being Used

        edges = cv2.Canny(img.copy(), 10, 20)
        # cv2.imshow("canny", edges)
        #         cv2.waitKey();
        # ret,edges = cv2.threshold(image.copy(), 0, 255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)

        # writing canny results to disk
        cv2.imwrite("canny.png", edges)  # output file
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
        cv2.imshow("otsu", thresh1);
        cv2.imshow("dilation", dilation);
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
