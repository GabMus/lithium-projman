from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.core.mail import send_mail
from django.conf import settings
import time
import hashlib
from smtplib import SMTPException
from .verifications import *

EMAIL_SUBJECT_HEADER='Lithium Projman: '
EMAIL_INVITE_SUBJECT=' invited you to join his project!'

def get_or_none(model, *args, **kwargs):
	try:
		return model.objects.get(*args, **kwargs)
	except model.DoesNotExist:
		return None

# Create your views here.
def signup(request):
	return render(request, 'projman/signup.html', None)

def submitsignup(request): #POST data is inside request
	username=request.POST.get('username', None)
	email=request.POST.get('email', None)
	password=request.POST.get('password', None)
	if not usernameExists(username) and emailIsValid(email) and usernameIsValid(username) and password:
		User.objects.create_user(username=username, email=email, password=password)
		return HttpResponse('201')
	else:
		return HttpResponse('401')

def signin(request):
	if userIsLogged(request.user):
		return redirect('/')
	else:
		return render(request, 'projman/signin.html', None)

def submitsignin(request):
	username=request.POST.get('username', None)
	password=request.POST.get('password', None)
	lgduser=authenticate(username=username, password=password)
	if lgduser:
		if lgduser.is_active:
			login(request, lgduser)
			return HttpResponse('200')
		else:
			print('The password is valid, but the account has been disabled!') #how can this happen??
	else:
		print('user does not exists') #shouldnt be happening
		return HttpResponse('403')

def signout(request):
	if request:
		logout(request)
	return redirect("/")

def submitnewproj(request):
	name=request.POST.get("name")
	desc=request.POST.get("description")
	user=request.user
	puser=get_object_or_404(ProjmanUser, user=user)
	if userIsLogged(user) and name:
		proj=Project(name=name, description=desc, author=puser)
		proj.save()
		part=Participation(user=puser, project=proj)
		part.save()
		return HttpResponse('200')
	else:
		return HttpResponse('401')

def index(request):
	if request and userIsLogged(request.user):
		puser=get_object_or_404(ProjmanUser, user=request.user)
		partlist=Participation.objects.filter(user=puser)
		projlist= []
		for i in partlist:
			projlist.append(i.project)
		userpic=puser.avatar
		context= {'projlist': projlist, 'userpic': userpic, 'userindex': True}

		return render(request, 'projman/app.html', context)
	else:
		#TODO maybe: separate welcome view?
		return render(request, 'projman/index.html', None)

def toggletododone(request, todoid):
	puser=get_object_or_404(ProjmanUser, user=request.user)
	todo=get_object_or_404(To_do, id=todoid)
	if userIsLogged(request.user) and userParticipatesProject(request.user, todo.parent_project):
		if not request.POST.get("todoCheckbox") and not request.POST.get("todoCheckbox")=="":
			todo.done=False
		else:
			todo.done=True
		todo.save()
		return HttpResponse("200")
	else:
		return HttpResponse('401')

def submitnewtodo(request):
	user=request.user
	title=request.POST.get("title")
	proj= get_object_or_404(Project, id= request.POST.get("parentproj"))
	if userIsLogged(user) and userParticipatesProject(user, proj) and title:
		puser=get_object_or_404(ProjmanUser, user=user)
		rawDesign=request.POST.get("newtodoDesignations")
		designationsList=[]
		if rawDesign:
			designationsList=rawDesign[:-1].split('|')
		details=request.POST.get("details")

		todo=To_do(title=title, details=details, author=puser, parent_project=proj)
		todo.save()

		if designationsList:
			for i in designationsList:
				desi=Designation(user=get_object_or_404(ProjmanUser, user=get_object_or_404(User, username=i)), todo=todo)
				desi.save()
		return HttpResponse('200')
	else:
		return HttpResponse('401')

def deletetodo(request, todoid):
	user=request.user
	todo=get_object_or_404(To_do, id=todoid)
	proj=todo.parent_project
	if userIsLogged(user) and userParticipatesProject(user, proj): #TODO: user should be author?
		puser=get_object_or_404(ProjmanUser, user=user)
		design=Designation.objects.filter(todo=todo)
		comments=Comment_todo.objects.filter(parent_todo=todo)
		for i in comments:
			i.delete()
		todo.delete()
		if design:
			for i in design:
				i.delete()
	return redirect('/project/'+str(proj.id))

def edittodo(request):
	user=request.user
	todo=get_object_or_404(To_do, id=request.POST.get("todoid"))
	project=todo.parent_project
	title=request.POST.get("title")
	if userIsLogged(user) and userParticipatesProject(user, project) and title:
		puser=get_object_or_404(ProjmanUser, user=user)
		details=request.POST.get("details")
		rawDesign=request.POST.get("edittodoDesignations")
		designationsList=[]
		if rawDesign:
			designationsList=rawDesign[:-1].split('|')
		oldDesigns=Designation.objects.filter(todo=todo)
		todo.title=title
		todo.details=details
		todo.save()
		if oldDesigns:
			for i in oldDesigns:
				if not i.user.user.username in designationsList:
					i.delete()
				else:
					del designationsList[designationsList.index(i.user.user.username)]
		for i in designationsList:
			duser=get_object_or_404(ProjmanUser, user=get_object_or_404(User, username=i))
			des=Designation(user=duser, todo=todo)
			des.save()
		return HttpResponse('200')
	else:
		return HttpResponse('401')

