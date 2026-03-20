from django.forms import ModelForm
from apps.todo.models import ToDoList


class ToDoListForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title', 'description', 'start_date', 'end_date']


class ToDoUpdateForm(ToDoListForm):
    class Meta(ToDoListForm.Meta):
        fields = ToDoListForm.Meta.fields + ['is_completed']