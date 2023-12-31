from django.urls import path
from . import views




urlpatterns = [
    path("", views.StartingPageView.as_view(), name="starting-page"),
    path("gallery", views.GalleryPageView, name="gallery-page"),
    path("posts",views.AllPostsView.as_view(), name="post-page"),
    path("posts/<slug:slug>", views.SinglePostsView.as_view(), name="post-detail-page"),    
    path("read-later", views.ReadLaterView.as_view(), name="read-later"),
    path('indexview', views.indexview, name='indexview-page')
]
