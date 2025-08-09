from django.urls import path
from .views import comment_page, comment_edit, comment_delete, toggle_like

urlpatterns = [
    # Thread page (list + create + reply)
    path("<str:model>/<int:object_id>/", comment_page, name="comment_thread"),

    # Edit/Delete
    path("<int:pk>/edit/", comment_edit, name="comment_edit"),
    path("<int:pk>/delete/", comment_delete, name="comment_delete"),

    # Like toggle
    path("<int:comment_id>/like/", toggle_like, name="comment_like_toggle"),
]
