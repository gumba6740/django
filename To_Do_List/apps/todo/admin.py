from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin

from apps.todo.models import ToDo, Comment


admin.site.register(Comment)

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['message', 'user',]


@admin.register(ToDo)
class TodoAdmin(SummernoteModelAdmin):
    summernote_fields = ('description',)
    list_display = ['id', 'title', 'description', 'is_completed', 'start_date', 'end_date']
    list_display_links = ['title', 'description',]
    list_filter = ['start_date', 'end_date', 'is_completed']
    fieldsets = (
        ('할일 상세', {'fields': ('title', 'description', 'image', 'is_completed', 'start_date', 'end_date', 'user')}),
    )
    inlines = [
        CommentInline,
    ]

