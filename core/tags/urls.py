from django.urls import path
from .views import (
    TagListCreateAPIView,
    TagRetrieveUpdateDestroyAPIView,
    tag_select2,
)

app_name = "tags"

urlpatterns = [
    # REST
    path("api/tags/", TagListCreateAPIView.as_view(), name="api_list_create"),
    path("api/tags/<int:pk>/", TagRetrieveUpdateDestroyAPIView.as_view(), name="api_detail"),
    path("api/tags/select2/", tag_select2, name="api_select2"),
]
