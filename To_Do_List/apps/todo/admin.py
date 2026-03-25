from django.contrib import admin

from apps.todo.models import ToDo, Comment


admin.site.register(Comment)
class CommentInline(admin.TabularInline):
    model = Comment
    fields = ['message', 'user',]


@admin.register(ToDo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'description', 'is_completed', 'start_date', 'end_date']
    list_display_links = ['title', 'description', 'is_completed', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date', 'is_completed']
    fieldsets = (
        ('할일 상세', {'fields': ('title', 'description', 'image', 'is_completed', 'start_date', 'end_date')}),
    )
    inlines = [
        CommentInline,
    ]

