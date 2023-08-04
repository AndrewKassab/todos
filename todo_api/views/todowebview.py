from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse 
from django.views import generic 
from django.views.decorators.http import require_POST
from django.contrib.auth.mixins import LoginRequiredMixin

from todo_api.models import Todo


class IndexView(LoginRequiredMixin, generic.ListView):
	template_name = "todo_api/index.html"
	context_object_name = "todo_list"

	def get_queryset(self):
		return Todo.objects.filter(user=self.request.user)


class DetailView(LoginRequiredMixin, generic.DetailView):
	template_name = "todo_api/detail.html"
	model = Todo

	def get_queryset(self):
		return Todo.objects.filter(user=self.request.user)


@require_POST
def complete_todo(request, todo_id):
	todo = get_object_or_404(Todo, pk=todo_id, user=request.user.id)
	todo.completed = True
	todo.save()
	return HttpResponseRedirect(reverse("todos:index"))