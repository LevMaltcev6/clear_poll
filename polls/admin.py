from django.contrib import admin
from .models import Question, Poll, ChoiceAnswer, Answer
# Register your models here.

admin.site.register(Poll)
admin.site.register(ChoiceAnswer)
admin.site.register(Question)
admin.site.register(Answer)


