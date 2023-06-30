from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.db import models
from django.dispatch import receiver


class Profile(models.Model):

    """Модель профиля User"""

    profile_id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)

    followers = models.ManyToManyField(User, related_name='followers', blank=True)
    following = models.ManyToManyField(User, related_name='following', blank=True)

    avatar = models.ImageField(upload_to='avatars/')

    # методы

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def photo_url(self):
        """Возвращает ссылку на изображение"""
        if self.avatar and hasattr(self.avatar, 'url'): return self.avatar.url

    def get_absolute_url(self):
        """Определение ссылки на объект модели"""
        return f'/avatars/{self.profile_id}'

    def follow(self, profile):
        """Подписаться на другой профиль"""
        self.following.add(profile.user)
        profile.followers.add(self.user)

    def unfollow(self, profile):
        """Отписаться от другого профиля"""
        self.following.remove(profile.user)
        profile.followers.remove(self.user)

    class Meta:
        """Отображение в админ панели"""
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Photo(models.Model):

    """Модель фотоальбома"""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    photo = models.ImageField(upload_to='photo/')
    like = models.ManyToManyField(User, related_name='like', blank=True)
    description = models.TextField(blank=True)

    # методы

    def __str__(self):
        return f'{self.author} / {self.date}'

    @property
    def photo_url(self):
        """Возвращает ссылку на изображение"""
        if self.photo and hasattr(self.photo, 'url'): return self.photo.url

    def get_absolute_url(self):
        """Определение ссылки на объект модели"""
        return f'/photo/{self.pk}'

    def set_like(self, profile):
        """Поставить лайк"""
        self.like.add(profile.user)

    def set_unlike(self, profile):
        """Отменить лайк"""
        self.like.remove(profile.user)

    class Meta:
        """Отображение в админ панели"""
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'


class PhotoComment(models.Model):

    """Модель комментариев к фотографии"""

    photo = models.ForeignKey(Photo, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)

    # методы

    def __str__(self):
        return f'{self.author} / {self.photo}'

    class Meta:
        """Отображение в админ панели"""
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Posts(models.Model):

    """Модель записей в ленте"""

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    like_post = models.ManyToManyField(User, related_name='like_post', blank=True)
    photo_post = models.ManyToManyField(Photo, related_name='photo_post', blank=True)

    # методы

    def __str__(self):
        return f'{self.author} / {self.date}'

    def set_like_post(self, profile):
        """Поставить лайк"""
        self.like_post.add(profile.user)

    def set_unlike_post(self, profile):
        """Отменить лайк"""
        self.like_post.remove(profile.user)

    def add_photo_in_post(self, photo):
        """Добавить фото в пост"""
        self.photo_post.add(photo.id)

    class Meta:
        """Отображение в админ панели"""
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


class PostsComment(models.Model):

    """Модель комментариев к фотографии"""

    posts = models.ForeignKey(Posts, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)

    # методы

    def __str__(self):
        return f'{self.author} / {self.posts}'

    class Meta:
        """Отображение в админ панели"""
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class RePosts(models.Model):

    """Модель репостов в ленте"""

    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    # методы

    def __str__(self):
        return f'{self.author} / {self.date}'

    class Meta:
        """Отображение в админ панели"""
        verbose_name = 'Репост'
        verbose_name_plural = 'Репосты'


class RePostsComment(models.Model):

    """Модель комментариев к фотографии"""

    reposts = models.ForeignKey(RePosts, on_delete=models.CASCADE)
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(blank=True)

    # методы

    def __str__(self):
        return f'{self.author} / {self.reposts}'

    class Meta:
        """Отображение в админ панели"""
        verbose_name = 'Комментарий репоста'
        verbose_name_plural = 'Комментарии репостов'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    """При регистрации автоматически создается Profile"""

    if created:
        Profile.objects.create(profile_id=instance.id,
                               user=instance,
                               first_name=(instance.first_name or 'SUPER'),
                               last_name=(instance.last_name or 'ADMIN'),
                               avatar='avatars/standard-avatar.jpg')

