from django.db import models

# Create your models here.
from django.contrib.auth.models import User


class Poll(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField()

    start_date = models.DateTimeField(editable=False)
    end_date = models.DateTimeField()

    def __str__(self):
        return self.name



class Question(models.Model):
    class QuestionType(models.TextChoices):
        text = "text", "Text answer"
        singlechoice = "singlechoice", "single option"
        multichoice = 'multichoice', "many options"

    poll = models.ForeignKey("polls.Poll", on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    type = models.CharField(
        max_length=50,
        choices=QuestionType.choices,
        default=QuestionType.text
    )

    # check if its singlechoice field
    @property
    def has_choise(self):
        return self.type in (self.QuestionType.singlechoice, self.QuestionType.multichoice)



class ChoiceAnswer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.TextField()

    """
    Allow to add choices just for questions with choice or multi_choice type in database level
    """
    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        if self.question.has_choise:

            cur_choies = ChoiceAnswer.objects.filter(question=self.question).exists()
            if self.question.type == Question().QuestionType.singlechoice and cur_choies:
                raise ValueError("Cant use more than one singlechoice for singlechoicefield")
        else:
            raise ValueError("Cant set singlechoice for text quiestion")

        return super().save(force_insert, force_update, using, update_fields)


    def __str__(self):
        return self.text



    class Meta:
        unique_together = ['text', 'question']



class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField(null=True, blank=True)
    choice = models.ManyToManyField(ChoiceAnswer, blank=True)

    # user = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    anon_token = models.CharField(max_length=256, blank=True, null=True)

    class Meta:
        unique_together = [
            ['question',"user", "anon_token"],
        ]




