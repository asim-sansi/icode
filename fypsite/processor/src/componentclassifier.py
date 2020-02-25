import cv2
import numpy as np

height = 28
width = 28

class ComponentClassifier:
    def __init__(self, model):
        self.model = model

    def Classify(self, img1):
        cv2.imshow(img1)
        img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        img1 = cv2.resize(img1, (height, width))
        img1 = img1[..., ::-1].astype(np.float32)
        #    img1 = img1.img_to_array(img1)
        img1 = img1 / 255
        # img1=img1.reshape(height,width,1)
        img1 = img1.reshape(1, -1)
        # img1=np.array([img1])
        print(img1.shape)
        answer = (self.model.predict(img1)[0])
        # print(answer)
        if answer == 0:
            answer = "button"
        if answer == 1:
            answer = "textbox"
        if answer == 2:
            answer = "text"
        print(answer)
        return answer
