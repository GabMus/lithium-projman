	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.

#Lithium Projman

Project management platform.
Django backend, Polymer frontend.

##Requirements
- Django 1.9.x
- Pillow
- Bower (optional, for fiddling with the polymer repos)

##Directory structure
####/server
Contains  the django backend, the web frontend and the database files.

####/doc
Contains the project documentation.

##Setup

- Create an `email.py` file into /server/lithium containing SMTP credentials for an email service of your preference (services like gmail, yahoo mail, outlook should be fine). The file content will look something like this:

		EMAIL_HOST="smtp.examplemail.com"
		EMAIL_PORT=465 #this is a frequently used port
		EMAIL_HOST_USER="myemail@address.com"
		EMAIL_HOST_PASSWORD="myEmailPassword"
		EMAIL_USE_SSL=True

	The reason this file hasn't been included (and is listed in the .gitignore file) is to avoid exposing my SMTP credentials, and to preserve yours.

- cd in the /server folder and run:

		./manage.py makemigrations
		./manage.py migrate
	
	To generate the database file

- (optional) It might be useful to create a superuser account to manage the database directly from the web interface. To do this run:

		./manage.py createsuperuser