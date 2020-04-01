from django.urls import path
import submissions.views as views

app_name = 'submissions'

urlpatterns = [
    path('<str:id>', views.Submission.as_view(), name='submission'),
    path('<str:id>/vote', views.SubmissionVote.as_view(), name='submission_vote'),
    path('<str:id>/reply', views.SubmissionReply.as_view(), name='submission_reply'),
    path(
        '<str:id>/crosspost',
        views.SubmissionCrosspost.as_view(),
        name='submission_crosspost',
    ),
    path(
        '<str:id>/comments',
        views.SubmissionComments.as_view(),
        name='submission_comments',
    ),
]
