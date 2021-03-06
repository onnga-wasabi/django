from django.db import models

# Create your models here.
'''
modelsに変更を加えたら
python manage.py makemigrarions　でマイグレーションを作成
python manage.py migrate　でデータベースにその変更を適用
'''
import datetime
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        '''
        １日以内に作成されたquestionの場合にTrueを返す
        '''
        return timezone.now() >= self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.short_description = 'Published recently?'
    # Tureの時に丸になるinstanse.boolean
    was_published_recently.boolean = True


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
