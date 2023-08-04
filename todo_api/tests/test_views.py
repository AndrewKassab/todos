from django.contrib.auth.models import User
from django.forms import model_to_dict
from rest_framework.test import APITestCase
from rest_framework import status
from todo_api.models import Todo
from todo_api.serializers import TodoSerializer

from todo_api.views.todoapiview import TodoListApiView

TODO_VIEW_ENDPOINT = '/todos/api/'
TODO_VIEW_ID_ENDPOINT = TODO_VIEW_ENDPOINT + "{id}/"

class TodoViewTest(APITestCase):

	def setUp(self):
		self.user_one = User.objects.create_user(username="userone", password="password")
		self.user_two = User.objects.create_user(username="usertwo", password="password")
		self.todos = [
			Todo(task="Task1", completed="False", user=self.user_one),
			Todo(task="Task1", completed="False", user=self.user_two),
			Todo(task="Task2", completed="False", user=self.user_one),
			Todo(task="Task2", completed="False", user=self.user_two)
		]
		Todo.objects.bulk_create(self.todos)
	
	def extract_list_from_response(self, data_list):
		serializer = TodoSerializer(data=data_list, many=True)
		serializer.is_valid(raise_exception=True)
		return serializer.validated_data

	def test_get_todos_for_user_one(self):
		self.client.force_authenticate(user=User.objects.get(username="userone"))
		response = self.client.get(TODO_VIEW_ENDPOINT)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		todo_list = self.extract_list_from_response(response.data)
		self.assertEqual(len(todo_list), 2)

	def test_get_todos_with_no_user(self):
		response = self.client.get(TODO_VIEW_ENDPOINT)
		self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

	def test_create_todo(self):
		self.client.force_authenticate(user=User.objects.get(username="userone"))
		data = {
			'task': 'New Task',
			'completed': 'False',
		}
		response = self.client.post(TODO_VIEW_ENDPOINT, data=data)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)
	
	def test_create_todo_invalid(self):
		self.client.force_authenticate(user=User.objects.get(username="userone"))
		data = {
			'task': 'New Task',
		}
		response = self.client.post(TODO_VIEW_ENDPOINT, data=data)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
	
	def test_get_todo(self):
		self.client.force_authenticate(user=User.objects.get(username="userone"))
		response = self.client.get(TODO_VIEW_ID_ENDPOINT.format(id=1))
		self.assertEqual(response.status_code, status.HTTP_200_OK)
	
	def test_get_todo_doesnt_exist(self):
		self.client.force_authenticate(user=User.objects.get(username="userone"))
		response = self.client.get(TODO_VIEW_ID_ENDPOINT.format(id=5))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_get_todo_wrong_user(self):
		self.client.force_authenticate(user=User.objects.get(username="userone"))
		response = self.client.get(TODO_VIEW_ID_ENDPOINT.format(id=2))
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		
	def test_update_todo(self):
		self.client.force_authenticate(user=User.objects.get(username="userone"))
		new_task_name = "New Task name"
		todo = Todo.objects.get(user=self.user_one, task="Task1")
		todo.task = new_task_name
		todo_dict = model_to_dict(todo)
		response = self.client.put(TODO_VIEW_ID_ENDPOINT.format(id=todo.id), data=todo_dict)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(response.data['task'], new_task_name)

	def test_delete_todo(self):
		self.client.force_authenticate(user=User.objects.get(username="userone"))
		response = self.client.delete(TODO_VIEW_ID_ENDPOINT.format(id=1))
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

