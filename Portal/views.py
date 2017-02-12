from django.shortcuts import (render, redirect)
from django.template import loader


def index(request):
	# template = loader.get_template('/index.html')
	# return HttpRequest(template.render(request=request))
	return redirect('/login')