from django.db import models
from core.utils import generate_token
from core.models import BaseModel


class Department(BaseModel):
    name = models.CharField(
        max_length=100,
        verbose_name='Название отдела',
    )
    director = models.OneToOneField(
        'Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='departments',
        verbose_name='Директор отдела',
    )

    class Meta:
        verbose_name = 'Отдел'
        verbose_name_plural = 'Отделы'

    def __str__(self):
        return self.name
    
    @property
    def director_name(self):
        return self.director.full_name if self.director else None 

class Employee(BaseModel):
    full_name = models.CharField(
        max_length=100,
        verbose_name='Полное имя сотрудника',
    )
    photo = models.ImageField(
        upload_to='photos/',
        default='img/photo.jpg',
        verbose_name='Фото сотрудника',
    )
    position = models.CharField(
        max_length=100,
        verbose_name='Должность',
    )
    salary = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Оклад',
    )
    age = models.IntegerField(verbose_name='Возраст', )
    department = models.ForeignKey(
        'Department',
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name='Отдел',
    )
    # Это поле создано исключительно для проверки токена актуальных юзеров
    is_active = models.BooleanField(
        verbose_name='Актуальный сотрудник',
        default=True,
    )

    class Meta:
        verbose_name = 'Сотрудник'
        verbose_name_plural = 'Сотрудники'

    def __str__(self):
        return self.full_name
    
    def get_token(self):
        return UserToken.objects.filter(user=self).order_by('updated').first()

    def create_token(self):
        tokens = UserToken.objects.filter(user=self).order_by('updated')
        # TODO убрать число в консты
        if len(tokens) < 2:
            token = UserToken.objects.create(user=self)
        else:
            token = tokens[0]
            token.refresh_token()

        return token

    @property
    def is_authenticated(self):
        """
        Always return True. This is a way to tell if the user has been
        authenticated in templates.
        """
        return True

class UserToken(BaseModel):
    user = models.ForeignKey(
        'Employee',
        related_name='tokens',
        on_delete=models.CASCADE,
        verbose_name='Сотрудник',
    )
    key = models.CharField('Ключ', max_length=40, default=generate_token)

    class Meta:
        db_table = 'users_user_token'
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'

    def refresh_token(self):
        self.key = generate_token()
        self.save(update_fields=('key',))

    def __str__(self):
        return '{owner} {key}'.format(owner=self.user.full_name, key=self.key)