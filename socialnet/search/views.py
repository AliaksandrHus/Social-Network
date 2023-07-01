from django.shortcuts import render
from django.shortcuts import redirect

from django.contrib.auth.decorators import login_required

from account.models import Profile, Posts, PostsComment, RePosts, RePostsComment
from account.forms import CommentPhotoForm

from itertools import chain


@login_required(login_url='/')
def search(request):

    """Страница поиска"""

    user = f'{request.user.first_name} {request.user.last_name}'
    comment_form = CommentPhotoForm

    if request.method == 'POST':

    # Кнопка найти

        if 'submit_button' in request.POST and request.POST['submit_button'] == 'start_search':

            search_text = request.POST['comment']
            return redirect('search_result', search_text)

    data = {
        'user': user,
        'title': 'Поиск',
        'comment_form': comment_form,
    }

    return render(request, 'search/search.html', data)



@login_required(login_url='/')
def search_result(request, text_search):

    """Страница общий результат поиска"""

    if request.method == 'POST':

    # Кнопка найти

        if 'submit_button' in request.POST and request.POST['submit_button'] == 'start_search':

            search_text = request.POST['comment']
            return redirect('search_result', search_text)

    # Кнопка подписаться

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'follow':

            pk = request.POST['user_id']
            person = Profile.objects.get(profile_id=request.user.id)
            person.follow(Profile.objects.get(profile_id=pk))

    # Кнопка отменить подписку

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'unfollow':

            pk = request.POST['user_id']
            person = Profile.objects.get(profile_id=request.user.id)
            person.unfollow(Profile.objects.get(profile_id=pk))

    # Добавить комментарий

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'create_comment':

            need_post = request.POST['post_id']

            new_comment = PostsComment()
            new_comment.posts = Posts.objects.get(pk=need_post)
            new_comment.author = Profile.objects.get(profile_id=request.user.id)
            new_comment.comment = request.POST['comment']
            new_comment.save()

    # Кнопка поставить / отменить лайк

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'set_like':

            need_post = Posts.objects.get(id=request.POST['post_id'])
            need_post.set_like_post(Profile.objects.get(profile_id=request.user.id))

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'set_unlike':

            need_post = Posts.objects.get(id=request.POST['post_id'])
            need_post.set_unlike_post(Profile.objects.get(profile_id=request.user.id))

    # Кнопка удалить комментарий

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'comment-delete':

            comment_id = request.POST['comment_id']
            comment_delete = PostsComment.objects.get(id=comment_id)
            comment_delete.delete()

    # Добавить комментарий к репосту

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'create_comment_repost':

            need_repost = request.POST['post_id']

            new_comment = RePostsComment()
            new_comment.reposts = RePosts.objects.get(pk=need_repost)
            new_comment.author = Profile.objects.get(profile_id=request.user.id)
            new_comment.comment = request.POST['comment']
            new_comment.save()

    # Кнопка удалить комментарий к репосту

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 're-comment-delete':

            comment_id = request.POST['comment_id']
            comment_delete = RePostsComment.objects.get(id=comment_id)
            comment_delete.delete()

    user = f'{request.user.first_name} {request.user.last_name}'
    i_following = Profile.objects.get(user=request.user.id).following.all()
    comment_form = CommentPhotoForm

    search_people = []
    search_people_all = ''

    # Если запрос состоит из 1 слова

    if len(text_search.split()) == 1:

        search_people += Profile.objects.filter(first_name__iregex=text_search)
        search_people += Profile.objects.filter(last_name__iregex=text_search)
        search_people = [person for person in set(search_people) if person.profile_id != request.user.id]

        search_people_count = len(search_people)
        search_people_all = '' if search_people_count <= 5 else search_people_count - 5

        search_people = search_people[:5]

    # Если запрос состоит из 2 слов

    if len(text_search.split()) == 2:

        text_search_list = text_search.split()

        search_people += Profile.objects.filter(first_name__iregex=text_search_list[0], last_name__iregex=text_search_list[1])
        search_people += Profile.objects.filter(first_name__iregex=text_search_list[1], last_name__iregex=text_search_list[0])
        search_people = [person for person in set(search_people) if person.profile_id != request.user.id]

        search_people_count = len(search_people)
        search_people_all = '' if search_people_count <= 5 else search_people_count - 5

        search_people = search_people[:5]

    # Создаем список поиска по постам

    post_and_repost = []

    posts = Posts.objects.filter(content__iregex=text_search)
    reposts = RePosts.objects.filter(content__iregex=text_search)
    post_and_repost += sorted(chain(posts, reposts), key=lambda x: x.date, reverse=True)

    post_and_repost = [post for post in post_and_repost if post.author.profile_id != request.user.id]

    # Добавить 3 последних комментария к постам и репостам

    for target_post in post_and_repost:

        if type(target_post) == Posts:
            target_post.comments = reversed(PostsComment.objects.filter(posts=target_post).order_by('-date')[:3])

        elif type(target_post) == RePosts:
            target_post.comments = reversed(
                RePostsComment.objects.filter(reposts=target_post).order_by('-date')[:3])

    data = {
        'user': user,
        'title': 'Результат поиска',
        'text_search': text_search,
        'i_following': i_following,
        'comment_form': comment_form,
        'search_people': search_people,
        'search_people_all': search_people_all,
        'post_and_repost': post_and_repost,
    }

    return render(request, 'search/search_result.html', data)


@login_required(login_url='/')
def search_result_people(request, text_search):

    """Страница результат поиска профилей"""

    if request.method == 'POST':

    # Кнопка найти

        if 'submit_button' in request.POST and request.POST['submit_button'] == 'start_search':

            search_text = request.POST['comment']
            return redirect('search_result', search_text)

    # Кнопка подписаться

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'follow':

            pk = request.POST['user_id']
            person = Profile.objects.get(profile_id=request.user.id)
            person.follow(Profile.objects.get(profile_id=pk))

    # Кнопка отменить подписку

        elif 'submit_button' in request.POST and request.POST['submit_button'] == 'unfollow':

            pk = request.POST['user_id']
            person = Profile.objects.get(profile_id=request.user.id)
            person.unfollow(Profile.objects.get(profile_id=pk))

    user = f'{request.user.first_name} {request.user.last_name}'
    i_following = Profile.objects.get(user=request.user.id).following.all()
    comment_form = CommentPhotoForm

    search_people = []

    # Если запрос состоит из 1 слова

    if len(text_search.split()) == 1:

        search_people += Profile.objects.filter(first_name__iregex=text_search)
        search_people += Profile.objects.filter(last_name__iregex=text_search)
        search_people = [person for person in set(search_people) if person.profile_id != request.user.id]

    # Если запрос состоит из 2 слов

    if len(text_search.split()) == 2:

        text_search_list = text_search.split()

        search_people += Profile.objects.filter(first_name__iregex=text_search_list[0], last_name__iregex=text_search_list[1])
        search_people += Profile.objects.filter(first_name__iregex=text_search_list[1], last_name__iregex=text_search_list[0])
        search_people = [person for person in set(search_people) if person.profile_id != request.user.id]

    data = {
        'user': user,
        'title': 'Результат поиска',
        'i_following': i_following,
        'comment_form': comment_form,
        'search_people': search_people,
    }

    return render(request, 'search/search_result.html', data)
