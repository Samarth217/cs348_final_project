from django.urls import path
from . import views

urlpatterns = [
    path('',                          views.index,                   name='index'),
    path('songs/',                    views.song_list,               name='song_list'),
    path('songs/add/',                views.add_song,                name='add_song'),
    path('songs/edit/<int:song_id>/', views.edit_song,               name='edit_song'),
    path('songs/delete/<int:song_id>/', views.delete_song,           name='delete_song'),

    path('playlists/create/',         views.create_playlist_with_songs, name='create_playlist'),
    path('playlists/',                views.playlist_list,           name='playlist_list'),
    path('playlists/<int:playlist_id>/', views.playlist_detail,      name='playlist_detail'),
]
