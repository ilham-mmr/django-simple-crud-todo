from django.shortcuts import redirect, render
from django.views.generic.edit import FormView
from django.views.generic import ListView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin

from .models import Todo
from .forms import TodoForm
from django.views import View


class AddTodoView(FormView):
    form_class = TodoForm
    template_name = 'todos/todos.html'
    success_url = '/todos/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)


class ShowTodosView(ListView):
    template_name = 'todos/all-todos.html'
    model = Todo


class UpdateTodoView(UpdateView):
    template_name = 'todos/todos.html'
    model = Todo
    success_url = '/todos'
    form_class = TodoForm


class DeleteTodoView(DeleteView):
    model = Todo
    success_url = '/todos'


def todo_done(request, id):
    todo = Todo.objects.get(id=id)
    todo.is_done = not todo.is_done
    todo.save()
    return redirect('/todos')

