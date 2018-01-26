from django.db import models

# Create your models here.
'''
modelsに変更を加えたら
python manage.py makemigrarions　でマイグレーションを作成
python manage.py migrate　でデータベースにその変更を適用
'''


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
