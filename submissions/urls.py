from django.urls import path
import submissions.views as views

app_name = 'submissions'

urlpatterns = [
    path('<str:id>', views.SubmissionView.as_view(), name='submission_info'),
    path('<str:id>/vote', views.SubmissionVoteView.as_view(), name='submission_vote'),
    path('<str:id>/reply', views.SubmissionReplyView.as_view(), name='submission_reply'),
    path(
        '<str:id>/comments',
        views.SubmissionCommentsView.as_view(),
        name='submission_comments',
    ),
]
