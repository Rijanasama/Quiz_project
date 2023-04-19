from django.contrib import admin

# Register your models here.
from .models import *


class AnswerAdmin(admin.StackedInline):
    model = Choice

class QuestionAdmin(admin.ModelAdmin):
    inlines = [AnswerAdmin]

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
admin.site.register(Marks)