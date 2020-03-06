

import cv2
import numpy as np
import tensorflow as tf
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
folders = [{'tag': 'a'}, {'tag': 'button'}, {'tag': 'form'}, {'tag': 'i'}, {'tag': 'img'},
           {'tag': 'input', 'type': 'text'}, {'tag': 'p'},
           {'tag': 'ul'}]


height = 64
width = 64
class ComponentClassifier:
  def __init__(self, model):
    self.model = model
  def Classify(self,image):

    #asim sansi edit
    image = cv2.resize(image, (width, height))
    # scale the pixel values to [0, 1]
    image = image.astype("float") / 255.0

    # when working with a CNN: don't flatten the image, simply add the batch dimension
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

    with graph.as_default():
      preds = self.model.predict(image)


    probas = np.array(preds)
    labels = np.argmax(probas, axis=-1)
    answer = folders[labels[0]]
    print(answer)

    return answer.copy()
