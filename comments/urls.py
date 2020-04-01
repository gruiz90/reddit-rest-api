from django.urls import path
import comments.views as views

app_name = 'comments'

urlpatterns = [
    path('<str:id>', views.Comment.as_view(), name='comment'),
    path('<str:id>/vote', views.CommentVote.as_view(), name='comment_vote'),
    path('<str:id>/replies', views.CommentReplies.as_view(), name='comment_replies'),
]