def deletetodocomment(request, commentid):
	user=request.user
	puser=get_object_or_404(ProjmanUser, user=user)
	comment=get_object_or_404(Comment_todo, id=commentid)
	todo=comment.parent_todo
	if userIsLogged(user) and comment.author==puser and userParticipatesProject(user, todo.parent_project):
		comment.delete()
		return redirect('/todo/'+str(todo.id))
	else:
		return HttpResponse('401')

def todoview(request, todoid):
	user=request.user
	todo=get_object_or_404(To_do, id=todoid)
	proj=todo.parent_project
	if userIsLogged(user) and userParticipatesProject(user, proj):
		participants=Participation.objects.filter(project=proj)
		puser=get_object_or_404(ProjmanUser, user=user)
		commentstodolist=Comment_todo.objects.filter(parent_todo=todo).order_by('date_time')
		designations=Designation.objects.filter(todo=todo)
		context= {'commentstodolist': commentstodolist, 'todo': todo, 'designations': designations, 'participants': participants, 'project': proj}
		return render(request, 'projman/app.html', context)
	else:
		return HttpResponse('401')

def submittodocomment(request, todoid):
	user=request.user
	todo= get_object_or_404(To_do, id=todoid)
	if userIsLogged(user) and userParticipatesProject(user, todo.parent_proj) and content:
		puser=get_object_or_404(ProjmanUser, user=user)
		content=request.POST.get("content")
		comment=Comment_todo(author=puser, content=content, parent_todo=todo)
		comment.save()
		return HttpResponse('200')
	else:
		return HttpResponse('401')

def projview(request, projid):
	user=request.user
	project=get_object_or_404(Project, id=projid)
	if userIsLogged(user) and userParticipatesProject(user, project):
		puser=get_object_or_404(ProjmanUser, user=request.user)
		todolist=To_do.objects.filter(parent_project=project).order_by('done')
		participants=Participation.objects.filter(project=project)
		designations=[]
		pinnednotes=Note.objects.filter(parent_project=project, pinned=True)
		for i in todolist:
			d=Designation.objects.filter(todo=i)
			for j in d:
				designations.append(j)
		userpic=puser.avatar
		context= {'project': project, 'todolist': todolist, 'userpic': puser.avatar, 'designations': designations, 'participants': participants, 'todoview': True, 'pinnednotes':pinnednotes}

		return render(request, 'projman/app.html', context)
	else:
		return redirect('/')

def notesview(request, projid):
	user=request.user
	project=get_object_or_404(Project, id=projid)
	if userIsLogged(user) and userParticipatesProject(user, project):
		puser=get_object_or_404(ProjmanUser, user=request.user)
		noteslist=Note.objects.filter(parent_project=project).order_by('-pinned')
		particip=Participation.objects.filter(project=project)
		userpic=puser.avatar
		context= {'project': project, 'noteslist': noteslist, 'userpic': puser.avatar, 'notesview': True}
		return render(request, 'projman/app.html', context)
	else:
		return redirect('/')

def submitnewnote(request):
	user=request.user
	proj= get_object_or_404(Project, id= request.POST.get("parentproj"))
	if userIsLogged(user) and userParticipatesProject(user, proj):
		pinned=request.POST.get("pinned")
		title=request.POST.get("title")
		content=request.POST.get("content")
		puser=get_object_or_404(ProjmanUser, user=user)
		note=Note(title=title, content=content, author=puser, parent_project=proj)
		if pinned:
			note.pinned=True
		note.save()
	return HttpResponse('200')

	#FROM HERE DOWN OPTIMIZATION AND CLEANUP TO BE DONE
def notecommentsview(request, noteid):
	puser=get_object_or_404(ProjmanUser, user=request.user)
	note=get_object_or_404(Note, id=noteid)
	particip=get_object_or_404(Participation, project=note.parent_project, user=puser)
	if request and not request.user.is_anonymous() and particip:
		proj=note.parent_project
		commentsnotelist=Comment_note.objects.filter(parent_note=note).order_by('date_time')
		context= {'commentsnotelist': commentsnotelist, 'note': note, 'project': proj}
		return render(request, 'projman/app.html', context)

def editnote(request):
	puser=get_object_or_404(ProjmanUser, user=request.user)
	title=request.POST.get("title")
	content=request.POST.get("content")
	note=get_object_or_404(Note, id=request.POST.get("noteid"))
	particip=Participation.objects.filter(project=note.parent_project, user=puser)
	pinned=request.POST.get("pinned")
	if request and not request.user.is_anonymous() and title and particip:
		note.title=title
		note.content=content
		if pinned:
			note.pinned=True
		else:
			note.pinned=False
		note.save()
	return HttpResponse('200')

