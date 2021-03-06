import copy


class Backend(object):
    #: Actor proxy to an instance of :class:`mopidy.audio.Audio`.
    #:
    #: Should be passed to the backend constructor as the kwarg ``audio``,
    #: which will then set this field.
    audio = None

    #: The library provider. An instance of
    # :class:`mopidy.backends.base.BaseLibraryProvider`.
    library = None

    #: The playback provider. An instance of
    #: :class:`mopidy.backends.base.BasePlaybackProvider`.
    playback = None

    #: The stored playlists provider. An instance of
    #: :class:`mopidy.backends.base.BaseStoredPlaylistsProvider`.
    stored_playlists = None

    #: List of URI schemes this backend can handle.
    uri_schemes = []


class BaseLibraryProvider(object):
    """
    :param backend: backend the controller is a part of
    :type backend: :class:`mopidy.backends.base.Backend`
    """

    pykka_traversable = True

    def __init__(self, backend):
        self.backend = backend

    def find_exact(self, **query):
        """
        See :meth:`mopidy.core.LibraryController.find_exact`.

        *MUST be implemented by subclass.*
        """
        raise NotImplementedError

    def lookup(self, uri):
        """
        See :meth:`mopidy.core.LibraryController.lookup`.

        *MUST be implemented by subclass.*
        """
        raise NotImplementedError

    def refresh(self, uri=None):
        """
        See :meth:`mopidy.core.LibraryController.refresh`.

        *MUST be implemented by subclass.*
        """
        raise NotImplementedError

    def search(self, **query):
        """
        See :meth:`mopidy.core.LibraryController.search`.

        *MUST be implemented by subclass.*
        """
        raise NotImplementedError


class BasePlaybackProvider(object):
    """
    :param audio: the audio actor
    :type audio: actor proxy to an instance of :class:`mopidy.audio.Audio`
    :param backend: the backend
    :type backend: :class:`mopidy.backends.base.Backend`
    """

    pykka_traversable = True

    def __init__(self, audio, backend):
        self.audio = audio
        self.backend = backend

    def pause(self):
        """
        Pause playback.

        *MAY be reimplemented by subclass.*

        :rtype: :class:`True` if successful, else :class:`False`
        """
        return self.audio.pause_playback().get()

    def play(self, track):
        """
        Play given track.

        *MAY be reimplemented by subclass.*

        :param track: the track to play
        :type track: :class:`mopidy.models.Track`
        :rtype: :class:`True` if successful, else :class:`False`
        """
        self.audio.prepare_change()
        self.audio.set_uri(track.uri).get()
        return self.audio.start_playback().get()

    def resume(self):
        """
        Resume playback at the same time position playback was paused.

        *MAY be reimplemented by subclass.*

        :rtype: :class:`True` if successful, else :class:`False`
        """
        return self.audio.start_playback().get()

    def seek(self, time_position):
        """
        Seek to a given time position.

        *MAY be reimplemented by subclass.*

        :param time_position: time position in milliseconds
        :type time_position: int
        :rtype: :class:`True` if successful, else :class:`False`
        """
        return self.audio.set_position(time_position).get()

    def stop(self):
        """
        Stop playback.

        *MAY be reimplemented by subclass.*

        :rtype: :class:`True` if successful, else :class:`False`
        """
        return self.audio.stop_playback().get()

    def get_time_position(self):
        """
        Get the current time position in milliseconds.

        *MAY be reimplemented by subclass.*

        :rtype: int
        """
        return self.audio.get_position().get()


class BaseStoredPlaylistsProvider(object):
    """
    :param backend: backend the controller is a part of
    :type backend: :class:`mopidy.backends.base.Backend`
    """

    pykka_traversable = True

    def __init__(self, backend):
        self.backend = backend
        self._playlists = []

    @property
    def playlists(self):
        """
        Currently stored playlists.

        Read/write. List of :class:`mopidy.models.Playlist`.
        """
        return copy.copy(self._playlists)

    @playlists.setter  # noqa
    def playlists(self, playlists):
        self._playlists = playlists

    def create(self, name):
        """
        See :meth:`mopidy.core.StoredPlaylistsController.create`.

        *MUST be implemented by subclass.*
        """
        raise NotImplementedError

    def delete(self, uri):
        """
        See :meth:`mopidy.core.StoredPlaylistsController.delete`.

        *MUST be implemented by subclass.*
        """
        raise NotImplementedError

    def lookup(self, uri):
        """
        See :meth:`mopidy.core.StoredPlaylistsController.lookup`.

        *MUST be implemented by subclass.*
        """
        raise NotImplementedError

    def refresh(self):
        """
        See :meth:`mopidy.core.StoredPlaylistsController.refresh`.

        *MUST be implemented by subclass.*
        """
        raise NotImplementedError

    def save(self, playlist):
        """
        See :meth:`mopidy.core.StoredPlaylistsController.save`.

        *MUST be implemented by subclass.*
        """
        raise NotImplementedError
