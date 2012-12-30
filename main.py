#!/usr/bin/env python
#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import os
import logging
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import db

# logging define
logging.getLogger().setLevel(logging.DEBUG)


class ToDoData(db.Model):
	# author = db.UserProperty()
	todo_desc = db.StringProperty(multiline=True)
	create_date = db.DateTimeProperty(auto_now_add=True)



class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class EditHandler(webapp2.RequestHandler):
	def post(self):
		desc = self.request.get('todo_desc')
		if desc:
			self.redirect('/show')

		todoData = ToDoData()

		todoData.todo_desc = desc
		ToDoData.put()

class DeleteHandler(webapp2.RequestHandler):
	def post(self):
		todoKey = self.request.get('todo_key')
		if toDoKey:
			self.redirect('/')

		todo = ToDoData.get(toDoKey)

		if todo:
			todo.delete()

		self.redirect('/')


class ShowHandler(webapp2.RequestHandler):
	def get(self):

		user = users.get_current_user()
		logging.debug(user)

		#toDoList = db.GqlQuery('SELECT * from ToDoData order by create_date DESC')
		toDoList = ToDoData.all()
		toDoList.order('-create_date')
		template_values = {'toDoList':toDoList}
		path = os.path.join(os.path.dirname(__file__), 'template/index.html')
		self.response.out.write(template.render(path, template_values))

	def post(self):

		toDo = ToDoData()

		desc = self.request.get('todo_desc')
		logging.debug(desc)
		toDo.todo_desc = desc
		toDo.put()
		self.redirect('/')


app = webapp2.WSGIApplication([
    ('/', ShowHandler)
    , ('/show', ShowHandler)
    , ('/edit', EditHandler)
], debug=True)
