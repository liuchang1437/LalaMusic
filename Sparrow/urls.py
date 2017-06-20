from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'song/(\d+)/$', views.play_song, name='play_song'),
	url(r'$', views.search, name='search'),
]
