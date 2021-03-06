# Generated by Django 2.2 on 2019-05-14 18:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TypeForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('form_id', models.CharField(max_length=20, verbose_name='ID в тайпформ')),
                ('name', models.CharField(max_length=500, verbose_name='Название формы')),
            ],
            options={
                'verbose_name_plural': 'Формы',
                'verbose_name': 'Форма',
            },
        ),
        migrations.CreateModel(
            name='TypeFormQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.CharField(max_length=20, verbose_name='ID в тайпформ')),
                ('field_name', models.CharField(max_length=500, verbose_name='Название поля')),
                ('form', models.ForeignKey(on_delete=None, related_name='questions', to='typeform.TypeForm', verbose_name='TypeForm')),
            ],
            options={
                'verbose_name_plural': 'Вопросы в TypeForm',
                'verbose_name': 'Вопрос в TypeForm',
            },
        ),
        migrations.CreateModel(
            name='Result',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время создания')),
                ('submitted_at', models.DateTimeField(verbose_name='Время заполнения')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Название формы')),
                ('content', models.TextField(verbose_name='Содержимое формы')),
                ('hidden_id', models.CharField(blank=True, max_length=100, null=True, verbose_name='Скрытое поле идентификатор')),
                ('hidden_data', models.CharField(blank=True, max_length=100, null=True, verbose_name='Скрытые поля идентификаторы')),
                ('score', models.IntegerField(blank=True, null=True, verbose_name='Очки')),
                ('answers', models.TextField(blank=True, null=True, verbose_name='Ответы на вопросы')),
                ('form', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='results', to='typeform.TypeForm', verbose_name='Id формы')),
            ],
            options={
                'verbose_name_plural': 'Результаты TypeForm',
                'verbose_name': 'Результат TypeForm',
            },
        ),
    ]
