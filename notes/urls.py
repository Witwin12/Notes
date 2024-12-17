from django.urls import path
from . import views

app_name = 'notes'

urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("<int:pk>/", views.DetailView.as_view(), name="detail"),
    path("directory/", views.directory_browser, name="directory_browser"),
    path("directory/<path:path>/", views.directory_browser, name="directory_browser_with_path"),
]
