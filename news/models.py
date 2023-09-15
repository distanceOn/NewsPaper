from django.db import models
from django.contrib.auth.models import User
from django.db.models import Sum


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def update_rating(self):
        # Считаем суммарный рейтинг статей автора, умноженный на 3
        post_rating = self.post_set.aggregate(
            Sum('rating'))['rating__sum'] or 0
        post_rating *= 3

        # Считаем суммарный рейтинг всех комментариев автора
        comment_rating = Comment.objects.filter(
            post__author=self).aggregate(Sum('rating'))['rating__sum'] or 0

        # Считаем суммарный рейтинг всех комментариев к статьям автора
        comment_to_posts_rating = Comment.objects.filter(
            post__author__user=self.user).aggregate(Sum('rating'))['rating__sum'] or 0

        # Обновляем общий рейтинг автора
        self.rating = post_rating + comment_rating + comment_to_posts_rating
        self.save()


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    post_type = models.CharField(max_length=10, choices=[
                                 ('статья', 'Статья'), ('новость', 'Новость')])
    created_at = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Category, through='PostCategory')
    title = models.CharField(max_length=200)
    text = models.TextField()
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()

    def preview(self):
        return self.text[:124] + '...'


class PostCategory(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(default=0)

    def like(self):
        self.rating += 1
        self.save()

    def dislike(self):
        self.rating -= 1
        self.save()
