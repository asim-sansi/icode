

import cv2
import numpy as np

folders = ['a href=\"\"', 'button', 'form', 'img', 'input type=\"text\"', 'ul']
#%%
height=64
width=64
class ComponentClassifier:
  def __init__(self,model):
    self.model=model
  def Classify(self,image):
    # cv2_imshow(image)
#     # img1=cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
#     img1= cv2.resize(img1, (height, width))
#     img1= img1[...,::-1].astype(np.float32)
# #    img1 = img1.img_to_array(img1)
#     img1 = img1/255
#     #img1=img1.reshape(height,width,1)
#     img1=img1.reshape(1,-1)
#     #img1=np.array([img1])
#     print(img1.shape)
#     answer=(self.model.predict(img1)[0])
    #print(answer)



    #asim sansi edit
    image = cv2.resize(image, (width, height))
    # scale the pixel values to [0, 1]
    image = image.astype("float") / 255.0

    # when working with a CNN: don't flatten the image, simply add the batch dimension
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

    preds = self.model.predict(image)

    # find the class label index with the largest corresponding probability
    #i = preds.argmax(axis=1)[0]
    #label = lb.classes_[i]
    print(preds)
    probas = np.array(preds)
    labels = np.argmax(probas, axis=-1)
    # print('******  '+folders[labels[0]]+'  ********')
    answer = folders[labels[0]]

    # if(answer==0):
    #   answer="button"
    # if(answer==1):
    #   answer="textbox"
    # if(answer==2):
    #   answer="text"
    # print(answer)
    return answer


#%%