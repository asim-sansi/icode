

import cv2
import numpy as np
import tensorflow as tf
# global graph
# graph = tf.get_default_graph()

folders = [{'tag': 'a'}, {'tag': 'button'}, {'tag': 'form'}, {'tag': 'img'}, {'tag': 'input', 'type': 'text'}, {'tag': 'ul'}]
#%%
height = 64
width = 64
class ComponentClassifier:
  def __init__(self,model):
    self.model=model
  def Classify(self,image):

    #asim sansi edit
    image = cv2.resize(image, (width, height))
    # scale the pixel values to [0, 1]
    image = image.astype("float") / 255.0

    # when working with a CNN: don't flatten the image, simply add the batch dimension
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))

    # with graph.as_default():
    with tf.Graph().as_default():
      preds = self.model.predict(image)


    # find the class label index with the largest corresponding probability
    #i = preds.argmax(axis=1)[0]
    #label = lb.classes_[i]
    # print(preds)
    probas = np.array(preds)
    labels = np.argmax(probas, axis=-1)
    # print('******  '+folders[labels[0]]+'  ********')
    answer = folders[labels[0]]
    print(answer)




    #clearing previous session for CNN
    return answer


#%%