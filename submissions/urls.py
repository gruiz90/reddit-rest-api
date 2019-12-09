from django.urls import path
import submissions.views as views

app_name = 'submissions'

urlpatterns = [
	path('<str:id>', views.SubmissionView.as_view()),
	path('<str:id>/vote', views.SubmissionVoteView.as_view()),
	path('<str:id>/comments', views.SubmissionCommentsView.as_view()),
]