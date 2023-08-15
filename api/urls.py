from django.urls import path
from .views import UploadView, ChatView, ListCollectionsView

urlpatterns = [
    path('upload', UploadView.as_view(), name='upload'),
    path('chat', ChatView.as_view(), name='chat'),
    path('collections/', ListCollectionsView.as_view(), name='list-collections'),
]
