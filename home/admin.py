from django.contrib import admin
from .models import Artist, Genre, Album, Song, User, Playlist, PlaylistSong

admin.site.register(Artist)
admin.site.register(Genre)
admin.site.register(Album)
admin.site.register(Song)
admin.site.register(User)
admin.site.register(Playlist)
admin.site.register(PlaylistSong)