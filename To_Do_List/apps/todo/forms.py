from django.forms import ModelForm, TextInput
from django_summernote.widgets import SummernoteWidget

from apps.todo.models import ToDo, Comment


class ToDoForm(ModelForm):
    class Meta:
        model = ToDo
        fields = ['title', 'description', 'start_date', 'end_date', 'image']
        widgets = {
            'description': SummernoteWidget(),
        }


class ToDoUpdateForm(ToDoForm):
    class Meta(ToDoForm.Meta):
        fields = ToDoForm.Meta.fields + ['is_completed']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message',]
        labels = {
            'message': '',
        }
        widgets = {
            'message': TextInput(attrs={'class': 'form-control'}),
        }