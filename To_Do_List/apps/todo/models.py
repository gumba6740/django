from io import BytesIO
from pathlib import Path

from PIL import Image

from django.db import models

from django.conf import settings


class ToDo(models.Model):

    title = models.CharField(max_length=50)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    image = models.ImageField(upload_to='todo/%Y/%m/%d', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='todo/%Y/%m/%d/thumbnail', default="default/todo_default.png", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# save() 오버라이드
    def save(self, *args, **kwargs):
    # 이미지가 없다면 바로 저장
        if not self.image:
            return super().save(*args, **kwargs)

    # 파일 경로 문자열 파싱
        image_path = Path(self.image.name)
        thumbnail_name = image_path.stem
        thumbnail_extension = image_path.suffix
        thumbnail_filename = f'{thumbnail_name}_thumb{thumbnail_extension}'

    # jpg, jpeg, gif, png만 썸네일화. 나머지 이미지는 원본만 저장
        if thumbnail_extension in ['.jpg', '.jpeg']:
            file_type = 'JPEG'
        elif thumbnail_extension == '.gif':
            file_type = 'GIF'
        elif thumbnail_extension == '.png':
            file_type = 'PNG'
        else:
            return super().save(*args, **kwargs)

    # pillow로 이미지 리사이즈
        image = Image.open(self.image)
        image.thumbnail((130, 130),)

    # 메모리 공간에 썸네일 임시 저장 및 커서 위치 지정
        temp_thumb = BytesIO()
        image.save(temp_thumb, file_type)
        temp_thumb.seek(0)

    # self.thumbnail에 썸네일 저장 및 디스크에 썸네일 저장
        self.thumbnail.save(thumbnail_filename, temp_thumb, save=False)
        temp_thumb.close()

    # 디비에 self 저장 및 디스크에 이미지 저장
        return super().save(*args, **kwargs)

    class Meta:
        db_table = 'todos'
        verbose_name = '할 일'
        verbose_name_plural = '할 일 목록'


class Comment(models.Model):
    todo = models.ForeignKey(ToDo, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    message = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.todo.title}"

    class Meta:
        db_table = 'comments'
        verbose_name = '댓글'
        verbose_name_plural = '댓글 목록'

