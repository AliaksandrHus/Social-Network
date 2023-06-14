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

    content = forms.CharField(label='', widget=forms.TextInput(attrs={'placeholder': 'Введите текст:'}))
