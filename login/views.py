from django.contrib.auth.models import User
from login.models import Studies,Profile
from login.forms import StudyForm, ProfileForm
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import (render, redirect, get_object_or_404)
from django.template import loader
from user_profile import views
# Create your views here.

from django.http import HttpResponse


def index(request):
	template = loader.get_template('login/index.html')
	context = {}
	if request.user.is_authenticated:
		logout(request)
	return HttpResponse(template.render(context,request))


def new_account(request):
	errorMsg = []
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		passwordConfirm = request.POST['password(confirm)']
		if len(username) < 8:
			errorMsg = ["Username too short!"]
		if password != passwordConfirm:
			errorMsg.append("Passwords did not match!")
		users = User.objects.all()
		for i in users:
			if (i.username==username):
				errorMsg.append("Sorry, username is taken!")
				break
		if len(errorMsg)==0:
			# prof = Profile(username=username)
			user = User.objects.create_user(username=username, password=password)
			user.save()
			return redirect('/login')
	template = loader.get_template('login/new_account.html')
	users = User.objects.all()
	usernames = []
	for i in users:
		usernames.append(i)
	context = {'usernames':usernames, 'errorMsg':errorMsg, 'errLen':(len(errorMsg))}
	return HttpResponse(template.render(context,request))

def created_account(request):
	username = request.POST['username']
	password = request.POST['password']
	passwordConfirm = request.POST['password(confirm)']
	
	if len(username) < 8:
		return HttpResponse("Username too short")
	
	if password != passwordConfirm:
		return (HttpResponse("Passwords did not match."))
	
	users = User.objects.all()
	for i in users:
		if (i.username==username):
			return (HttpResponse("sorry username is taken"))

	user = User.objects.create_user(username=username, password=password)
	user.save()
	return HttpResponse(str(request.POST['username']))

def verify(request):
	username = request.POST['username']
	password = request.POST['password']

	user = authenticate(username=username, password=password)

	if user is not None:
		login(request, user)
		# template = loader.get_template('login/home.html')
		# return HttpResponse("asdfasdfasdf")
		return redirect('/login/home')
		# return HttpResponse(template.render(context=None, request=request))

	else:
		return HttpResponse("Invalid user")


# @login_required(login_url='/login/')
def home(request):
	if request.user.is_authenticated():
		template = loader.get_template('login/home.html')
		name = request.user.username
		context = {'username':name}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('..')


def researcher(request):
	if request.user.is_authenticated():
		template = loader.get_template('login/researcher.html')
		currentStudies=Studies.objects.filter(creator=request.user)
		context = {'username':request.user.username, 'currentStudies':currentStudies}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('..')


def participant(request):
	if request.user.is_authenticated():
		submitMsg = ""
		instance = Profile.objects.get(username=request.user.profile.username)

		if (request.method == 'POST'):

			form = ProfileForm(request.POST,instance=instance)
			if form.is_valid():
				form.save()
				submitMsg="Changes updated"
			else: 
				submitMsg = "Invalid Entry!"
		form = ProfileForm(instance=instance)
		template = loader.get_template('login/participant.html')
		studyProfiles = Profile.objects.filter(isStudy=True)
		suggestedStudies=[]
		for i in studyProfiles:
			if i.isSimilar(request.user.profile):
				suggestedStudies.append(i.username)
		name = request.user.username
		dateOfBirth = request.user.profile.dateOfBirth
		context = {'username':name, 'suggestedStudies':suggestedStudies, 'form':form, 'submitMsg':submitMsg}
		return HttpResponse(template.render(context,request))
	else:
		return redirect('..')


def make_study(request):
	if request.user.is_authenticated():

		errorMsg = ""
		successMsg = ""
		if request.method == "POST":
			formResults = StudyForm(request.POST)
			if formResults.is_valid():
				

				currentStudies=Studies.objects.filter(creator=request.user)
				studyName = formResults.cleaned_data['name']

				# If the study already exists in this researcher's studies then return back to the form and print the error message
				for i in currentStudies:
					if i.name == studyName:
						errorMsg = "Study with that name already exists!"

						template = loader.get_template('login/make_study.html')
						context = {'user':request.user,'form':StudyForm(),'errorMsg':errorMsg}
						return HttpResponse(template.render(context,request))
				# description = formResults.cleaned_data['description']
				# inclusion = formResults.cleaned_data['inclusion']
				# exclusion = formResults.cleaned_data['exclusion']

				# sampleProfile = Profile.objects.create(username=(request.user.username+'/'+studyName))
				# study = Studies(creator=request.user ,name=studyName, description =description, inclusion=inclusion, exclusion = exclusion,profile=sampleProfile)
				study = StudyForm(request.POST).save()
				study.creator = request.user.username
				sampleProfile = ProfileForm(request.POST).save()
				sampleProfile.isStudy = True
				sampleProfile.username = request.user.username+'/'+study.name
				sampleProfile.save()
				# return HttpResponse(study.name)
				study.profile= sampleProfile
				# Try to save the study to the database, if it doesn't work set errorMsg to the appropriate message
				# try:
				study.save()
				successMsg = "Study created!"
				# except:
					# successMsg = ""
					# errorMsg = "Ooops, couldn't write your study to the database..."
				
				template = loader.get_template('login/make_study.html')
				context = {'user':request.user,'form':formResults,'successMsg':successMsg, "errorMsg":errorMsg}
				return HttpResponse(template.render(context,request))
			else:
				errorMsg = "Couldn't validate study criteria input, check that your input is valid."
		template = loader.get_template('login/make_study.html')
		studyForm = StudyForm()
		profileForm = ProfileForm()
		context = {'studyForm':studyForm,'profileForm':profileForm, 'errorMsg':errorMsg, 'successMsg':successMsg}
		return HttpResponse(template.render(context, request))
	else:
		return redirect('..')


