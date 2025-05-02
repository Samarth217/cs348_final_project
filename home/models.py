from django.db import models

class Artist(models.Model):
    artist_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Genre(models.Model):
    genre_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Album(models.Model):
    album_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    release_year = models.IntegerField()

    def __str__(self):
        return self.title

class Song(models.Model):
    song_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    duration = models.FloatField(help_text='Duration in minutes')
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Playlist(models.Model):
    playlist_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class PlaylistSong(models.Model):
    playlist_song_id = models.AutoField(primary_key=True)
    playlist = models.ForeignKey(Playlist, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    #def __str__(self):
        #return f"{self.song.title} in {self.playlist.title}"
