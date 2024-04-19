from django.http import HttpResponse

from django.shortcuts import render
from django.template import loader
from . import audio

# Create your views here.
def index(request):
    template = loader.get_template("lookingGlassApp/index.html")

    return HttpResponse(template.render({},request))

def process_audio(request):
  if request.method == 'POST':
    # Assuming the user interaction triggers a POST request
    userprompt = audio.speech2text()
    print(userprompt)

    geminiresponse = audio.callGemini(userprompt)
    print(geminiresponse)
    # Handle the geminiresponse (e.g., display text or play audio)
    # ... (your code to handle the response)
    context = {'geminiresponse': geminiresponse}  # Pass response data to template
    audio.text2speech(geminiresponse)
    return render(request, 'lookingGlassApp/index.html', context)  # Render the same template with context
  
  else:
    return HttpResponse("Invalid request method")