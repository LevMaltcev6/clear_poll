from rest_framework import  status, viewsets, permissions, serializers
from rest_framework.response import Response
from .models import Poll, Question, Answer, ChoiceAnswer
from rest_framework.exceptions import MethodNotAllowed

from drf_spectacular.utils import extend_schema, OpenApiParameter
from .serializers import PollBaseSerializer, CreatePollAdminSerializer
from . import serializers


"""
Unnecessary method PUT in all viewsets
"""
class BlockPut:
    http_method_names = ['get','post','patch','options','head', 'delete'] # ALL not PUT

"""
Poll Admin ViewSet
"""
class PollAdminViewSet(BlockPut, viewsets.ModelViewSet):
    model = Poll
    queryset = Poll.objects.all()
    permission_classes = [permissions.IsAdminUser]

    def get_serializer_class(self):
        if self.action == "create":
            return CreatePollAdminSerializer
        else:
            return PollBaseSerializer

"""
Question Admin ViewSet
"""
class QusetionAdminViewSet(BlockPut, viewsets.ModelViewSet):
    model = Question
    queryset = Question.objects.all()
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.QuestionSerializer


    def list(self, request, poll_pk=None, *args, **kwargs):
        self.queryset = Question.objects.filter(poll=poll_pk)

        return super().list(request, *args,**kwargs)

    def create(self, request, poll_pk=None, *args, **kwargs):
        request.data['poll'] = poll_pk

        return super().create(request, *args, **kwargs)

    def partial_update(self, request, poll_pk=None, *args, **kwargs):
        request.data['poll'] = poll_pk

        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, poll_pk=None, *args, **kwargs):
        request.data['poll'] = poll_pk

        return super().destroy(request, *args, **kwargs)

    def update(self, request,poll_pk=None, *args, **kwargs):
        request.data['poll'] = poll_pk

        return super().update(request, *args, **kwargs)

"""
User usage ViewSet

API has methods:
get_active_polls = list of active polls
get_answer = get one answer per call from user
get_questions = get list of questions from chosen poll
"""
class UserPollAPIViewSet(viewsets.ModelViewSet):
    model = Answer
    queryset = Answer.objects.all()
    serializer_class = serializers.AnswerSerializer
    lookup_field = 'poll_pk'

    def get_serializer_class(self):
        """
        For answer and questions - find poll_pk.

        For get_active_polls method without poll_pk
        """
        if self.action == "get_answer":
            return serializers.AnswerSerializer

        elif self.action == "get_questions":
            return serializers.QuestionForUserSerializer

        elif self.action == "get_active_polls":
            return serializers.PollBaseSerializer

        elif self.action == "get_completed_polls":
            return serializers.CompletedPollsSerializer
        else:
            print("error")
            return serializers.AnswerSerializer

    """ list of actual polls """
    @property
    def actual_polls(self):
        from django.utils.timezone import now

        return Poll.objects.filter(start_date__lt=now(), end_date__gt=now())


    """ GET method to take list of actual polls """
    def get_active_polls(self, request, *args, **kwargs):
        self.queryset = self.actual_polls
        self.serializer_class = self.get_serializer_class()

        return super().list(request, args, kwargs)


    """ POST method function to take answer from user"""
    def get_answer(self, request, *args, **kwargs):
        self.serializer_class = self.get_serializer_class()
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'success': "your answer correctly saved"}, status=status.HTTP_200_OK)


    """ GET method to get list of questions from chosen poll """
    @extend_schema(
        parameters=[
            OpenApiParameter(name='user_id', description='user id', required=False, type=int),
            OpenApiParameter(name='sessionid', description='session id', required=False, type=str)
        ]
    )
    def get_questions(self, request, poll_pk=None, *args, **kwargs):
        from .utils import validate_user_or_session, get_questions, poll_by_pk
        # user id and session id from params
        user_id = request.query_params.get('user_id')
        sessionid = request.query_params.get('sessionid')
        validate_user_or_session(user_id, sessionid)

        # getting poll object with pk from parameter
        poll = poll_by_pk(poll_pk)
        questions = get_questions(poll, user_id, sessionid)

        if not questions:
            return Response("You completed this poll", status=status.HTTP_204_NO_CONTENT)

        # paginate output
        self.serializer_class = self.get_serializer_class()
        page = self.paginate_queryset(questions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(questions, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    """
    GET method to get list of completed polls for chosen user
    """
    def get_completed_polls(self, request, user_id=None, *args, **kwargs):
        from .utils import get_user_by_id, get_completed_polls
        user = get_user_by_id(user_id)

        data = get_completed_polls(user=user, token=user_id)

        self.serializer_class = self.get_serializer_class()
        serializer = self.serializer_class(data=data, many=True)
        serializer.is_valid()

        return Response(serializer.data, status=status.HTTP_200_OK)





