from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models import Profile, Posts, PostsComment, RePosts, RePostsComment
from account.forms import CommentPhotoForm

from itertools import chain


@login_required(login_url='/')
def news(request):

    """Страница общих новостей пользователя"""

    if request.method == 'POST':

    # Добавить комментарий

        if 'submit_button' in request.POST and request.POST['submit_button'] == 'create_comment':

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
    following = Profile.objects.get(user=request.user.id).following.all()
    comment_form = CommentPhotoForm

    # Создаем список новостей

    post_and_repost = []

    for follow_person in following:

        posts = Posts.objects.filter(author=follow_person.id)
        reposts = RePosts.objects.filter(author=follow_person.id)
        post_and_repost += sorted(chain(posts, reposts), key=lambda x: x.date, reverse=True)

    post_and_repost = sorted(post_and_repost, key=lambda x: x.date, reverse=True)

    # Добавить 3 последних комментария к постам и репостам

    for target_post in post_and_repost:

        if type(target_post) == Posts:
            target_post.comments = reversed(PostsComment.objects.filter(posts=target_post).order_by('-date')[:3])

        elif type(target_post) == RePosts:
            target_post.comments = reversed(
                RePostsComment.objects.filter(reposts=target_post).order_by('-date')[:3])

    data = {
        'title': 'Новости',
        'user': user,
        'post_and_repost': post_and_repost,
        'comment_form': comment_form,
    }

    return render(request, 'news/all_news.html', data)
