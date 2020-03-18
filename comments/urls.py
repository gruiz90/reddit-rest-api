from django.urls import path
import comments.views as views

app_name = 'comments'

urlpatterns = [
    path('<str:id>', views.CommentView.as_view(), name='comment_info'),
    path('<str:id>/vote', views.CommentVoteView.as_view(), name='comment_vote'),
    path('<str:id>/reply', views.CommentReplyView.as_view(), name='comment_reply'),
    path(
        '<str:id>/replies', views.CommentRepliesView.as_view(), name='comment_replies'
    ),
]
