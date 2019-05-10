from django.db import models
import json
import logging
from pygments import highlight
from pygments.lexers import JsonLexer
from pygments.formatters import HtmlFormatter
from django.utils.safestring import mark_safe

logger = logging.getLogger(__name__)


class Result(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='Время создания',
    )
    submitted_at = models.DateTimeField(
        blank=False, null=False, verbose_name='Время заполнения'
    )
    form = models.ForeignKey(
        'TypeForm', models.CASCADE,
        null=True, blank=True,
        verbose_name='Id формы',
        related_name='results',
    )
    name = models.CharField(
        max_length=255, verbose_name='Название формы',
        blank=True, null=True
    )
    content = models.TextField(
        verbose_name='Содержимое формы',
        blank=False, null=False,
    )
    hidden_id = models.CharField(
        blank=True, null=True, max_length=100,
        verbose_name='Скрытое поле идентификатор'
    )
    hidden_data = models.CharField(
        blank=True, null=True, max_length=100,
        verbose_name='Скрытые поля идентификаторы'
    )
    score = models.IntegerField(
        null=True, blank=True,
        verbose_name='Очки'
    )
    answers = models.TextField(
        verbose_name='Ответы на вопросы',
        null=True, blank=True
    )

    def __str__(self):
        return self.name

    def pretty_content(self):
        if not self.answers:
            return ''
        try:
            points = json.dumps(
                json.loads(self.content), sort_keys=True,
                indent=2, ensure_ascii=False
            )
        except Exception as e:
            logger.error('Parsing content error %s' % e)
            return ''
        formatter = HtmlFormatter(style='colorful')
        output = highlight(points, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        return mark_safe(style + output)
    pretty_content.allow_tags = True
    pretty_content.short_description = 'Содержимое ответа'

    def pretty_answers(self):
        if not self.answers:
            return ''
        try:
            points = json.dumps(
                json.loads(self.answers), sort_keys=True,
                indent=2, ensure_ascii=False
            )
        except Exception as e:
            logger.error('Parsing content error %s' % e)
            return ''
        formatter = HtmlFormatter(style='colorful')
        output = highlight(points, JsonLexer(), formatter)
        style = "<style>" + formatter.get_style_defs() + "</style><br>"
        return mark_safe(style + output)
    pretty_answers.allow_tags = True
    pretty_answers.short_description = 'Ответы'

    class Meta:
        verbose_name = 'Результат TypeForm'
        verbose_name_plural = 'Результаты TypeForm'


class TypeForm(models.Model):
    form_id = models.CharField(max_length=20, verbose_name='ID в тайпформ')
    name = models.CharField(max_length=500, verbose_name='Название формы')

    class Meta:
        verbose_name = "Форма"
        verbose_name_plural = "Формы"

    def __str__(self):
        return self.name


class TypeFormQuestion(models.Model):
    form = models.ForeignKey(
        TypeForm, related_name='questions',
        verbose_name='TypeForm', on_delete=None
    )
    question_id = models.CharField(max_length=20, verbose_name='ID в тайпформ')
    field_name = models.CharField(max_length=500, verbose_name='Название поля')

    class Meta:
        verbose_name = "Вопрос в TypeForm"
        verbose_name_plural = "Вопросы в TypeForm"
