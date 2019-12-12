# Create your views here.
# from django.http import HttpResponse
# from django.http import HttpResponseRedirect
import base64
import io


import threading
from PIL import Image
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from .src import processor as engine


def index(request):
    return render(request, "welcome_page.html")


@csrf_exempt
def initiate(request):
    image_data = request.POST['imageData']
    image_data = base64.b64decode(str(image_data))
    image = Image.open(io.BytesIO(image_data))

    # handler = open("photo.png", "wb+")
    # handler.write(image_data)
    # handler.close()

    process_thread = threading.Thread(target=process_function, args=[request, [image, request.POST['getText']]])
    process_thread.start()
    return JsonResponse({"data": "Your query is being processed and will open in a new tab shortly"})




def process_function(request, some_args):
    # do some stuff
    engine.main(some_args)
    # render(some_args[0])
    # continue doing stuff
