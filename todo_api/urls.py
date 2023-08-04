from django.urls import path, include
from todo_api.views.todoapiview import TodoListApiView, TodoDetailApiView
from todo_api.views.todowebview import IndexView, DetailView, complete_todo

app_name = 'todos'
urlpatterns = [
	path('api/', TodoListApiView.as_view()),
	path('api/<int:todo_id>/', TodoDetailApiView.as_view()),
	path('', IndexView.as_view(), name='index'),
	path('<int:pk>/', DetailView.as_view(), name='detail'),
	path('<int:todo_id>/complete', complete_todo, name="complete")
]