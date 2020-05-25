import cv2
from .webpage import Webpage
from .htmlcomponent import HTMLComponent
from .text import TEXT
import numpy as np


class HtmlMapper:
    def __init__(self, classifier):
        self.classifier = classifier;
        self.component_number=1

    def remove_white(self, img):
        # cv2_imshow(img)
        h, w = img.shape[:2]
        whitespace_found = True
        white = np.array([255, 255, 255]);
        # print(white)
        h, w = img.shape[:2]
        while h>1 and w>1:
            h, w = img.shape[:2]
            for i in range(w):
                if np.array_equal(img[0][i], white) == False or np.array_equal(img[h - 1][i], white) == False:
                    # print("True")
                    whitespace_found = False
            if whitespace_found == False:
                break
            else:
                # print("removing white");
                img = img[1:h - 1, 0:w]
                h, w = img.shape[:2]
        whitespace_found = True
        while h>1 and w>1:
            h, w = img.shape[:2]
            # print(h,w)
            for i in range(h):
                if np.array_equal(img[i][0], white) == False or np.array_equal(img[i][w - 1], white) == False:
                    whitespace_found = False
            if whitespace_found == False:
                return img
            else:
                # print("removing white");
                img = img[0:h, 1:w - 1]
                h, w = img.shape[:2]
        return img


    # creates an element from an image
    def element_from_contour(self, text, image, c, parent):
        x, y, w, h = cv2.boundingRect(c)
        if w == parent.w and h == parent.h:
            return 0
        approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
        """w > 15 and h > 15"""
        if w > 15 and h > 15:
            new_img = image[y:y + h, x:x + w]
            #new_img_c=self.remove_white(new_img.copy())
            element_type = self.classifier.Classify(new_img)
            # cv2.imshow(element_type,new_img)#showing image with label for debugging
            # cv2.waitKey()
            # if parent.attributes['tag'] == "input" and element_type == 'a':
            #     return 0
            element = HTMLComponent(new_img, x, y, h, w, element_type,self.component_number, parent, text)
            self.component_number+=1
            if element.attributes['tag'] != "i":
                element.set_shape(approx)

            return element
        else:
            return 0


    def image_to_elements(self, parentElement, options):
        image = parentElement.img
        # Storing height and width of image
        hhh, www = image.shape[:2]
        img=image.copy()
        if parentElement.attributes['tag'] == "body":
            # Creating initial boundary around image
            cv2.rectangle(image, (0, 0), (www, hhh), (255, 255, 255), www // 150)
            #image=cv2.copyMakeBorder(image,2,2,2,2,cv2.BORDER_CONSTANT)
        #
        # kernel_sharpening = np.array([[-1, -1, -1],
        #                               [-1, 9, -1],
        #                               [-1, -1,
        #                                -1]])  # applying the sharpening kernel to the input image & displaying it.
        # img = cv2.filter2D(img, -1, kernel_sharpening)
        img = self.getBoundariesEnchanced(image.copy())
        img = self.EnhanceInnerSurface(img.copy(), image)

        edged = cv2.Canny(img.copy(), 10, 20)
        # cv2.imshow("canny2nd", edged)
        # edged = img
        # cv2.imshow("", img)
        # cv2.waitKey()

        (contours, h) = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        #h[i] holds info for cnts[i]
        #h[i][0] holds next child in same heiarchy
        #h[i][1] holds previous child in same heiarchy
        #h[i][2] holds first child in next heiarchy
        #h[i][3] holds parent from previous heirarchy
        idx = 0
        print(len(contours))
        for c in contours:
            if parentElement.attributes['tag'] == "body":
                idx += 1
                options['comm-channel'].put(10 + int((idx/len(contours))*65))
            element = self.element_from_contour(options['text-type'], image, c, parentElement)
            if element != 0:
                if element.attributes['tag'] not in ["button", "a", "img", "p", "i"]:
                    element = self.image_to_elements(element, options)
                    if element.attributes['tag'] in ["input", "button"]:
                        sub_tags = [child.attributes['tag'] for child in element.sub]
                        #make div if found same tag nested
                        if element.attributes['tag'] in sub_tags and len(element.sub)>1:
                            element.attributes['tag'] = "div"
                        else:
                            element.sub.clear()

                    if element.attributes['tag'] == 'form':
                        sub_tags = [child.attributes['tag'] for child in element.sub]
                        if 'form' in sub_tags:
                            element.attributes['tag'] = "div"
                            element.sub = [item for item in element.sub if item.attributes['tag'] == 'form']


                parentElement.AddSubElement(element)

        return parentElement

    def ImgToWebpage(self, image, text):

        # Creating instance of Webpage Class
        webpage = Webpage()

        # Storing height and width of image
        hhh, www = image.shape[:2]

        # Creating initial boundary around image
        cv2.rectangle(image, (0, 0), (www, hhh), (255, 255, 255), www//150)

        img = self.getBoundariesEnchanced(image.copy())
        img = self.EnhanceInnerSurface(img.copy(), image)

        edged = cv2.Canny(img, 10, 20)
        cv2.imshow("canny2nd", edged)
        edged = img

        (cnts, h) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        parentElement = HTMLComponent(image, -1, -1, -1, -1, "body",self.component_number, 0)
        self.component_number+=1
        webpage.addElement(parentElement)
        idx = 0
        #h[i] holds info for cnts[i]
        #h[i][0] holds next child in same heiarchy
        #h[i][1] holds previous child in same heiarchy
        #h[i][2] holds first child in next heiarchy
        #h[i][3] holds parent from previous heirarchy
        for c, h1 in zip(cnts, h[0]):
            element = self.element_from_contour(text, image, c)
            webpage.addElement(element)
            idx += 1
        idx = 1
        for h1 in h[0]:
            if h1[3] == -1:
                parentElement.AddSubElement(webpage.elements[idx])
            else:
                webpage.elements[h1[3]].AddSubElement(webpage.elements[idx])
            idx += 1

        return webpage


    #
    # def ImgToWebpage(self, image, text):
    #
    #     # Creating instance of Webpage Class
    #     webpage = Webpage()
    #
    #     # Storing height and width of image
    #     hhh, www = image.shape[:2]
    #
    #     # Creating initial boundary around image
    #     cv2.rectangle(image, (0, 0), (www, hhh), (255, 255, 255), 10)
    #
    #     img = self.getBoundariesEnchanced(image.copy())
    #     img = self.EnhanceInnerSurface(img.copy(), image)
    #
    #     # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #     edged = cv2.Canny(img, 10, 20)
    #     # cv2.imshow("canny2nd", edged)
    #     edged = img
    #     (cnts, h) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #     idx = 0
    #     parentElement = HTMLComponent(-1, -1, -1, -1, -1, 0, '')
    #     for c, h1 in zip(cnts, h[0]):
    #         x, y, w, h = cv2.boundingRect(c)
    #         approx = cv2.approxPolyDP(c, 0.01 * cv2.arcLength(c, True), True)
    #         if w > 15 and h > 15:  # and len(approx)==4:# and x+w<700 and y+h<700:#15
    #             idx += 1
    #             new_img = image[y:y + h, x:x + w]
    #             # if text:  # and h < 50 and h1[2] == -1 and isText(new_img)):  # has no child
    #             #     element = TEXT(new_img, x, y, h, w, 0)
    #             # else:
    #             #     element = HTMLComponent(new_img, x, y, h, w, 0)
    #             new_img = self.remove_white(new_img)
    #             etype = self.classifier.Classify(new_img)
    #
    #             # -->asim sansi (edit)
    #             # if(etype=="text"):
    #             element = HTMLComponent(new_img, x, y, h, w, 0, etype, text)
    #
    #             # elif(etype=="button"):
    #             #   element=Button(new_img,x,y,h,w,0)
    #             # elif(etype=="textbox"):
    #             #   element=TextBox(new_img,x,y,h,w,0)
    #
    #             element.set_shape(approx)
    #             if h1[3] != -1:
    #                 # if new image is less than 80% of parent image
    #                 # pshape=parentElement.getImage().shape
    #                 # newshape=new_img.shape
    #                 # if(0.4*pshape[0]*pshape[1]>newshape[0]*newshape[1]):
    #                 parentElement.AddSubElement(element)
    #             else:
    #                 parentElement = element;
    #                 webpage.addElement(element)
    #
    #     # cv2.imshow('final', minus_img)
    #     # cv2.waitKey()
    #     # self.g(image.copy(), webpage)
    #     return webpage
    def MapGrid(self,element,code,path,options,cssCode,level=0):#experimental
        another_path = "processor/static/generated_resources/"
        save_path = path + "images/"  # path provided for saving images
        access_path = "images/"  # path provided to webpage for later access
        imname = str(element.x) + '-' + str(element.y) + element.attributes['tag'] + ".png"
        cssCode += element.getCSSCode()
        cv2.imwrite(save_path + imname, element.getImage())
        cv2.imwrite(another_path + "images/" + imname, element.getImage())
        if options['image-type'] == 0:
            imname = "default_image.png"
        if element.attributes['tag'] == 'img':
            element.attributes['src'] = access_path + imname
        if element.attributes['tag'] == 'i':
            element.styles['background'] = "url(" + access_path + imname + ")"
        element.PopulateGrid()
        code+= element.StartTag()
        cssCode+= element.getCSSCode()
        if (len(element.sub) == 0):
            code += element.innerHTML
        else:
            for i in range(element.rows):
                code += (level*"\t")+"<div class='row'>\n"
                for j in range(element.cols):
                    if (element.grid[i][j] == 0):
                        code += (level*"\t")+"\t<div class='col-sm-1'></div>\n"
                        continue
                    if (element.grid[i][j] == 1):
                        continue
                    code += "<div class='col-sm-" + str(element.grid[i][j].col_size) + "'>\n"
                    code, cssCode = self.MapGrid(element.grid[i][j],code,path,options,cssCode,level+1)
                    code += "</div>\n"
                code += "</div>\n"

        code += element.CloseTag();
        return code, cssCode
    def map_dom_tree(self, element, code, path, options,cssCode, level=0):
        another_path = "processor/static/generated_resources/"
        save_path = path + "images/"  # path provided for saving images
        access_path = "images/"  # path provided to webpage for later access
        imname = str(element.x) + '-' + str(element.y) + element.attributes['tag']+".png"
        cssCode+=element.getCSSCode()
        cv2.imwrite(save_path + imname, element.getImage())
        cv2.imwrite(another_path + "images/" + imname, element.getImage())
        if options['image-type'] == 0:
            imname = "default_image.png"
        if element.attributes['tag'] == 'img':
            element.attributes['src'] = access_path + imname
        if element.attributes['tag'] == 'i':
            element.styles['background'] = "url(" + access_path + imname + ")"
        #element.SetupGrid()
        code += '\t' *level
        code += element.StartTag()
        idx = 0
        for item in element.sub:
            code,cssCode = self.map_dom_tree(item, code, path, options,cssCode, level+1)
            if level == 0:
                idx += 1
                options['comm-channel'].put(75 + int((idx/len(element.sub))*20))
        if len(element.sub) == 0:
            code += '\t' * (level+1)
            code += element.innerHTML + '\n'
            code += '\t' * (level+1)
        code = code[:len(code)-1]
        code += element.CloseTag()
        return code,cssCode

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
                code += e.StartTag()
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

        if hierarchy is None:
            return img

        for cnt, h1 in zip(contours, hierarchy[0]):
            # epsilon = 0.01*cv2.arcLength(cnt, True)
            # approx = cv2.approxPolyDP(cnt, epsilon, True)
            x, y, w, h = cv2.boundingRect(cnt)
            # if w>10 and h>10:# and h1[3]!=-1:# and w<width and h<height:
            # if(h<20 or w<20):
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 2)
            # img[y:y+h,x:x+w]=255
            # img = cv2.drawContours(img, [approx], 0, (0,255,0),1)
        cv2.imwrite("canny.png", img)
        return img


    # Function accepts Image and returns HTML Code

    def ImgToHtml(self, image, path, options):

        # w = self.ImgToWebpage(image, text)
        # s = self.MapHtml(w, path)

        parentElement = HTMLComponent(image, -1, -1, -1, -1, {"tag": "body"},self.component_number, None, options['text-type'])
        self.component_number+=1
        parentElement.styles["padding"] = "0"
        parentElement.styles["margin"] = "0"
        # parentElement.styles["font-size"] = "13px"
        options['comm-channel'].put(4)
        parentElement = self.image_to_elements(parentElement, options)
        options['comm-channel'].put(75)
        #s,css = self.map_dom_tree(parentElement, "", path, options,"", 0)
        s, css = self.MapGrid(parentElement, "", path, options, "", 0)
        s="<head><link rel='stylesheet' href='styles.css'>" \
          "<link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css'></head>"+s
        return s,css

    def EnhanceInnerSurface(self, img, omg):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)

        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 3))
        dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
        # cv2.imshow("otsu", thresh1);
        # cv2.imshow("dilation", dilation);
        #         cv2.waitKey();
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
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
