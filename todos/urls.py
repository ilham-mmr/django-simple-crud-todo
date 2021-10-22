from django.urls import include, path

# GET POST/todos show all todos/ post todo
# GET /todos/create create todo
# GET POST /todos/<int:id> detail todo/ delete todo
from . import views
urlpatterns = [
    path('create/', views.AddTodoView.as_view()),
    path('', views.ShowTodosView.as_view()),
    # path('done/', views.ShowDoneTodosView.as_view()),
    path('<int:pk>', views.UpdateTodoView.as_view()),
    path('<int:pk>/delete/', views.DeleteTodoView.as_view()),
    path('<int:id>/is_done/', views.todo_done),
]
