from django.shortcuts import render, redirect, get_object_or_404
from django.db import connection, transaction
from .models import (
    Song, Artist, Genre, Album,
    Playlist, PlaylistSong
)
from .forms import SongForm, PlaylistForm, AddSongsToPlaylistForm
from django.http import HttpResponse

# CRUD

def index(request):
    return HttpResponse("Hello World")

def song_list(request):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT s.song_id, s.title, s.duration,
                   a.name AS artist, g.name AS genre, al.title AS album
            FROM   home_song   s
            JOIN   home_artist a ON s.artist_id = a.artist_id
            JOIN   home_genre  g ON s.genre_id = g.genre_id
            JOIN   home_album  al ON s.album_id = al.album_id
            ORDER  BY s.song_id
        """)
        songs = cursor.fetchall()
    return render(request, "home/song_list.html", {"songs": songs})

def add_song(request):
    form = SongForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("song_list")
    return render(request, "home/add_edit_song.html", {"form": form, "action": "Add"})

def edit_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    form = SongForm(request.POST or None, instance=song)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("song_list")
    return render(request, "home/add_edit_song.html", {"form": form, "action": "Edit"})

def delete_song(request, song_id):
    get_object_or_404(Song, pk=song_id).delete()
    return redirect("song_list")

#  PLAYLIST 

def create_playlist_with_songs(request):
    """Create playlist + songs atomically."""
    playlist_form = PlaylistForm(request.POST or None)
    song_form     = AddSongsToPlaylistForm(request.POST or None)

    if request.method == "POST" and playlist_form.is_valid() and song_form.is_valid():
        with transaction.atomic():
            playlist = playlist_form.save()
            PlaylistSong.objects.bulk_create([
                PlaylistSong(playlist=playlist, song=s)
                for s in song_form.cleaned_data["songs"]
            ])
        return redirect("playlist_list")

    return render(
        request,
        "home/create_playlist.html",
        {"playlist_form": playlist_form, "song_form": song_form}
    )

def playlist_list(request):
    playlists = Playlist.objects.select_related("user").all()
    return render(request, "home/playlist_list.html", {"playlists": playlists})

def playlist_detail(request, playlist_id):

    playlist = get_object_or_404(
        Playlist.objects.select_related("user"), pk=playlist_id
    )

    #  Filter  
    selected_artist_id = request.GET.get("artist")
    selected_genre_id  = request.GET.get("genre")

    #  ORM 
    songs_qs = (Song.objects
                    .filter(playlistsong__playlist=playlist)
                    .select_related("artist", "genre", "album"))

    if selected_artist_id:
        songs_qs = songs_qs.filter(artist_id=selected_artist_id)
    if selected_genre_id:
        songs_qs = songs_qs.filter(genre_id=selected_genre_id)

    songs = songs_qs.order_by("title")

    base_filters = ["ps.playlist_id = %s"]
    params = [playlist_id]

    if selected_artist_id:
        base_filters.append("s.artist_id = %s")
        params.append(selected_artist_id)
    if selected_genre_id:
        base_filters.append("s.genre_id = %s")
        params.append(selected_genre_id)

    where_clause = " AND ".join(base_filters)

    # Prepared Statements
    with connection.cursor() as cur:
        # longest, shortest, avg
        cur.execute(f"""
            SELECT MAX(s.duration), MIN(s.duration), AVG(s.duration)
            FROM home_song s
            JOIN home_playlistsong ps ON ps.song_id = s.song_id
            WHERE {where_clause}
        """, params)
        max_dur, min_dur, avg_dur = cur.fetchone()

        # top artists
        cur.execute(f"""
            SELECT a.name, COUNT(*) cnt
            FROM home_song s
            JOIN home_artist a ON a.artist_id = s.artist_id
            JOIN home_playlistsong ps ON ps.song_id = s.song_id
            WHERE {where_clause}
            GROUP BY a.name
            HAVING COUNT(*) = (
                SELECT MAX(song_count)
                FROM (
                    SELECT COUNT(*) song_count
                    FROM home_song s2
                    JOIN home_playlistsong ps2 ON ps2.song_id = s2.song_id
                    WHERE {where_clause.replace("s.", "s2.").replace("ps.", "ps2.")}
                    GROUP BY s2.artist_id
                ) sub
            )
        """, params * 2) 

        top_artists = cur.fetchall()

    # dynamic dropdown
    artist_choices = (Artist.objects
                         .filter(song__playlistsong__playlist=playlist)
                         .distinct().order_by("name"))
    genre_choices  = (Genre.objects
                         .filter(song__playlistsong__playlist=playlist)
                         .distinct().order_by("name"))

    context = {
        "playlist": playlist,
        "songs": songs,
        "max_dur": max_dur,
        "min_dur": min_dur,
        "avg_dur": avg_dur,
        "top_artists": top_artists,
        "artist_choices": artist_choices,
        "genre_choices": genre_choices,
        "selected_artist_id": int(selected_artist_id) if selected_artist_id else "",
        "selected_genre_id": int(selected_genre_id) if selected_genre_id else "",
    }
    return render(request, "home/playlist_detail.html", context)
