from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django import forms

def get_or_none(model, *args, **kwargs):
	try:
		return model.objects.get(*args, **kwargs)
	except model.DoesNotExist:
		return None

# Create your views here.
def signup(request):
	return render(request, 'projman/signup.html', None)

def submitsignup(request): #POST data is inside request
	username=request.POST.get("username", None)
	email=request.POST.get("email", None)
	password=request.POST.get("password", None)
	if username and email and password:
		User.objects.create_user(username=username, email=email, password=password)
	return HttpResponse('OK')

def signin(request):
	return render(request, 'projman/signin.html', None)

def submitsignin(request):
	username=request.POST.get("username", None)
	password=request.POST.get("password", None)
	lgduser=authenticate(username=username, password=password)
	if lgduser:
		if lgduser.is_active:
			login(request, lgduser)
			print('user is authenticated and active')
			return HttpResponse('OK')
		else:
			print("The password is valid, but the account has been disabled!") #how can this happen??
	else:
		print('user does not exists') #shouldnt be happening
		return HttpResponse('401')

def signout(request):
	if request:
		logout(request)
	return redirect("/")

def submitnewproj(request):
	name=request.POST.get("name")
	desc=request.POST.get("description")
	if request and not request.user.is_anonymous() and name:
		user=get_object_or_404(ProjmanUser, user=request.user)
		proj=Project(name=name, description=desc, author=user)
		proj.save()
		part=Participation(user=user, project=proj)
		part.save()
	return HttpResponse('200')

def updateavatar(request):
	print(request.POST)
	#pic=request.POST.get("")
	return HttpResponse('200')

def index(request):
	if request and not request.user.is_anonymous():
		puser=get_object_or_404(ProjmanUser, user=request.user)
		partlist=Participation.objects.filter(user=puser)
		projlist= []
		for i in partlist:
			projlist.append(i.project)
		userpic=puser.avatar
		context= {'projlist': projlist, 'userpic': userpic, 'userindex': True}

		return render(request, 'projman/app.html', context)
	else:
		#TODO: separate welcome view?
		return render(request, 'projman/index.html', None)

def toggletododone(request, todoid):
	puser=get_object_or_404(ProjmanUser, user=request.user)
	todo=get_object_or_404(To_do, id=todoid)
	particip=Participation.objects.filter(project=todo.parent_project, user=puser)
	if request and not request.user.is_anonymous() and particip:
		print(type(request.POST.get("todoCheckbox")))
		print(request.POST.get("todoCheckbox"))
		#IGNOREME inverted booleans, the checkbox returns its state BEFORE it was pressed.
		if not request.POST.get("todoCheckbox") and not request.POST.get("todoCheckbox")=="":
			todo.done=False
		else:
			todo.done=True
		todo.save()

	return HttpResponse("200")

def submitnewtodo(request):
	rawDesign=request.POST.get("newtodoDesignations")
	designationsList=[]
	if rawDesign:
		designationsList=rawDesign[:-1].split('|')

	title=request.POST.get("title")
	details=request.POST.get("details")
	proj= get_object_or_404(Project, id= request.POST.get("parentproj"))
	if request and not request.user.is_anonymous() and title:
		user=get_object_or_404(ProjmanUser, user=request.user)
		todo=To_do(title=title, details=details, author=user, parent_project=proj)
		todo.save()

		if designationsList:
			for i in designationsList:
				desi=Designation(user=get_object_or_404(ProjmanUser, user=get_object_or_404(User, username=i)), todo=todo)
				desi.save()
		#TODO: designation
		#des=Participation(user=user, project=proj)
		#part.save()
	return HttpResponse('200')

def deletetodo(request, todoid):
	puser=get_object_or_404(ProjmanUser, user=request.user)
	todo=get_object_or_404(To_do, id=todoid)
	particip=Participation.objects.filter(project=todo.parent_project, user=puser)
	design=Designation.objects.filter(todo=todo)
	if request and not request.user.is_anonymous() and particip:
		proj=todo.parent_project
		comments=Comment_todo.objects.filter(parent_todo=todo)
		for i in comments:
			i.delete()
		todo.delete()
		if design:
			for i in design:
				i.delete()
	return redirect('/project/'+str(proj.id))

