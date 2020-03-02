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
from .models import Template
from .src import processor as engine


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

    process_thread = threading.Thread(target=process_function, args=[request, [image, request.POST['getText']]])
    process_thread.start()
    return JsonResponse({"data": "Your query is being processed and will open in a new tab shortly"})


def process_function(request, some_args):
    # do some stuff
    engine.main(some_args)
    # render(some_args[0])
    # continue doing stuff
