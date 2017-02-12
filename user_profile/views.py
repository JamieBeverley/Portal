from django.shortcuts import render
from django.template import loader
from login.models import Users
# Create your views here.

from django.http import HttpResponse



# Create your views here.
def index(username):
	template = loader.get_template('user_profile/index.html')
	context = {}
	
	return HttpResponse(template.render(None,None))

	# try:
	# 	a= HttpResponse(template.render(username))
	# except (TemplateDoesNotExist, TemplateSyntaxError) :
	# 	return HttpResponse(str(e))
	# except:
		# return HttpResponse("hmmmm")
	# # try:
	# 	return HttpResponse(template.render())
	# except TemplateSyntaxError(e):
	# 	return HttpResponse(e)