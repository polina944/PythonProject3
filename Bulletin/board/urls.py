from django.urls import path
from board.views import (
    activate_user, home, PostListView, PostDetailView,
    PostCreateView, PostUpdateView, CommentListView,
    comment_accept, comment_delete,
)

urlpatterns = [
    path('', home, name='home'),
    path('activate_user/', activate_user, name='activate_user'),
    path('board/', PostListView.as_view(), name='board_list'),
    path('board/<int:pk>/', PostDetailView.as_view(), name='board_detail'),
    path('board/create/', PostCreateView.as_view(), name='board_create'),
    path('board/<int:pk>/update/', PostUpdateView.as_view(), name='board_update'),
    path('comments/', CommentListView.as_view(), name='comment_list'),
    path('comment/<int:comment_id>/accept/', comment_accept, name='comment_accept'),
    path('comment/<int:comment_id>/delete/', comment_delete, name='comment_delete'),
]
