from django.db import models
from users.models import User


class BlogPost(models.Model):
    title = models.CharField(
        max_length=256,
        verbose_name="Заголовок посту",
        blank=False,
    )
    text = models.TextField(
        verbose_name="текст к посту"
    )
    image = models.ImageField(
        upload_to='photos/',
        verbose_name="фотография к посту",
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Время создания"
    )

    def __str__(self):
        return self.title


class Comment(models.Model):
    blog_post = models.ForeignKey(
        BlogPost,
        verbose_name='к посту',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        verbose_name='пользователь',
        on_delete=models.CASCADE,
    )
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Комментарий от {self.user.first_name} в {self.blog_post.title}'


# class CommentsInNews(models.Model):
#     comments = models.ForeignKey(
#         Comment,
#         verbose_name='комментарий',
#         on_delete=models.CASCADE,
#         related_name='comments'
#     )
#     block_post = models.ForeignKey(
#         BlogPost,
#         verbose_name="блог-пост",
#         on_delete=models.CASCADE,
#         related_name='block_posts'
#     )
#
#     class Meta:
#         verbose_name = "Комментарий в блог-посте"
#         verbose_name_plural = "Комментарии в блог-посте"
#         constraints = [
#             models.UniqueConstraint(
#                 fields=[
#                     'block_post',
#                     'comments'
#                 ],
#                 name='unique_combination'
#             )
#         ]
#
#     def __str__(self):
#         return (
#             f'{self.block_post.title}: '
#         )
