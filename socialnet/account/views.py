from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from .models import Profile, Posts
from .forms import LoginForm, RegistrationForm, PostsForm

import random
import re


def index(request):

    """Главная страница"""

    if request.user.is_authenticated: return redirect('profile_page')

    else:

        count_profile = Profile.objects.count()
        count_posts = Posts.objects.count()

        data = {
            'title': 'Приветствие',
            'count_profile': count_profile,
            'count_posts': count_posts
        }

        return render(request, 'account/index.html', data)


@login_required(login_url='/')
def profile_page(request):

    """Профиль пользователя"""

    if request.method == 'POST':

        if request.POST['submit_button'] == 'create_post':   # кнопка создать пост в ленте

            content = request.POST['content']
            user = request.user

            Posts.objects.create(content=content, author=user)

    user = f'{request.user.first_name} {request.user.last_name}'
    person = Profile.objects.get(user=request.user.id)
    posts = Posts.objects.filter(author__username=request.user.username).order_by('-date')

    posts_form = PostsForm

    followers = Profile.objects.get(user=request.user.id).followers.all()
    followers_count = followers.count()
    followers = [Profile.objects.get(profile_id=target.id) for target in followers]
    random.shuffle(followers)
    followers = followers[:5]

    following = Profile.objects.get(user=request.user.id).following.all()
    following_count = following.count()
    following = [Profile.objects.get(profile_id=target.id) for target in following]
    random.shuffle(following)
    following = following[:5]

    data = {
        'title': 'Моя страница:',
        'posts_form': posts_form,
        'user': user,
        'person': person,
        'posts': posts,
        'followers': followers,
        'following': following,
        'followers_count': followers_count,
        'following_count': following_count
    }

    return render(request, 'account/profile_page.html', data)


@login_required(login_url='/')
def another_user_page(request, pk):

    """Профиль другого пользователя"""

    if request.method == 'POST':

        if request.POST['submit_button'] == 'follow':   # кнопка подписаться
            person = Profile.objects.get(profile_id=request.user.id)
            person.follow(Profile.objects.get(profile_id=pk))

        elif request.POST['submit_button'] == 'unfollow':   # кнопка отменить подписку
            person = Profile.objects.get(profile_id=request.user.id)
            person.unfollow(Profile.objects.get(profile_id=pk))

    if request.user.id != pk:

        user = f'{request.user.first_name} {request.user.last_name}'

        person = get_object_or_404(Profile, user=pk)                                            # профиль другого user
        posts = Posts.objects.filter(author__username=person.user).order_by('-date')            # посты другого user
        follower = person.followers.filter(username=request.user.username).exists()             # проверка подписки

        followers = Profile.objects.get(user=pk).followers.all()
        followers_count = followers.count()
        followers = [Profile.objects.get(profile_id=target.id) for target in followers]
        random.shuffle(followers)
        followers = followers[:5]

        following = Profile.objects.get(user=pk).following.all()
        following_count = following.count()
        following = [Profile.objects.get(profile_id=target.id) for target in following]
        random.shuffle(following)
        following = following[:5]

        data = {
            'title': f'Пользователь #{pk}',
            'user': user,
            'person': person,
            'follower': follower,
            'posts': posts,
            'followers': followers,
            'following': following,
            'followers_count': followers_count,
            'following_count': following_count
        }

        return render(request, 'account/another_user_page.html', data)

    else: return redirect('profile_page')


@login_required(login_url='/')
def settings_page(request):

    """Страничка настроек / выход"""

    user = f'{request.user.first_name} {request.user.last_name}'

    data = {
        'title': 'Настройки',
        'user': user
    }

    return render(request, 'account/settings_page.html', data)


def login_page(request):

    """Страничка логирования"""

    error = ''

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')

        else:
            error = 'Данные не корректны, повторите ввод!'
            login_form = LoginForm

            data = {
                'title': 'Вход',
                'login_form': login_form,
                'error': error
            }

            return render(request, 'account/login_page.html', data)

    else:
        login_form = LoginForm

        data = {
            'title': 'Вход',
            'login_form': login_form,
            'error': error
        }

        return render(request, 'account/login_page.html', data)


def registration_page(request):

    """Страничка регистрации"""

    error = ''

    step1 = r"(?:[a-z0-9!#$%&'*+=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+=?^_`{|}~-]+)*)@(?:[a-z0-9]+(?:-[a-z0-9]+)*)\.[a-z]{2,5}"
    step2 = r"@.{1,63}\."

    def check_email(arg): return True if re.fullmatch(step1, arg) and re.search(step2, arg) else False

    if request.method == 'POST':

        registration_form = RegistrationForm(request.POST)

        first_name = request.POST['first_name']
        last_name = request.POST['last_name']

        email = request.POST['email']
        username = email

        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        if User.objects.filter(username=username).exists():

            error = 'Пользователь с таким email уже существует!'
            registration_form = RegistrationForm

            data = {
                'title': 'Регистрация',
                'registration_form': registration_form,
                'error': error
            }

            return render(request, 'account/registration_page.html', data)

        elif registration_form.is_valid() and password == password_confirmation and check_email(email):

            User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)

            user = authenticate(request, username=username, password=password)
            login(request, user)

            return redirect('profile_page')

        else:

            error = 'Данные не корректны, повторите ввод!'
            registration_form = RegistrationForm

            data = {
                'title': 'Регистрация',
                'registration_form': registration_form,
                'error': error
            }

            return render(request, 'account/registration_page.html', data)

    else:
        registration_form = RegistrationForm

        data = {
            'title': 'Регистрация',
            'registration_form': registration_form,
            'error': error
        }

        return render(request, 'account/registration_page.html', data)


@login_required(login_url='/')
def logout_page(request):

    """Функция выхода для страницы настроек"""

    logout(request)
    return redirect('index')
