#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
# import pytesseract
import cv2 
import sys
import numpy as np
import shutil
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


# In[2]:
from prompt_toolkit.key_binding.bindings.named_commands import self_insert


class HTMLComponent:
    def  __init__(self,img,x,y,h,w,cnt):
        self.img=img
        self.x=x
        self.y=y
        self.h=h
        self.w=w
        self.cnt=cnt
        self.path=""
        self.sub=[]#sub elements
    def setImage(self,img):
        self.img=img
    def setCoordinates(self,x,y):
        self.x=x
        self.y=y
    def AddSubElement(self,e):
        self.sub.append(e);
    def getSubElements(self):
        return self.sub;
    def getImage(self):
        return self.img
    def getCorrdinates(self):
        return self.x,self.y
    def getAttributes(self):
        return self.x,self.y,self.w,self.h
    def setPath(self,p):
        self.path=p;
    def Code(self):
        code="<IMG STYLE=\"position:absolute; TOP:"+str(self.y)+"px;LEFT:"+str(self.x)+"px; WIDTH:"+str(self.w)+"px; HEIGHT:"+str(self.h)+"px\" SRC=\""+self.path+"\">"
        return code;
    
    


# In[3]:

#
# def isText(img):
#     if(len(pytesseract.image_to_string(img))>3):
#         return True
#     return False
# class TEXT(HTMLComponent):
#     def __init__(self,img,x,y,h,w,p):
#         super().__init__(img,x,y,h,w,p)
#         self.txt=" "
#         self.type=" "
#         self.link=False;
#
#         if(h>30):
#
#             self.type="p"
#         elif(h>24):
#
#             self.type="h2"
#         #else:
#         else:
#             self.type="p"
#         #self.LinkCheck()
#         #print(self.type)
#     def setPath(self,p):
#         super().setPath(p)
#     def LinkCheck(self):
#         img = cv2.cvtColor(super().getImage(), cv2.COLOR_BGR2RGB)
#         im_pil = Image.fromarray(img)
#         #im_np = np.asarray(im_pil)
#         self.link=BlueCheck(im_pil)
#         print(self.link)
#         self.type="a"
#     def translateText(self):
#         self.txt=(pytesseract.image_to_string(super().getImage()))
#         return self.txt
#     def Code(self):
#         x,y=super().getCorrdinates()
#         code="<"+self.type
#         code+=r' STYLE="position:absolute; TOP:'+str(y)+"px;LEFT:"+str(x)+"px;\""
#         if(self.link):
#             code+="href=\"a.html\""
#         code+=">";
#         code+=self.translateText();
#         code+="</"+self.type+">";
#         return code
#

# In[4]:


class Webpage:
    def __init__(self):
        self.elements=[]
    def addElement(self,e):
        self.elements.append(e);
    def setElements(self, e):
        self.elements = e
    def getelements(self):
        return self.elements



# In[5]:


def contourIntersect(original_image, contour1, contour2):
    # Two separate contours trying to check intersection on
    contours = [contour1, contour2]

    # Create image filled with zeros the same size of original image
    blank = np.zeros(original_image.shape[0:2])
    blank2 = np.zeros(original_image.shape[0:2])
    # Copy each contour into its own image and fill it with '1'
    x,y,w,h = cv2.boundingRect(contour1)      
    cv2.rectangle(blank, (x, y), (x + w, y + h), 1, 1)
    #image1 = cv2.drawContours(blank.copy(), contours, 0, 1)
    #image2 = cv2.drawContours(blank.copy(), contours, 1, 1)
    x,y,w,h = cv2.boundingRect(contour2)      
    cv2.rectangle(blank2, (x, y), (x + w, y + h), 1, 1)
    # Use the logical AND operation on the two images
    # Since the two images had bitwise and applied to it,
    # there should be a '1' or 'True' where there was intersection
    # and a '0' or 'False' where it didnt intersect
    intersection = np.logical_and(blank, blank2)

    # Check if there was a '1' in the intersection
    return intersection.any()


# In[6]:


