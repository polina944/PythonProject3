from django.urls import reverse
from django.db import models #Импортирует основной модуль models для создания моделей
from django.contrib.auth.models import AbstractUser #Импортирует AbstractUser - базовый класс пользователя Django для создания кастомной модели пользователя
from ckeditor_uploader.fields import RichTextUploadingField

class User(AbstractUser): #Создает кастомную модель пользователя, наследующую от AbstractUser
    code = models.CharField(max_length = 15, unique = True, null=True, blank=True) #Добавляет поле code (код пользователя) к стандартным полям пользователя
#CharField - текстовое поле с ограничением длины
#max_length=15 - максимальная длина 15 символов
#unique=True - значение должно быть уникальным для каждого пользователя

class Category(models.Model):#Создает модель Category для категорий объявлений
    name = models.CharField(max_length = 100) #Поле name для названия категории

    def __str__(self): #Информация об объекте категории выводилась в виде имени категорий
        return self.name #При отображении категории будет показываться её название


class Post(models.Model): #Создает модель Post для объявлений
    user = models.ForeignKey(User, on_delete = models.CASCADE) #Внешний ключ к модели User (связь "многие-к-одному")
    category = models.ForeignKey(Category, on_delete = models.CASCADE) #Внешний ключ к модели Category,Определяет категорию объявления,при удалении категории удаляются все связанные объявления
    created_at = models.DateTimeField(auto_now_add=True) #auto_now_add=True - автоматически устанавливает текущую дату/время при создании объекта
    title = models.CharField(max_length = 255) #Максимальная длина 255 символов
    content = RichTextUploadingField()

    def get_absolute_url(self):
        return reverse('board_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title



class Comment(models.Model): #Создает модель Comment для комментариев/откликов к объявлениям
    user = models.ForeignKey(User, on_delete = models.CASCADE) #Внешний ключ к пользователю (автор комментария)
    post = models.ForeignKey(Post, on_delete = models.CASCADE) #Внешний ключ к объявлению (связь комментария с конкретным постом)
    created_at = models.DateTimeField(auto_now_add=True) #Время создания комментария
    content = models.TextField() #Содержимое комментария
    status = models.BooleanField(default=False)

#Все модели идут в базу данных



