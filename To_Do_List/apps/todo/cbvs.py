from django.core.paginator import Paginator
from django.db.models import Q
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
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
    pk_url_kwarg = 'todo_id'

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
        context['comment_create_form'] = CommentForm()

        comment_id = self.request.GET.get('update_cmt')
        if comment_id:
            comment = self.object.comments.get(pk=comment_id)
            context['comment_update_form'] = CommentForm(instance=comment)

# 댓글 페이지네이터
        comments = Comment.objects.filter(todo_id=self.object.id).order_by('-created_at')
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
        return reverse_lazy('cbv_todo:info', kwargs={'todo_id': self.object.pk})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDoList
    template_name = 'todo/cbv_update_todo.html'
    fields = ['title', 'description', 'is_completed', 'start_date', 'end_date']
    context_object_name = 'todo'
    pk_url_kwarg = 'todo_id'

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
        return reverse_lazy('cbv_todo:info', kwargs={'todo_id': self.object.pk})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDoList
    pk_url_kwarg = 'todo_id'

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


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['message']
    # pk_url_kwarg = 'todo_id'

# self.object에 작성자와 todo 넣고 디비에 저장
    def form_valid(self, form):
        todo = get_object_or_404(ToDoList, pk=self.kwargs['todo_id'])
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.todo = todo
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('cbv_todo:info', kwargs={'todo_id': self.kwargs['todo_id']})


class CommentUpdateView(LoginRequiredMixin, UpdateView):
    model = Comment
    fields = ['message',]

    def get_object(self, queryset=None):
        object = super().get_object()
        if self.request.user.is_superuser:
            return object
        if object.user != self.request.user:
            raise Http404()

        return object

    def get_success_url(self):
        page = self.request.GET.get('page')
        url = reverse_lazy('cbv_todo:info', kwargs={'todo_id': self.object.todo_id})
        if page:
            return f'{url}?page={page}'
        return url


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        object = super().get_object()
        if object.user != self.request.user and not self.request.user.is_superuser:
            raise Http404()
        return object

    def get_success_url(self):
        return reverse_lazy("cbv_todo:info", kwargs={'todo_id': self.object.todo_id})