def deletenote(request, noteid):
	puser=get_object_or_404(ProjmanUser, user=request.user)
	note=get_object_or_404(Note, id=noteid)
	particip=Participation.objects.filter(project=note.parent_project, user=puser)
	if request and not request.user.is_anonymous() and particip:
		proj=note.parent_project
		comments=Comment_note.objects.filter(parent_note=note)
		for i in comments:
			i.delete()
		note.delete()
	return redirect('/project/'+str(proj.id)+'/note')

def submitnotecomment(request, noteid):
	puser=get_object_or_404(ProjmanUser, user=request.user)
	content=request.POST.get("content")
	note= get_object_or_404(Note, id=noteid)
	particip=Participation.objects.filter(project=note.parent_project, user=puser)
	if request and not request.user.is_anonymous() and particip and content:
		comment=Comment_note(author=puser, content=content, parent_note=note)
		comment.save()
	return HttpResponse('200')

def deletenotecomment(request, commentid):
	puser=get_object_or_404(ProjmanUser, user=request.user)
	comment=get_object_or_404(Comment_note, id=commentid)
	particip=Participation.objects.filter(project=comment.parent_note.parent_project, user=puser)
	if request and not request.user.is_anonymous() and particip:
		note=comment.parent_note
		comment.delete()
	return redirect('/note/'+str(note.id))

class ImageUploadForm(forms.Form):
    image = forms.ImageField()

def userpicupload(request):
	puser=get_object_or_404(ProjmanUser, user=request.user)
	imform= ImageUploadForm(request.POST, request.FILES)
	if imform.is_valid():
		puser.avatar=imform.cleaned_data['image']
		puser.save()
		return redirect('/')
	else:
		return HttpResponse('403: forbidden')

def sendemail(subject, message, to):
	try:
		send_mail(subject, message, settings.EMAIL_HOST_USER, [to], fail_silently=False)
		return True
	except SMTPException:
		return False

def sendinvite(request):
	email=request.POST.get('invitemail')
	projid=request.POST.get('projid')
	proj=get_object_or_404(Project, id=projid)
	tstamp=int(time.time())
	unccode=str(tstamp)+str(projid)
	unccode=unccode.encode()
	code=hashlib.sha256(unccode).hexdigest()
	pcode=Projcode(project=proj, code=code)
	pcode.save()
	baseurl=request.META['HTTP_HOST']
	url='http://'+baseurl+'/getinvite/'+email+'/'+code
	subj=EMAIL_SUBJECT_HEADER+request.user.username+EMAIL_INVITE_SUBJECT
	message=request.user.username+" (email: "+request.user.email+") invited you to join his project "+proj.name+" on Lithium Projman.\nClick on the link below to join "+request.user.username+" now!\n"+url
	result=sendemail(subj, message, email)
	if result:
		return HttpResponse('200')
	else:
		return HttpResponse('400')

def submitinvitesignup(request):
	username=request.POST.get("username")
	email=request.POST.get("email")
	password=request.POST.get("password")
	projcode=request.POST.get("pcode")
	projcodeobj=get_object_or_404(Projcode, code=projcode)
	proj=projcodeobj.project
	if username and email and password and proj:
		User.objects.create_user(username=username, email=email, password=password)
		u=get_object_or_404(User, username=username)
		pu=get_object_or_404(ProjmanUser, user=u)
		part=Participation(user=pu, project=proj)
		part.save()
		projcodeobj.delete()
		return redirect('/signin')
	return HttpResponse('403')


def getinvite(request, email, projcode):
	user=get_or_none(User, email=email)
	puser=get_or_none(ProjmanUser, user=user)
	if puser:
		projcodeobj=get_object_or_404(Projcode, code=projcode)
		proj=projcodeobj.project
		part=Participation(user=puser, project=proj)
		part.save()
		projcodeobj.delete()
		return redirect('/')
	else:
		context = {'invite': True, 'invitemail': email, 'pcode': projcode}
		return render(request, 'projman/signup.html', context)

def deleteproject(request):
	projid=request.POST.get('projid')
	if request.POST.get('iamsure'):
		project=get_object_or_404(Project, id=projid)
		participationslist=Participation.objects.filter(project=project)
		noteslist=Note.objects.filter(parent_project=project)
		todolist=To_do.objects.filter(parent_project=project)
		tcommlist= []
		ncommlist= []
		for i in noteslist:
			ncomms=Comment_note.objects.filter(parent_note=i)
			for j in ncomms:
				ncommlist.append(j)
		for i in todolist:
			tcomms=Comment_todo.objects.filter(parent_todo=i)
			for j in tcomms:
				tcommlist.append(j)
		#begin deletion
		for i in tcommlist:
			i.delete()
		for i in ncommlist:
			i.delete()
		for i in todolist:
			i.delete()
		for i in noteslist:
			i.delete()
		for i in participationslist:
			i.delete()
		project.delete()
		return HttpResponse('200')
	else:
		return HttpResponse('400')
