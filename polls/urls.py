from . import views
from django.urls import path, include
from rest_framework_nested import routers


router = routers.DefaultRouter()
router.register(r'polls', views.PollAdminViewSet, basename="poll_admin")

domains_router = routers.NestedSimpleRouter(router, r'polls', lookup='poll')
domains_router.register(r'questions', views.QusetionAdminViewSet, basename='poll-question')


urlpatterns = [
    path("admin/", include(router.urls)),
    path("admin/", include(domains_router.urls)),

    path("user/answer/", views.UserPollAPIViewSet.as_view({'post': "get_answer"}), name='get_answer'),
    path("user/question_list/<int:poll_pk>/", views.UserPollAPIViewSet.as_view({"get": "get_questions"}), name='get_qustions'),
    path("user/actual_polls/", views.UserPollAPIViewSet.as_view({"get": "get_active_polls"}), name='get_qustions'),
    path('user/done_polls/<str:user_id>/', views.UserPollAPIViewSet.as_view({"get":"get_completed_polls"}), name='get_completed_polls'),
]





