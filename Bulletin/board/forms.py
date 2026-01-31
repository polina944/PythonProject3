import secrets
from allauth.account.forms import SignupForm
from django.core.mail import send_mail
from django.conf import settings
from django.forms import ModelForm
from django import forms
from board.models import Post, Comment


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super().save(request)
        secrets_code = secrets.token_urlsafe(10)
        user.is_active = False
        user.code = secrets_code
        user.save()
        send_mail(
            subject='Активация аккаунта',
            message=f'Активируйте свой аккаунт по коду: {secrets_code}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )
        return user


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '',
        }
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Напишите комментарий...',
                'style': 'resize: none;',
            }),
        }



#import secrets:
#Импортирует модуль secrets из стандартной библиотеки Python
#from allauth.account.forms import SignupForm:
#Импортирует базовый класс формы регистрации из Django allauth
#SignupForm - стандартная форма регистрации allauth
#from django.core.mail import send_mail:
#Эта функция позволяет отправлять электронные письма
#Импортирует функцию send_mail из Django
#from django.conf import settings:
#settings содержит все настройки из settings.py
#Позволяет получить доступ к переменным типа DEFAULT_FROM_EMAIL
#class BasicSignupForm(SignupForm):
#Создает пользовательский класс формы BasicSignupForm
#Наследуется от стандартной формы allauth SignupForm
#Позволяет переопределить поведение формы регистрации
#def save(self, request):
#Определяет метод save с параметром request
#Переопределяет стандартный метод сохранения формы
#self - ссылка на текущий экземпляр формы
#request - объект HTTP запроса (содержит данные пользователя, сессию и т.д.)
#user = super().save(request):
#Вызывает метод save родительского класса SignupForm
#super() дает доступ к методам родительского класса
#Создает  сохраняет пользователя в базе данных
#Возвращает объект созданного пользователя
#secrets_code = secrets.token_urlsafe(10):