def edit_study(request):
	if request.user.is_authenticated():
		# get the study
		msg=''
		studyName=''
		if (request.method=="POST"):
			if (request.POST['act'] == 'Delete'):

				study = Studies.objects.get(name=request.POST['studyName'],creator=request.user)
				study.delete();
				return redirect('../login/researcher')
			elif (request.POST['act'] == 'Save'): 
				studyName = request.POST['studyName']
				# instance = get_object_or_404(Studies,  creator=request.user.username, name=request.POST['studyName'])
				instance = Studies.objects.get(name=studyName,creator=request.user)
				form = StudyForm(data=request.POST,instance=instance)

				if form.is_valid():
					form.save()
					msg="succesfully saved"
				else:
					msg = "not saved"				
			else:
				studyName = request.POST['act']
				instance = Studies.objects.get(name=studyName,creator=request.user)
				form = StudyForm(instance=instance)

		template = loader.get_template('login/edit_study.html')
		context = {'form':form,'msg':msg, 'studyName':studyName}
		return HttpResponse(template.render(context, request))
	else:
		return redirect('..')

# 		msg = ""
# 		if request.method=="POST":
# 			if request.POST['act'] == 'Delete':
# 				study.delete()
# 				return redirect('../researcher')
# 			# formResults = StudyForm(request.POST, instance=study)
# 			# return HttpResponse(formResults)

# # profile = request.user.get_profile()
# #     edit_profile_form = EditProfileForm(request.POST or None,
# #         current_user=request.user, instance=profile)
# 			# study = Studies.objects.get(name=studyName,creator=request.user)
# 			formResults = StudyForm(request.POST, instance=study)
# 			if formResults.is_valid():

# 				study = StudyForm(request.POST).save()

# 				# study.name =   formResults.cleaned_data['studyName']
# 				# study.description = formResults.cleaned_data['description']
# 				# study.inclusion = formResults.cleaned_data['inclusion']
# 				# study.exclusion = formResults.cleaned_data['exclusion']

# 				# Try to save the study to the database, if it doesn't work set errorMsg to the appropriate message
# 				try:
# 					study.save()
# 					msg = "Study saved!"
# 				except:
# 					msg = "Ooops, couldn't write your study to the database..."
# 			else:
# 				msg = "Couldn't validate study criteria input, please check that your input is valid."
# 				msg =  formResults.errors


# 		# formDict = {'name':study.name, 'description':study.description, 'inclusion':study.inclusion, 'exclusion':study.exclusion}
# 		# form = StudyForm(initial=formDict)
# 		form = StudyForm(instance=study)
# 		template = loader.get_template('login/edit_study.html')
# 		context = {'form':form,'msg':msg, 'studyName':study.name}
# 		return HttpResponse(template.render(context, request))
# 	else:
# 		return redirect('..')


# def edit_study(request, studyName):
# 	if request.user.is_authenticated():
# 		# get the study
# 		try:
# 			study = Studies.objects.get(name=studyName,creator=request.user)
# 		except:
# 			return HttpResponse("Error, could not retrieve study '" + studyName+"'.")


# 		msg = ""
# 		if request.method=="POST":
# 			if request.POST['act'] == 'Delete':
# 				study.delete()
# 				return redirect('../researcher')
# 			# formResults = StudyForm(request.POST, instance=study)
# 			# return HttpResponse(formResults)

# # profile = request.user.get_profile()
# #     edit_profile_form = EditProfileForm(request.POST or None,
# #         current_user=request.user, instance=profile)
# 			# study = Studies.objects.get(name=studyName,creator=request.user)
# 			formResults = StudyForm(request.POST, instance=study)
# 			if formResults.is_valid():

# 				study = StudyForm(request.POST).save()

# 				# study.name =   formResults.cleaned_data['studyName']
# 				# study.description = formResults.cleaned_data['description']
# 				# study.inclusion = formResults.cleaned_data['inclusion']
# 				# study.exclusion = formResults.cleaned_data['exclusion']

# 				# Try to save the study to the database, if it doesn't work set errorMsg to the appropriate message
# 				try:
# 					study.save()
# 					msg = "Study saved!"
# 				except:
# 					msg = "Ooops, couldn't write your study to the database..."
# 			else:
# 				msg = "Couldn't validate study criteria input, please check that your input is valid."
# 				msg =  formResults.errors


# 		# formDict = {'name':study.name, 'description':study.description, 'inclusion':study.inclusion, 'exclusion':study.exclusion}
# 		# form = StudyForm(initial=formDict)
# 		form = StudyForm(instance=study)
# 		template = loader.get_template('login/edit_study.html')
# 		context = {'form':form,'msg':msg, 'studyName':study.name}
# 		return HttpResponse(template.render(context, request))
# 	else:
# 		return redirect('..')


def logout_(request):
	logout(request)
	return redirect('..')

def study_confirm(request):
	studyName =   form.cleaned_data['studyName']
	description = form.cleaned_data['description']
	inclusion = form.cleaned_data['inclusion']
	exclusion = form.cleaned_data['exclusion']
	template = loader.get_template('login/study_confirm.html')
	context = {'all':request.POST,'user':request.user}

	study = Studies(creator=request.user ,name=studyName, description =description, inclusion=inclusion, exclusion = exclusion)
	study.save()
	return HttpResponse(template.render(context,request))

	# try:
	#  	user = Users.objects.get(username=username)
	# except:
	# 	return HttpResponse("No account for:  "+str(username))

	# if user.password == password:
	# 	return redirect('/user_profile/');
	# else:
	# 	return HttpResponse("Incorrect password")
	# return HttpResponse("login verify")



