from django.core.paginator import Paginator
from django.db.models import Q, Prefetch
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from apps.todo.forms import CommentForm, ToDoForm, ToDoUpdateForm
from apps.todo.models import ToDo, Comment
from django.contrib.auth.mixins import LoginRequiredMixin


class ToDoListView(LoginRequiredMixin, ListView):

    queryset = ToDo.objects.all()
    template_name = 'todo/cbv_todo_list.html'
    ordering = ['-updated_at', '-created_at']
    paginate_by = 10

    def get_queryset(self):

# 할일과 작성자 매칭
        queryset = super().get_queryset()
    # 어드민 권한
        if not self.request.user.is_superuser:
            queryset = queryset.filter(user=self.request.user)

# 검색 기능
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) |
                Q(description__icontains=q)
            )

        return queryset



class TodoDetailView(LoginRequiredMixin, DetailView):
    queryset = ToDo.objects.select_related('user').prefetch_related(
        Prefetch('comments',
                 queryset=Comment.objects.order_by('-created_at').select_related('user'))
    )
    template_name = 'todo/cbv_todo_info.html'
    pk_url_kwarg = 'todo_id'

# 할일과 작성자 매칭
    def get_object(self, queryset=None):
        obj = super().get_object()
    # 어드민 권한
        if self.request.user.is_superuser:
            return obj

        if obj.user != self.request.user:
            raise Http404()
        return obj

# context에 todo, comment_form 추가
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todo'] = self.object
        context['comment_create_form'] = CommentForm()

        comment_id = self.request.GET.get('update_cmt')
        if comment_id:
            comment = self.object.comments.get(pk=comment_id)
            context['comment_update_form'] = CommentForm(instance=comment)

# 댓글 페이지네이터
        comments = self.object.comments.all()
        paginator = Paginator(comments, 10)
        page = self.request.GET.get('page')
        page_obj = paginator.get_page(page)
        context['page_obj'] = page_obj

        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = ToDo
    template_name = 'todo/todo_form.html'
    form_class = ToDoForm

# form을 받아서 작성자 추가 및 디비에 저장
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '할 일 작성'
        context['btn_name'] = '생성'

        return context


    def get_success_url(self):
        return reverse_lazy('cbv_todo:info', kwargs={'todo_id': self.object.pk})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = ToDo
    template_name = 'todo/todo_form.html'
    form_class = ToDoUpdateForm
    pk_url_kwarg = 'todo_id'

# 할일과 작성자 매칭
    def get_object(self, queryset=None):
        obj = super().get_object()
    # 어드민 권한
        if self.request.user.is_superuser:
            return obj

        if obj.user != self.request.user:
            raise Http404()
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sub_title'] = '수정'
        context['btn_name'] = '저장'

        return context

    def get_success_url(self):
        return reverse_lazy('cbv_todo:info', kwargs={'todo_id': self.object.pk})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = ToDo
    pk_url_kwarg = 'todo_id'

# 할일과 작성자 매칭
    def get_object(self, queryset=None):
        obj = super().get_object()
    # 어드민 권한
        if self.request.user.is_superuser:
            return obj

        if obj.user != self.request.user:
            raise Http404()
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo:list')


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['message']
    # pk_url_kwarg = 'todo_id'

# self.object에 작성자와 todo 넣고 디비에 저장
    def form_valid(self, form):
        todo = get_object_or_404(ToDo, pk=self.kwargs['todo_id'])
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
        obj = super().get_object()
        if self.request.user.is_superuser:
            return obj
        if obj.user != self.request.user:
            raise Http404()

        return obj

    def get_success_url(self):
        page = self.request.GET.get('page')
        url = reverse_lazy('cbv_todo:info', kwargs={'todo_id': self.object.todo_id})
        if page:
            return f'{url}?page={page}'
        return url


class CommentDeleteView(LoginRequiredMixin, DeleteView):
    model = Comment

    def get_object(self, queryset=None):
        obj = super().get_object()
        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404()
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo:list')