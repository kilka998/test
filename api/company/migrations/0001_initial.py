# Generated by Django 3.2.4 on 2023-06-02 14:07

import core.utils
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('name', models.CharField(max_length=100, verbose_name='Название отдела')),
            ],
            options={
                'verbose_name': 'Отдел',
                'verbose_name_plural': 'Отделы',
            },
        ),
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('full_name', models.CharField(max_length=100, verbose_name='Полное имя сотрудника')),
                ('photo', models.ImageField(default='img/photo.jpg', upload_to='photos/', verbose_name='Фото сотрудника')),
                ('position', models.CharField(max_length=100, verbose_name='Должность')),
                ('salary', models.DecimalField(decimal_places=2, max_digits=8, verbose_name='Оклад')),
                ('age', models.IntegerField(verbose_name='Возраст')),
                ('department', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employees', to='company.department', verbose_name='Отдел')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
            },
        ),
        migrations.CreateModel(
            name='UserToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('key', models.CharField(default=core.utils.generate_token, max_length=40, verbose_name='Ключ')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tokens', to='company.employee', verbose_name='Сотрудник')),
            ],
            options={
                'verbose_name': 'Токен',
                'verbose_name_plural': 'Токены',
                'db_table': 'users_user_token',
            },
        ),
        migrations.AddField(
            model_name='department',
            name='director',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='departments', to='company.employee', verbose_name='Директор отдела'),
        ),
    ]
