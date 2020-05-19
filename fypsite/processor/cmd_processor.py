from PIL import Image
from queue import Queue
from .src import processor as en
def Run():
    comm_channel = Queue()
    another_path = r"E:\ICode\icode\fypsite\processor\static\templates/"
    imgName="ask.png"
    while imgName!="exit":
        image = Image.open(another_path+imgName)
        dict = {
            "comm-channel": comm_channel,
            "text-type": 1,
            "image-type": 1,


            "use_defaults": ""
        }
        en.main([image,dict]);
        imgName=input("Enter Image Name from Template(exit to stop):")

