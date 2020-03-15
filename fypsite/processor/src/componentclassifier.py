

import cv2
import numpy as np
import tensorflow as tf
from keras.models import load_model
graph = tf.get_default_graph()

#1st CNN model
# folders = [{'tag': 'a'}, {'tag': 'button'}, {'tag': 'form'}, {'tag': 'img'},
#            {'tag': 'input', 'type': 'text'},
#            {'tag': 'ul'}]
#
# #2nd CNN model
# # folders = [{'tag': 'a'}, {'tag': 'button'}, {'tag': 'form'},{'tag': 'i'}, {'tag': 'img'},
# #            {'tag': 'input', 'type': 'checkbox'}, {'tag': 'input', 'type': 'radio'},
# #            {'tag': 'input', 'type': 'text'}, {'tag': 'p'},
# #            {'tag': 'ul'}]

# 3rd CNN model

class ComponentClassifier:
  def __init__(self, model):
    self.model = model
  def Classify(self,image):

    #asim sansi edit
    image = cv2.resize(image, (64, 64))
    # scale the pixel values to [0, 1]
    image = image.astype("float") / 255.0

    # when working with a CNN: don't flatten the image, simply add the batch dimension
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

    with graph.as_default():
      preds = self.model.predict(image)


    probas = np.array(preds)
    print(probas)
    labels = np.argmax(probas, axis=-1)
    print(labels)
    answer = folders[labels[0]]
    print(answer)
    print(probas[0][labels[0]])
    # if(probas[0][labels[0]]>=0.6):
    #   return answer.copy()
    # return {'tag':'div'}

    return answer.copy()

folders = [{'tag': 'a'}, {'tag': 'button'}, {'tag': 'form'}, {'tag': 'i'}, {'tag': 'img'},
           {'tag': 'input', 'type': 'text'}, {'tag': 'p'},
           {'tag': 'ul'}]


height = 64
width = 64
#
# i=cv2.imread(r"E:\ICode\icode\fypsite\processor\static\generated_resources\images\1125-126.png")
# loaded_model = load_model(r"E:\ICode\icode\fypsite\processor\CNN_model\third_CNN_model")
# c=ComponentClassifier(loaded_model)
# c.Classify(i);
#
# edged = cv2.Canny(i.copy(), 10, 20)
# cv2.imshow("canny2nd", edged)
# cv2.waitKey()