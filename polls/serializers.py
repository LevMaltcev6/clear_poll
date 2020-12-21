from rest_framework import serializers
from .models import Poll, Question, Answer, ChoiceAnswer
from rest_framework.exceptions import ValidationError


class PollBaseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Poll
        fields = '__all__'

class CreatePollAdminSerializer(PollBaseSerializer):
    start_date = serializers.DateTimeField(write_only=True)

class ChoiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChoiceAnswer
        fields = "__all__"
# -------------------------------------
class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        # fields = "__all__"
        fields = ['text', 'type', 'choices']
# ------------------------


class QuestionForUserSerializer(serializers.ModelSerializer):
    # choices = serializers.PrimaryKeyRelatedField(many=True, required=False, read_only=True)
    choices = ChoiceSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Question
        fields = "__all__"
# -----------------------------------

# Answer serializer
class AnswerSerializer(serializers.ModelSerializer):

    def validate(self, attrs):
        qtype = attrs.get('question').type
        if qtype == "text":
            if attrs.get("choice") != None:
                raise ValidationError("This is text question, not choice")

        elif qtype == "singlechoice":
            if len(attrs.get("choice")) > 1:
                raise ValidationError("This quiestion is just for one choice not many")
            if attrs.get('text') != None:
                raise ValidationError("Choice field not contains text")

        elif qtype == "multichoice":
            if attrs.get('text') != None:
                raise ValidationError("Choice field not contains text")

        return super().validate(attrs)

    class Meta:
        model = Answer
        fields = "__all__"


# completed polls serializer
class CompletedPollsSerializer(serializers.ModelSerializer):

    answers = AnswerSerializer(many=True, read_only=True)

    class Meta:
        model = Poll
        fields = "__all__"


