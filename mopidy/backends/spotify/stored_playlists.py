from mopidy.backends import base


class SpotifyStoredPlaylistsProvider(base.BaseStoredPlaylistsProvider):
    def create(self, name):
        pass  # TODO

    def delete(self, playlist):
        pass  # TODO

    def lookup(self, uri):
        pass  # TODO

    def refresh(self):
        pass  # TODO

    def rename(self, playlist, new_name):
        pass  # TODO

    def save(self, playlist):
        pass  # TODO
