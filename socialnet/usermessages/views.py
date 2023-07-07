from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from account.models import Profile, Posts, Photo, PhotoComment, PostsComment, RePosts, RePostsComment
from account.forms import LoginForm, RegistrationForm, PostsForm, DescriptionPhotoForm, CommentPhotoForm
from .models import Dialog, Messages, MessagePhoto
from groups.models import GroupPosts, GroupRePosts, GroupRePostsComment


from itertools import chain
import random
import re


@login_required(login_url='/')
def all_messages(request):

    """Страница всех сообщений пользователя"""

    user = f'{request.user.first_name} {request.user.last_name}'
    all_dialogs = Dialog.objects.filter(user_list=Profile.objects.get(profile_id=request.user.id)).order_by('-last_message_time')

    for target_dialog in all_dialogs:

        target_dialog.another_user = \
            [profile for profile in target_dialog.user_list.all() if profile.profile_id != request.user.id][0]

    not_read_message = Dialog.objects.filter(user_list__profile_id=request.user.id).filter(last_message__read=False)
    not_read_message = sum([1 for x in not_read_message if x.last_message.author.profile_id != request.user.id])

    data = {
        'not_read_message': not_read_message,
        'user': user,
        'title': 'Мои ообщения',
        'all_dialogs': all_dialogs
    }

    return render(request, 'usermessages/all_dialogs.html', data)


@login_required(login_url='/')
def dialog(request, dialog_id):

    """Страница диалог с другим пользователем"""

    start_slice = -10

    if request.method == 'POST':

    # Кнопка написать сообщение

        if 'submit_button' in request.POST and request.POST['submit_button'] == 'create_message':

            # Если в запросе текст или фото

            if request.POST['content'] or request.FILES:

                message = Messages()
                message.dialog = Dialog.objects.get(id=dialog_id)
                message.author = Profile.objects.get(profile_id=request.user.id)
                message.content = request.POST['content']
                message.save()

                dialog = Dialog.objects.get(id=dialog_id)

                if message.content == '' and request.FILES: dialog.last_message_text = 'Фото'
                else: dialog.last_message_text = str(request.POST['content'])[:50]

                if len(dialog.last_message_text) == 50: dialog.last_message_text += '...'

                dialog.last_message_time = message.date
                dialog.last_message = message
                dialog.save()

                # Если фото в запросе

                if 'photo_post' in request.FILES and request.FILES['photo_post']:

                    for send_photo in request.FILES.getlist('photo_post'):

                        photo = MessagePhoto()
                        photo.author = Profile.objects.get(profile_id=request.user.id)
                        photo.photo = send_photo
                        photo.save()
                        message.add_photo_in_post(photo)
                        message.save()

        # Кнопка удалить сообщение

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'message-delete':

            message_id = request.POST['message_id']
            message_id = int(message_id)

            # Если сообщение не последнее в спике

            if message_id != Messages.objects.latest('date').id:

                message_id = Messages.objects.get(id=message_id)
                message_id.delete()

            # Если сообщение последнее

            else:

                message_id = Messages.objects.get(id=message_id)
                message_id.delete()
                message = Messages.objects.latest('date')

                dialog = Dialog.objects.get(id=dialog_id)
                dialog.last_message_text = message.content[:50]
                print(dialog.last_message_text,'-----')
                dialog.last_message = message

                if dialog.last_message_text == ' ': dialog.last_message_text = 'Фото'
                if len(dialog.last_message_text) == 50: dialog.last_message_text += '...'

                dialog.last_message_time = message.date
                dialog.save()

        # Пост - Кнопка поставить / отменить лайк

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'set_like_post':

            need_post = Posts.objects.get(id=request.POST['post_id'])
            need_post.set_like_post(Profile.objects.get(profile_id=request.user.id))

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'set_unlike_post':

            need_post = Posts.objects.get(id=request.POST['post_id'])
            need_post.set_unlike_post(Profile.objects.get(profile_id=request.user.id))

        # Репост - Кнопка поставить / отменить лайк

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'set_like_repost':

            need_post = Posts.objects.get(id=request.POST['post_id'])
            need_post.set_like_post(Profile.objects.get(profile_id=request.user.id))

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'set_unlike_repost':

            need_post = Posts.objects.get(id=request.POST['post_id'])
            need_post.set_unlike_post(Profile.objects.get(profile_id=request.user.id))

        # Репост группы - Кнопка поставить / отменить лайк

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'set_like_group_post':

            need_post = GroupPosts.objects.get(id=request.POST['post_id'])
            need_post.set_like_post(Profile.objects.get(profile_id=request.user.id))

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'set_unlike_group_post':

            need_post = GroupPosts.objects.get(id=request.POST['post_id'])
            need_post.set_unlike_post(Profile.objects.get(profile_id=request.user.id))

        # Репост группы - Кнопка поставить / отменить лайк

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'set_like_group_repost':

            need_post = GroupPosts.objects.get(id=request.POST['post_id'])
            need_post.set_like_post(Profile.objects.get(profile_id=request.user.id))

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'set_unlike_group_repost':

            need_post = GroupPosts.objects.get(id=request.POST['post_id'])
            need_post.set_unlike_post(Profile.objects.get(profile_id=request.user.id))

        # Обновить страницу при прокрутке вверх

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'add_message_list':

            start_slice = int(request.POST['slice']) - 5

    user = f'{request.user.first_name} {request.user.last_name}'
    posts_form = PostsForm
    comment_form = CommentPhotoForm

    another_user = Dialog.objects.get(id=dialog_id).user_list.exclude(profile_id=request.user.id).first()
    print(another_user)

    for message in Messages.objects.filter(dialog=dialog_id):
        if message.author.profile_id != request.user.id:
            message.read = True
            message.save()

    messages_all = list(Messages.objects.filter(dialog=dialog_id).order_by('date'))
    messages = list(messages_all)[start_slice:]

    not_read_message = Dialog.objects.filter(user_list__profile_id=request.user.id).filter(last_message__read=False)
    not_read_message = sum([1 for x in not_read_message if x.last_message.author.profile_id != request.user.id])

    data = {
        'not_read_message': not_read_message,
        'user': user,
        'title': 'Диалог',
        'messages': messages,
        'posts_form': posts_form,
        'comment_form': comment_form,
        'start_slice': start_slice,
        'another_user': another_user,
    }

    return render(request, 'usermessages/single_dialog.html', data)
