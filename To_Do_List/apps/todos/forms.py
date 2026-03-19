from django.forms import ModelForm
from apps.todos.models import ToDoList


class ToDoListForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title', 'description', 'start_date', 'end_date']


class ToDoUpdateForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title', 'description', 'is_completed', 'start_date', 'end_date']