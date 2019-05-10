from django.contrib import admin
from .models import Result, TypeForm, TypeFormQuestion
# Register your models here.


class ResultAdmin(admin.ModelAdmin):
    model = Result
    list_display = ('created_at', 'submitted_at', 'name',)
    readonly_fields = (
        'score',
        'created_at',
        'pretty_answers',
        'pretty_content',
    )
    exclude = ('content', 'answers',)


class TypeFormQuestionInline(admin.StackedInline):
    model = TypeFormQuestion


class TypeFormAdmin(admin.ModelAdmin):
    model = TypeForm
    list_display = ('name', 'form_id')
    inlines = (TypeFormQuestionInline, )


admin.site.register(Result, ResultAdmin)
admin.site.register(TypeForm, TypeFormAdmin)