def edittodo(request):
	puser=get_object_or_404(ProjmanUser, user=request.user)
	title=request.POST.get("title")
	details=request.POST.get("details")
	todo=get_object_or_404(To_do, id=request.POST.get("todoid"))
	particip=Participation.objects.filter(project=todo.parent_project, user=puser)

	rawDesign=request.POST.get("edittodoDesignations")
	designationsList=[]
	if rawDesign:
		designationsList=rawDesign[:-1].split('|')
	oldDesigns=Designation.objects.filter(todo=todo)
	for i in oldDesigns:
		print(i.user.user.username)
	if request and not request.user.is_anonymous() and title and particip:
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

def deletetodocomment(request, commentid):
	puser=get_object_or_404(ProjmanUser, user=request.user)
	comment=get_object_or_404(Comment_todo, id=commentid)
	particip=Participation.objects.filter(project=comment.parent_todo.parent_project, user=puser)
	if request and not request.user.is_anonymous() and particip:
		todo=comment.parent_todo
		comment.delete()
	return redirect('/todo/'+str(todo.id))

def todoview(request, todoid):
	puser=get_object_or_404(ProjmanUser, user=request.user)
	todo=get_object_or_404(To_do, id=todoid)
	particip=Participation.objects.filter(project=todo.parent_project, user=puser)
	proj=todo.parent_project
	participants=Participation.objects.filter(project=proj)
	if request and not request.user.is_anonymous() and particip:
		commentstodolist=Comment_todo.objects.filter(parent_todo=todo).order_by('date_time')
		designations=Designation.objects.filter(todo=todo)
		context= {'commentstodolist': commentstodolist, 'todo': todo, 'designations': designations, 'participants': participants, 'project': proj}
		return render(request, 'projman/app.html', context)

def submittodocomment(request, todoid):
	puser=get_object_or_404(ProjmanUser, user=request.user)
	content=request.POST.get("content")
	todo= get_object_or_404(To_do, id=todoid)
	particip=Participation.objects.filter(project=todo.parent_project, user=puser)
	if request and not request.user.is_anonymous() and particip and content:
		print("all passed")
		comment=Comment_todo(author=puser, content=content, parent_todo=todo)
		comment.save()
	return HttpResponse('200')

def projview(request, projid):
	if request and not request.user.is_anonymous():
		puser=get_object_or_404(ProjmanUser, user=request.user)
		project=get_object_or_404(Project, id=projid)
		todolist=To_do.objects.filter(parent_project=project).order_by('done')
		particip=Participation.objects.filter(project=project)
		designations=[]
		for i in todolist:
			d=Designation.objects.filter(todo=i)
			for j in d:
				designations.append(j)

		userpic=puser.avatar
		context= {'project': project, 'todolist': todolist, 'userpic': puser.avatar, 'designations': designations, 'participants': particip, 'todoview': True}

		return render(request, 'projman/app.html', context)
	else:
		return render(request, 'projman/index.html', None)

def notesview(request, projid):
	if request and not request.user.is_anonymous():
		puser=get_object_or_404(ProjmanUser, user=request.user)
		project=get_object_or_404(Project, id=projid)
		noteslist=Note.objects.filter(parent_project=project).order_by('-pinned')
		particip=Participation.objects.filter(project=project)

		userpic=puser.avatar
		context= {'project': project, 'noteslist': noteslist, 'userpic': puser.avatar, 'notesview': True}

		return render(request, 'projman/app.html', context)
	else:
		return render(request, 'projman/index.html', None)

def submitnewnote(request):
	pinned=request.POST.get("pinned")
	title=request.POST.get("title")
	content=request.POST.get("content")
	proj= get_object_or_404(Project, id= request.POST.get("parentproj"))
	if request and not request.user.is_anonymous() and title:
		user=get_object_or_404(ProjmanUser, user=request.user)
		note=Note(title=title, content=content, author=user, parent_project=proj)
		if pinned:
			note.pinned=True
		note.save()
	return HttpResponse('200')

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
