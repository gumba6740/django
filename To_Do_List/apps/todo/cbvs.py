from django.db.models import Q
from django.views.generic import ListView
from apps.todo.models import ToDoList
from django.contrib.auth.mixins import LoginRequiredMixin


class ToDoListView(LoginRequiredMixin, ListView):

    queryset = ToDoList.objects.all()
    template_name = 'todo/todo_list.html'
    ordering = '-created_at'
    paginate_by = 10

    def get_queryset(self):

        queryset = super().get_queryset()

        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )

        return queryset


