from rest_framework import serializers
from .models import Answer, Question, Poll


# validation of user and session
def validate_user_or_session(user_id, session_id):
    if not (user_id or session_id):
        raise serializers.ValidationError("User or session must be NOT empty")

    if user_id and session_id:
        raise serializers.ValidationError("You need to enter user_id OR sessionID")


# get actual questions for poll
def get_questions(poll, user=None, token=None):
    from django.db.models import Q

    # get all answers from this user or anonim for this poll
    answers = Answer.objects.filter(Q(user=user) | Q(anon_token=token), question__poll=poll)

    # get all questions for this poll excluded answers
    questions = Question.objects.filter(poll=poll).exclude(answer__in=answers)

    return questions


# get poll by pk
def poll_by_pk(poll_pk):
    poll = Poll.objects.filter(pk=poll_pk)
    if poll.exists():
        return poll.first()
    else:
        raise serializers.ValidationError("Invalid poll pk")


# get user by id
def get_user_by_id(user_id):
    from django.contrib.auth.models import User
    try:

        user = User.objects.get(id=user_id)
        return user

    except:
        raise serializers.ValidationError("User with this ID not defined")




# find user completed polls
def get_completed_polls(user=None, token=None):
    from django.db.models import Q

    polls_of_user = Poll.objects.filter((Q(questions__answer__user=user) & Q(questions__answer__anon_token=None)) |
                                        (Q(questions__answer__anon_token=token) & Q(questions__answer__user=None)))

    all_answers_of_user = Answer.objects.filter((Q(user=user) & Q(anon_token=None)) |
                                                 (Q(user=None) & Q(anon_token=token)))

    answers = {}
    for answer in all_answers_of_user:
        if not answer.question.poll in answers:
            answers[answer.question.poll] = 1
        else:
            answers[answer.question.poll] += 1


    # all question in poll
    questions = {}
    for poll in polls_of_user:
        questions[poll] = poll.questions.count()

    # all polls with answers == questions
    completed_polls = {}
    for poll, count in answers.items():
        if questions[poll] == count:
            completed_polls[poll] = None

    """
    Set answers queryset to Poll field
    
    Make list from dict
    """
    to_res = []
    for poll, item in completed_polls.items():
        poll.answers = all_answers_of_user.filter(question__poll=poll)
        to_res.append(poll)



    return to_res



