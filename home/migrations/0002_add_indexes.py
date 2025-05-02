from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ("home", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE INDEX IF NOT EXISTS idx_song_artist_id
                    ON home_song(artist_id);
                CREATE INDEX IF NOT EXISTS idx_song_genre_id
                    ON home_song(genre_id);
                CREATE INDEX IF NOT EXISTS idx_song_album_id
                    ON home_song(album_id);
                CREATE INDEX IF NOT EXISTS idx_playlistsong_playlist_song
                    ON home_playlistsong(playlist_id, song_id);
            """,
            reverse_sql="""
                DROP INDEX IF EXISTS idx_song_artist_id;
                DROP INDEX IF EXISTS idx_song_genre_id;
                DROP INDEX IF EXISTS idx_song_album_id;
                DROP INDEX IF EXISTS idx_playlistsong_playlist_song;
            """,
        ),
    ]