class HtmlMapper:
    def ImgToWebpage(self,image,text):
        webpage=Webpage()
        
        hhh, www = image.shape[:2]
        cv2.rectangle(image, (0,0), (www,hhh), (255,255,255), 10)
        #cv2.imshow("image",image)
        img=image.copy();
        img=self.getBoundariesEnchanced(image.copy())
        img=self.EnhanceInnerSurface(img.copy(),image)
       
      # gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
        edged = cv2.Canny(img, 10, 20)
        cv2.imshow("canny2nd",edged)
        edged=img
        (cnts, h) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        idx = 0
        parentElement=HTMLComponent(-1,-1,-1,-1,-1,0)
        for c,h1 in zip(cnts,h[0]):
            x,y,w,h = cv2.boundingRect(c)
            approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)
            if w>15 and h>15: #and len(approx)==4:# and x+w<700 and y+h<700:#15
                idx+=1
                new_img=image[y:y+h,x:x+w]
                if( text==True and h<50 and h1[2]==-1 and isText(new_img)):#has no child
                    element=TEXT(new_img,x,y,h,w,0)
                else:
                    element=HTMLComponent(new_img,x,y,h,w,0)
                if(h1[3]!=-1):
                    #if new image is less than 80% of parent image
                    #pshape=parentElement.getImage().shape
                    #newshape=new_img.shape
                    #if(0.4*pshape[0]*pshape[1]>newshape[0]*newshape[1]):
                    parentElement.AddSubElement(element)
                else:
                    parentElement=element;
                    webpage.addElement(element)
                    
        #cv2.imshow('final', minus_img)
        #cv2.waitKey()
        return webpage  
    def MapHtml(self,webpage,path):
        code=""
        index=0
        for e in webpage.getelements():
            path = r'C:/Users/Asim_Sansi/Desktop/icode_FYP/icode/generated_resources/images/'
            ipath=path+str(index)+".png"
            e.setPath(ipath)
            cv2.imwrite(path+str(index)+".png",e.getImage())
            x,y,w,h=e.getAttributes()
            for (i,e1) in enumerate(e.getSubElements()):
                path1=path+str(index)+"-"+str(i)+".png"
                cv2.imwrite(path1,e1.getImage())
                #x1,y1,w1,h1=e1.getAttributes()
                e1.setPath(path1)
                code+=e1.Code();
                #code+="<IMG STYLE=\"position:absolute; TOP:"+str(y1)+"px;LEFT:"+str(x1)+"px; WIDTH:"+str(w1)+"px; HEIGHT:"+str(h1)+"px\" SRC=\""+path1+"\">"
            code+=e.Code()
            #code+="<IMG STYLE=\"position:absolute; TOP:"+str(y)+"px;LEFT:"+str(x)+"px; WIDTH:"+str(w)+"px; HEIGHT:"+str(h)+"px\" SRC=\""+ipath+"\">"
            index+=1

        return code
    def getBoundariesEnchanced(self,img):
        
        #img = cv2.imread('stack.png')
        image = cv2.cvtColor(img.copy(),cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(img.copy(),10,20)
        cv2.imshow("canny",edges);
#         cv2.waitKey();
        #ret,edges = cv2.threshold(image.copy(), 0, 255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)
        cv2.imwrite("canny.png",edges)#output file
        #ab = cv2.imread('canny.png')
        #ab = cv2.cvtColor(ab,cv2.COLOR_BGR2GRAY)

        contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #print ('no of shapes {0}'.format(len(contours)))
        # for cnt in contours:
        #     rect = cv2.minAreaRect(cnt)
        #     box = cv2.boxPoints(rect)
        #     box = np.int0(box)
        #     img = cv2.drawContours(img, [box], 0, (0,255,0), 3)
        cntlist=[]
        for cnt,h1 in zip(contours,hierarchy[0]):
            #epsilon = 0.01*cv2.arcLength(cnt, True)
            #approx = cv2.approxPolyDP(cnt, epsilon, True)
            x,y,w,h = cv2.boundingRect(cnt)
            #if w>10 and h>10:# and h1[3]!=-1:# and w<width and h<height:
            #if(h<20 or w<20):
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), 1)
                #img[y:y+h,x:x+w]=255
            #img = cv2.drawContours(img, [approx], 0, (0,255,0),1)
        cv2.imwrite("canny.png",img)
        return img

    def ImgToHtml(self,image,path,text):
        
        w=self.ImgToWebpage(image,text)
        s=self.MapHtml(w,path)
        return s;
    def InsersectionCheck(self,img,cnt):
        for i,c in enumerate(cnt):
            x, y, w, h = cv2.boundingRect(c)
            if(h<10 or w<10):
                cnt.pop(i)
        for a,c in enumerate(cnt):
            for j,c1 in enumerate(cnt):
                if(contourIntersect(img,c,c1)):
                    cnt.pop(a)
                    break
        return cnt
    def EnhanceInnerSurface(self,img,omg):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  
        ret,thresh1 = cv2.threshold(gray, 0, 255,cv2.THRESH_OTSU|cv2.THRESH_BINARY_INV)
       
        rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (12, 3))
        dilation = cv2.dilate(thresh1, rect_kernel, iterations = 1)
        cv2.imshow("otsu",thresh1);
        cv2.imshow("dilation",dilation);
#         cv2.waitKey();
        contours, hierarchy = cv2.findContours(dilation, cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        im2 = omg.copy()
       # print(type(contours))
        #return;
        #contours=self.InsersectionCheck(im2,contours)
        for cnt in contours:
            x, y, w, h = cv2.boundingRect(cnt)
            #if(h>10 and w>10):
                #fg=img[y:y+h,x:x+w]
                #cv2.imshow("A",fg)
                #cv2.waitKey()
            cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
                
        #return thresh1
        cv2.imwrite("otso.png",im2)
        return dilation#im2


# In[ ]:


def main(arg):
    #p=arg[0]
    #imgname=arg[1]
    #flush()
    OCR_INTEGRATION=False;#set true to use OCR
    p="../generated_resources/webpages/"
    imgname="../resources/flex.png"#change this with the path of image
    i = cv2.imread(imgname)
#     cv2.imshow("bla", i)
    h=HtmlMapper()
    code=h.ImgToHtml(i,p,OCR_INTEGRATION)
    file=open(p+"webpage.html","w+")
    file.write(code)
    file.close()
    os.system("start \"\" "+p+"webpage.html\"")
    cv2.waitKey();
if __name__ == "__main__":
    main(sys.argv[1:])  
    
        


# In[ ]:


# def flush():
#     shutil.rmtree(r'C:\Users\Dell\Desktop\icode\generated_resources\images/')
#     os.mkdir(r'C:\Users\Dell\Desktop\icode\generated_resources\images')


# In[ ]:


# a=[5]
# type(a)


# In[ ]:




