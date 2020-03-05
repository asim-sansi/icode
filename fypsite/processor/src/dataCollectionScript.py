# # HTML element data collection script
# # Auther- Asim Sansi
# # Date : 8-DEcEMBER-2019


from selenium import webdriver
from selenium.common import exceptions

driver = webdriver.Firefox()

''' URL's '''
file = open("A:\FYP\script\\urls.txt", "r")
urls = file.readlines()

p = 0
for k in urls:

    try:
        driver.get(k)
        driver.maximize_window()

        HTML_Elements = ["p"]
        # notice = driver.find_element_by_xpath ("//a[@class='s-btn s-btn__muted s-btn__icon js-notice-close']")
        # notice.click()

        for j in HTML_Elements:
            elements = driver.find_elements_by_tag_name(j)
            type = ""
            threshold = 0
            for i in elements:
                try:
                    threshold +=1
                    if threshold == 250:
                        break
                    if (j == 'input'):
                        type = '/' + str(i.get_attribute("type"))
                    if (i.rect['width'] != 0 and i.rect['height'] != 0):
                        i.screenshot(
                            "A:\FYP\script\data\\" + j + type + "\\bla" + str(p) + "-" + str(i.rect['x']) + "-" + str(i.rect['y']) + "-"
                            + str(i.rect['width']) + "-" + str(i.rect['height']) + ".png")
                        p += 1
                        type = ""
                except exceptions.StaleElementReferenceException:
                    pass
    except exceptions.WebDriverException:
            pass

driver.quit()




















































# location = element.location;
# size = element.size;
#
# driver.save_screenshot("data/image.png");
# print (element.rect)
# element.screenshot('data/bla.png')
# size = element.size
# x = location['x'];
# y = location['y'];
#
# width = location['x']+(size['width'] * pixel_ratio);
# height = location['y']+(size['height'] * pixel_ratio);

# im = Image.open('data/image.png')
# im = im.crop((int(x), int(y), int(width), int(height)))
# im.save('data/image1.png')










#
# import cv2
# from math import ceil
# from selenium import webdriver
# from PIL import Image
# import PIL.ImageOps
# import time
# import numpy as np
#
# fox = webdriver.Firefox()
# fox.get('https://www.google.com/')
# fox.maximize_window()
# pixel_ratio = fox.execute_script("return window.devicePixelRatio")
#
# time.sleep(5)
# fox.save_screenshot('data/main.png')
# main = cv2.imread('data/main.png')
#
# i = fox.find_element_by_class_name('iblpc')
#
# j=0
# # for i in element:
#
# # print (i.rect)
# # x = int(ceil(i.rect['x']))
# # y = int(ceil(i.rect['y']))
# # w = int((ceil(i.rect['width'])) * pixel_ratio)
# # h = int((ceil(i.rect['height'])) * pixel_ratio)
# # print (x, y, x+w, y+h)
# #
# # crop_image = main[y:(y+h), x:(x+w)]
# # cv2.imshow("bla", crop_image)
# # cv2.waitKey(0)
#
# j+=1
# # img = Image.open('data/bla.png')
# # # img.show()
#
# fox.quit()









# # trim selenium screen shot inspired from stackoverlow
# # http://stackoverflow.com/questions/15018372/how-to-take-partial-screenshot-with-selenium-webdriver-in-python
#
# im = Image.open('weather_mn.png')
#
# left = location['x']
# top = location['y']
# # dimensions added to capture just widget area
# right = location['x'] + 500
# bottom = location['y'] + 245
#
# im = im.crop((left, top, right, bottom)) # defines crop points
#
# im = im.convert("RGB")
# im = PIL.ImageOps.invert(im)
#
# im = im.convert("RGBA")
# datas = im.getdata()
#
#
# # make portions of image transparent inspired from stackoverflow by cr333
# # http://stackoverflow.com/questions/765736/using-pil-to-make-all-white-pixels-transparent
#
# newData = []
# for item in datas:
#
#     if item[0] == 0 and item[1] == 0 and item[2] == 0:
#         newData.append((255, 255, 255, 0))
#     else:
#         newData.append(item)
#
# im.putdata(newData)
#
# # replace colors based on stackoverflow from Joe Kington
# # http://stackoverflow.com/questions/3752476/python-pil-replace-a-single-rgba-color
#
# data = np.array(im)   # "data" is a height x width x 4 numpy array
# red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
#
# white_areas = (red == 0) & (blue == 0) & (green == 0)
# data[..., :-1][white_areas] = (255, 255, 255)
#
# im2 = Image.fromarray(data)
#
# im2.save("weather_mn_desktop.png", "PNG")






























#
# from selenium import webdriver
# from PIL import Image
# from io import BytesIO
#
# fox = webdriver.Firefox()
# fox.get('https://www.google.com/')
# fox.maximize_window()
#
# # now that we have the preliminary stuff out of the way time to get that image :D
# i = fox.find_element_by_class_name('iblpc') # find part of the page you want image of
# # print(len(element))
#
# pixel_ratio = fox.execute_script("return window.devicePixelRatio")
# png = fox.get_screenshot_as_png()  # saves screenshot of entire page
# img = Image.open(BytesIO(png))
# img.show()
#
# p = 0
# # for i in element:
# location = i.location
# size = i.size
# im = Image.open(BytesIO(png)) # uses PIL library to open image in memory
# left = location['x']
# top = location['y']
# right = location['x'] + size['width'] * pixel_ratio
# bottom = location['y'] + size['height'] * pixel_ratio
# print(left, top, right, bottom)
#
# im = im.crop((left, top, right, bottom)) # defines crop points
# output = '%s/%s.png' % ('data', 'link' + str(p))
# print(p)
# im.save(output) # saves new cropped image
# p+=1
#
# fox.quit()

