from django.http import HttpResponse
from django.template import loader

# Create your views here.
def mainmap(request):
    template = loader.get_template('map.html')
    return HttpResponse(template.render())