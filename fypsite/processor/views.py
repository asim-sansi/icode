# Create your views here.
# from django.http import HttpResponse
# from django.http import HttpResponseRedirect
import base64
import io
import os
from queue import Queue
from django.conf import settings
from zipfile import ZipFile
from PIL import Image
from django.http import JsonResponse, FileResponse, HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Template
from .src import processor as engine
from wsgiref.util import FileWrapper


comm_channel = Queue()


def index(request):
    return render(request, "welcome_page.html")


def show_form(request):
    image = ""
    if 'image' in request.GET:
        image = request.GET['image']
    print(image)
    return render(request, "process_form.html", {"image": str(image)})


def show_templates(request):
    query = ""
    templates = []
    if 'query' in request.GET:
        query = request.GET['query']
        templates = Template.objects.filter(name__contains=query)
    else:
        templates = Template.objects.all()
    response = {
        "query": query,
        "count": len(templates),
        "range": range(len(templates)),
        "templates": templates
    }
    return render(request, "templates.html", response)


def show_aboutus(request):
    return render(request, "aboutus.html")


def show_contactus(request):
    return render(request, "contactus.html")

@csrf_exempt
def initiate(request):
    image_data = request.POST['imageData']
    image_data = base64.b64decode(str(image_data))
    image = Image.open(io.BytesIO(image_data))

    # handler = open("photo.png", "wb+")
    # handler.write(image_data)
    # handler.close()

    dict = {
        "comm-channel": comm_channel,
        "text-type": int(request.POST["textType"]),
        "image-type": int(request.POST["imageType"]),
        "use_defaults": ""
    }
    process_thread = engine.threading.Thread(target=process_function, args=[request, [image, dict]])
    process_thread.start()

    return JsonResponse({"data": "Your query is being processed and will be ready shortly"})

@csrf_exempt
def trackProcess(request):
    if comm_channel.empty() == False:
        return JsonResponse({"progress": comm_channel.get()})
    else:
        return JsonResponse({"progress": -1})

def viewCode(request):
    data = ""
    file = open('../generated_resources/webpages/webpage.html', 'r')
    data = file.readlines()
    data = ''.join(data)

    return render(request, "viewcode.html", {"data": data})

def viewPage(request):
    # return render(request, "webpage.html")
    file_path = os.path.join(settings.BASE_DIR, "processor/static/generated_resources/webpage.html")
    os.system("start \"\" " + file_path)
    return JsonResponse({"progress": -1})

@csrf_exempt
def download(request):
    file_path = os.path.join(settings.BASE_DIR, "processor/static/generated_resources/")
    # # create a ZipFile object
    # zipObj = ZipFile(file_path + 'page.zip', 'w')
    #
    # # Add multiple files to the zip
    # zipObj.write(file_path + "webpage.html")
    #
    # zipObj.write(file_path + "default_image.png")
    # # close the Zip File
    # zipObj.close()
    file = open(file_path + "webpage.zip")
    wrapper = FileWrapper(file)
    res = FileResponse(wrapper,content_type='application/zip')
    res['Content-Disposition'] = 'attachment; filename=page.zip'
    return res

def process_function(request, some_args):
    # do some stuff
    engine.main(some_args)
    # continue doing stuff
