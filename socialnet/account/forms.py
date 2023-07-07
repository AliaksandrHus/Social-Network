from django import forms


class LoginForm(forms.Form):

    """Форма логирования"""

    username = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Введите email'}))
    password = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Введите пароль'}))


class RegistrationForm(forms.Form):

    """Форма регистрации"""

    first_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))
    last_name = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Введите фамилия'}))

    email = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Введите почту'}))
    password = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Введите пароль'}))
    password_confirmation = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Повторите пароль'}))


class PostsForm(forms.Form):

    """Форма создания поста в ленте профиля"""

    content = forms.CharField(required=False, label='', widget=forms.Textarea(attrs={'placeholder': '',
                                                                     'rows': 1,
                                                                     'class': 'post-create-textarea'}))


class DescriptionPhotoForm(forms.Form):

    """Форма создания описания фотографии"""

    description = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': '',
                                                                         'rows': 1,
                                                                         'class': 'description-photo-textarea'}))


class CommentPhotoForm(forms.Form):

    """Форма создания комментария к фотографии"""

    comment = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': '',
                                                                     'rows': 1,
                                                                     'class': 'comment-photo-textarea'}))


class StatusForm(forms.Form):

    """Форма создания статуса"""

    status = forms.CharField(label='', widget=forms.Textarea(attrs={'placeholder': '',
                                                                     'rows': 1,
                                                                     'class': 'status-textarea'}))
