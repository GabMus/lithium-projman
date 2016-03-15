#    This file is part of Lithium-Projman.
#
#    Lithium-Projman is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Lithium-Projman is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Lithium-Projman.  If not, see <http://www.gnu.org/licenses/>.


from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
import os

class ProjmanUser(models.Model):  # inherits Django default user class
	user = models.OneToOneField(User, on_delete = models.CASCADE, null = False)
	avatar= models.ImageField(upload_to='uploads/photos/%Y/%m/%d', blank = True, null = True)

	def create_user(sender, instance, created, **kwargs):
		if created:
			profile, created = ProjmanUser.objects.get_or_create(user = instance)

	post_save.connect(create_user, sender = User)

	def __str__(self):
		return self.user.username

class Project(models.Model):
	#  id is already defined as default in django
	author = models.ForeignKey('ProjmanUser', null = False)
	date_time = models.DateTimeField(auto_now_add = True)
	name = models.CharField(max_length=250, blank = False)
	description = models.TextField(blank = True)

	def __str__(self):
		return self.name

class To_do(models.Model):
	#  id is already defined as default in django
	author = models.ForeignKey('ProjmanUser', null = False)
	parent_project = models.ForeignKey('Project', null = False)
	title = models.TextField(blank = False)
	details = models.TextField(blank = True)
	done = models.BooleanField(default = False)
	date_time = models.DateTimeField(auto_now_add = True)

	def __str__(self):
		return self.author.user.username+" "+self.title

class Comment_todo(models.Model):
	# id is already defined as default in django
	author = models.ForeignKey('ProjmanUser', null = False)
	parent_todo = models.ForeignKey('To_do', null = False)
	content = models.TextField(blank = False)
	date_time = models.DateTimeField(auto_now_add = True)

class Note(models.Model):
	# id is already defined as default in django
	author = models.ForeignKey('ProjmanUser', null = False)
	parent_project = models.ForeignKey('Project', null = False)
	title = models.TextField(blank = False)
	content = models.TextField(blank = True)
	pinned = models.BooleanField(default = False)
	date_time = models.DateTimeField(auto_now_add = True)

class Comment_note(models.Model):
	# id is already defined as default in django
	author = models.ForeignKey('ProjmanUser', null = False)
	parent_note = models.ForeignKey('Note', null = False)
	content = models.TextField(blank = False)
	date_time = models.DateTimeField(auto_now_add = True)

class Participation(models.Model):
	user = models.ForeignKey('ProjmanUser', null = False)
	project = models.ForeignKey('Project', null = False)

	def __str__(self):
		return self.user.user.username + " -> " + self.project.name

class Designation(models.Model):
	user = models.ForeignKey('ProjmanUser', null = False)
	todo = models.ForeignKey('To_do', null = False)

	def __str__(self):
		return self.user.user.username + " -> " + self.todo.title

class Projcode(models.Model):
	project = models.ForeignKey('Project', null = False)
	code = models.TextField(null = False, blank = False)

	def __str__(self):
		return self.project.name
