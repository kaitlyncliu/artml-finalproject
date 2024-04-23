from django import forms
from django.http import HttpResponse

from django.shortcuts import redirect
from django.template import loader
from . import audio
from . import rpi

# Create your views here.
def index(request):
    template = loader.get_template("lookingGlassApp/index.html")

    return HttpResponse(template.render({},request))

def animate(request):
    template = loader.get_template("lookingGlassApp/animate.html")

    return HttpResponse(template.render({},request))

def process_audio(request):
    # if request.method == 'POST':
    print("[INFO] Processing audio")

    # Assuming the user interaction triggers a POST request
    userprompt = audio.speech2text()
    print(userprompt)

    # Get the name of the user from the RPI
    user = rpi.getUser()

    geminiresponse = audio.callGemini(user, userprompt)
    print(geminiresponse)

    # # Handle the geminiresponse (e.g., display text or play audio)
    # # ... (your code to handle the response)
    audio.text2speech(geminiresponse)
    
    # Redirect to a different URL
    return redirect('/animate')
