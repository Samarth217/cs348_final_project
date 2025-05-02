from django import forms
from .models import Song, Playlist

class SongForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ['title', 'duration', 'artist', 'genre', 'album']
        widgets = {
            'title':    forms.TextInput(attrs={'class': 'form-control'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.1, 'min': 0}),
            'artist':   forms.Select(attrs={'class': 'form-select'}),
            'genre':    forms.Select(attrs={'class': 'form-select'}),
            'album':    forms.Select(attrs={'class': 'form-select'}),
        }

#playlists

class PlaylistForm(forms.ModelForm):
    class Meta:
        model  = Playlist
        fields = ['title', 'user']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'user':  forms.Select(attrs={'class': 'form-select'}),
        }

class AddSongsToPlaylistForm(forms.Form):
    songs = forms.ModelMultipleChoiceField(
        queryset=Song.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Select songs to add"
    )
