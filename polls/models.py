import uuid

from django.db import models
from django.contrib.auth.models import User
import random
from django.core.validators import MinValueValidator, MaxValueValidator
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    marks=models.IntegerField(default=1)
    def __str__(self):
        return self.question_text
    def get_answers(self):
        answers=list(Choice.objects.filter(question=self))
        random.shuffle(answers)
        data =[]
        for answer in answers:
            data.append({
                'options':answer.option,
                'is_correct_option':answer.is_correct_option
            })
        return data


class Choice(models.Model):
    question = models.ForeignKey(Question,related_name='question_answer', on_delete=models.CASCADE)
    option = models.CharField(max_length=200)
    is_correct_option=models.BooleanField(default=False)
    def __str__(self):
        return self.option

class Marks(models.Model):
    user=models.CharField(max_length=200)
    score=models.IntegerField(default=0,validators=[MinValueValidator(0), MaxValueValidator(5)])


