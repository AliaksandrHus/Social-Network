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


class Posts(models.Model):

    """Модель записей в ленте"""

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

    # методы

    def __str__(self):
        return f'{self.author} / {self.date}'

    class Meta:
        """Отображение в админ панели"""
        verbose_name = 'Пост'
        verbose_name_plural = 'Посты'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    """При регистрации автоматически создается Profile"""

    if created:
        Profile.objects.create(profile_id=instance.id,
                               user=instance,
                               first_name=(instance.first_name or 'SUPER'),
                               last_name=(instance.last_name or 'ADMIN'),
                               avatar='avatars/standard-avatar.jpg')




