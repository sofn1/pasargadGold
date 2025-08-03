from django.urls import path
from .views import (
    CommentCreateView, CommentListView, CommentUpdateDeleteView, ToggleLikeView
)

urlpatterns = [
    path('', CommentCreateView.as_view(), name='comment_create'),
    path('<str:model>/<int:object_id>/', CommentListView.as_view(), name='comment_list'),
    path('<int:pk>/edit/', CommentUpdateDeleteView.as_view(), name='comment_update_delete'),
    path('<int:comment_id>/like/', ToggleLikeView.as_view(), name='comment_like_toggle'),
]
