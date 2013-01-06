#!/usr/bin/env python
# encoding: utf-8
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
import time,datetime
from google.appengine.api import users
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import mail

# logging define
logging.getLogger().setLevel(logging.DEBUG)


class ToDoData(db.Model):
	user = db.UserProperty()
	todo_desc = db.StringProperty(multiline=True)
	todo_due_date = db.DateProperty()
	complete_flg = db.BooleanProperty()
	create_date = db.DateTimeProperty(auto_now_add=True)
	update_date = db.DateTimeProperty(auto_now=True)



class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

class EditHandler(webapp2.RequestHandler):
	def post(self):
		toDoKey = self.request.get('todo_key')
		desc = self.request.get('todo_desc')
		str_due_date = self.request.get('todo_due_date')
		# if desc:
		# 	self.redirect('/show')

		st = time.strptime(str_due_date, '%Y/%m/%d')
		due_date = datetime.date(st[0], st[1], st[2])

		todoData = db.get(toDoKey)
		logging.debug(todoData)

		todoData.todo_desc = desc
		todoData.todo_due_date = due_date
		ToDoData.put()

class DeleteHandler(webapp2.RequestHandler):
	def get(self):
		toDoKey = self.request.get('todo_key')
		logging.debug(toDoKey)
		if toDoKey is None:
			return

		entity = db.get(toDoKey)
		logging.debug(entity)

		if entity:
			entity.delete()


class CompleteHandler(webapp2.RequestHandler):
	def get(self):
		toDoKey = self.request.get('todo_key')
		logging.debug(toDoKey)
		# if not toDoKey is None:
		# 	return


		logging.debug(self.response.headers)
		entity = db.get(toDoKey)
		logging.debug(entity)

		if entity:
			entity.complete_flg = True
			entity.put()


class ShowHandler(webapp2.RequestHandler):
	def get(self):

		user = users.get_current_user()
		logging.debug(user)


		toDoList = ToDoData.all().filter('user', user)
		toDoList.order('-todo_due_date')
		template_values = {'toDoList':toDoList, 'user': user}
		path = os.path.join(os.path.dirname(__file__), 'template/index.html')
		self.response.out.write(template.render(path, template_values))


class RegisterHandler(webapp2.RequestHandler):
	def post(self):
		toDo = ToDoData()

		desc = self.request.get('todo_desc')
		str_due_date = self.request.get('todo_due_date')


		st = time.strptime(str_due_date, '%Y/%m/%d')
		due_date = datetime.date(st[0], st[1], st[2])
		logging.debug(desc)
		logging.debug(due_date)
		toDo.todo_desc = desc
		toDo.todo_due_date = due_date
		toDo.complete_flg = False
		toDo.user = users.get_current_user()
		toDo.put()
		# self.redirect('/')


class RemainderHandler(webapp2.RequestHandler):
	def get(self):
		nowDate = datetime.date.today()
		yesterday = nowDate - datetime.timedelta(days=1)
		logging.debug(yesterday)
		todoList = ToDoData.all().filter("todo_due_date >=", yesterday).filter("complete_flg = ", False)

		for todo in todoList:

			message = mail.EmailMessage()
			message.sender = "Example.com Support <support@example.com>"
			message.to = todo.user.email()
			message.subject = "To Do remainder"
			message.body = u"""
			remainder　
			desc:%s
			duu date:%s

			complete:%s """ % (todo.todo_desc, todo.todo_due_date, "http://" + os.environ['HTTP_HOST'] + "/complete?todo_key=" + str(todo.key()) )

			message.send()





app = webapp2.WSGIApplication([
    ('/', ShowHandler)
    , ('/show', ShowHandler)
    , ('/register', RegisterHandler)
    # , ('/edit', EditHandler)
    , ('/delete', DeleteHandler)
    , ('/complete', CompleteHandler)
    , ('/remainder', RemainderHandler)
], debug=True)
