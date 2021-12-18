from django.db import models
from import_export.resources import ModelResource


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    @staticmethod
    def get_export_resources():
        return {
            'rsc1': ('Question', QuestionResource),
        }


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)


class QuestionResource(ModelResource):
    class Meta:
        model = Question
