from django.urls import path
import comments.views as views

app_name = 'comments'

urlpatterns = [
    path('<str:id>', views.CommentView.as_view()),
	path('<str:id>/vote', views.CommentVoteView.as_view()),
	path('<str:id>/replies', views.CommentRepliesView.as_view()),
]
