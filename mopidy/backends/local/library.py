import logging

from mopidy import settings
from mopidy.backends import base
from mopidy.models import Playlist, Album

from .translator import parse_mpd_tag_cache

logger = logging.getLogger(u'mopidy.backends.local')


class LocalLibraryProvider(base.BaseLibraryProvider):
    def __init__(self, *args, **kwargs):
        super(LocalLibraryProvider, self).__init__(*args, **kwargs)
        self._uri_mapping = {}
        self.refresh()

    def refresh(self, uri=None):
        tracks = parse_mpd_tag_cache(
            settings.LOCAL_TAG_CACHE_FILE, settings.LOCAL_MUSIC_PATH)

        logger.info(
            'Loading tracks from %s using %s',
            settings.LOCAL_MUSIC_PATH, settings.LOCAL_TAG_CACHE_FILE)

        for track in tracks:
            self._uri_mapping[track.uri] = track

    def lookup(self, uri):
        try:
            return self._uri_mapping[uri]
        except KeyError:
            logger.debug(u'Failed to lookup %r', uri)
            return None

    def find_exact(self, **query):
        self._validate_query(query)
        result_tracks = self._uri_mapping.values()

        for (field, values) in query.iteritems():
            if not hasattr(values, '__iter__'):
                values = [values]
            # FIXME this is bound to be slow for large libraries
            for value in values:
                q = value.strip()

                track_filter = lambda t: q == t.name
                album_filter = lambda t: q == getattr(t, 'album', Album()).name
                artist_filter = lambda t: filter(
                    lambda a: q == a.name, t.artists)
                uri_filter = lambda t: q == t.uri
                any_filter = lambda t: (
                    track_filter(t) or album_filter(t) or
                    artist_filter(t) or uri_filter(t))

                if field == 'track':
                    result_tracks = filter(track_filter, result_tracks)
                elif field == 'album':
                    result_tracks = filter(album_filter, result_tracks)
                elif field == 'artist':
                    result_tracks = filter(artist_filter, result_tracks)
                elif field in ('uri', 'filename'):
                    result_tracks = filter(uri_filter, result_tracks)
                elif field == 'any':
                    result_tracks = filter(any_filter, result_tracks)
                else:
                    raise LookupError('Invalid lookup field: %s' % field)
        return Playlist(tracks=result_tracks)

    def search(self, **query):
        self._validate_query(query)
        result_tracks = self._uri_mapping.values()

        for (field, values) in query.iteritems():
            if not hasattr(values, '__iter__'):
                values = [values]
            # FIXME this is bound to be slow for large libraries
            for value in values:
                q = value.strip().lower()

                track_filter = lambda t: q in t.name.lower()
                album_filter = lambda t: q in getattr(
                    t, 'album', Album()).name.lower()
                artist_filter = lambda t: filter(
                    lambda a: q in a.name.lower(), t.artists)
                uri_filter = lambda t: q in t.uri.lower()
                any_filter = lambda t: track_filter(t) or album_filter(t) or \
                    artist_filter(t) or uri_filter(t)

                if field == 'track':
                    result_tracks = filter(track_filter, result_tracks)
                elif field == 'album':
                    result_tracks = filter(album_filter, result_tracks)
                elif field == 'artist':
                    result_tracks = filter(artist_filter, result_tracks)
                elif field in ('uri', 'filename'):
                    result_tracks = filter(uri_filter, result_tracks)
                elif field == 'any':
                    result_tracks = filter(any_filter, result_tracks)
                else:
                    raise LookupError('Invalid lookup field: %s' % field)
        return Playlist(tracks=result_tracks)

    def _validate_query(self, query):
        for (_, values) in query.iteritems():
            if not values:
                raise LookupError('Missing query')
            for value in values:
                if not value:
                    raise LookupError('Missing query')
