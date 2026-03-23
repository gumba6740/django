from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.todo.forms import CommentForm
from apps.todo.models import ToDoList, Comment
from django.contrib.auth.mixins import LoginRequiredMixin


class ToDoListView(LoginRequiredMixin, ListView):

    queryset = ToDoList.objects.all()
    template_name = 'todo/cbv_todo_list.html'
    ordering = ['-modified_at', '-created_at']
    paginate_by = 10

    def get_queryset(self):

# 할일과 작성자 매칭
        queryset = super().get_queryset()
    # 어드민 권한
        if not self.request.user.is_superuser:
            queryset = queryset.filter(author=self.request.user)

# 검색 기능
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )

        return queryset



class TodoDetailView(LoginRequiredMixin, DetailView):
    model = ToDoList
    template_name = 'todo/cbv_todo_info.html'

# 할일과 작성자 매칭
    def get_object(self, queryset=None):
        object = super().get_object()
    # 어드민 권한
        if self.request.user.is_superuser:
            return object

        if object.author != self.request.user:
            raise Http404()
        return object

# context에 todo, comment_form 추가
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = self.object.__dict__
        context['comment_form'] = CommentForm()

# 댓글 페이지네이터
        comments = Comment.objects.filter(todo_id=self.object.id)
        paginator = Paginator(comments, 10)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context['page_obj'] = page_obj

        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = ToDoList
    template_name = 'todo/cbv_create_todo.html'
    fields = ['title', 'description', 'start_date', 'end_date']

# form을 받아서 작성자 추가 및 디비에 저장
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cbv_todo:info', kwargs={'pk': self.object.pk})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDoList
    template_name = 'todo/cbv_update_todo.html'
    fields = ['title', 'description', 'is_completed', 'start_date', 'end_date']
    context_object_name = 'todo'

# 할일과 작성자 매칭
    def get_object(self, queryset=None):
        object = super().get_object()
    # 어드민 권한
        if self.request.user.is_superuser:
            return object

        if object.author != self.request.user:
            raise Http404()
        return object

    def get_success_url(self):
        return reverse_lazy('cbv_todo:info', args=(self.object.pk,))


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDoList

# 할일과 작성자 매칭
    def get_object(self, queryset=None):
        object = super().get_object()
    # 어드민 권한
        if self.request.user.is_superuser:
            return object

        if object.author != self.request.user:
            raise Http404()
        return object

    def get_success_url(self):
        return reverse_lazy('cbv_todo:list')