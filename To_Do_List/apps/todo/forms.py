from django.forms import ModelForm, TextInput
from apps.todo.models import ToDoList, Comment


class ToDoListForm(ModelForm):
    class Meta:
        model = ToDoList
        fields = ['title', 'description', 'start_date', 'end_date']


class ToDoUpdateForm(ToDoListForm):
    class Meta(ToDoListForm.Meta):
        fields = ToDoListForm.Meta.fields + ['is_completed']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['message',]
        labels = {
            'message': '댓글',
        }
        widgets = {
            'message': TextInput(attrs={'class': 'form-control'}),
        }