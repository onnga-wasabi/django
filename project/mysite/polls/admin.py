from django.contrib import admin

# Register your models here.
from .models import Question, Choice


# class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    # admin/pollsに表示するリスト
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    # 右横のリストバー
    list_filter = ['pub_date']
    # 検索窓
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
# admin.site.register(Choice)
