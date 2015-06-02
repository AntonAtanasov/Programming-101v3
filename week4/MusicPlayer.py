import json
import random


class SongLength:

    def __init__(self, length):
        self.length = length
        self.hours = 0
        self.minutes = 0
        self.seconds = 0

        parts = [int(part.strip()) for part in length.split(":")]

        if len(parts) == 3:
            self.hours = parts[0]
            self.minutes = parts[1]
            self.seconds = parts[2]
        elif len(parts) == 2:
            self.minutes = parts[0]
            self.seconds = parts[1]
        else:
            raise ValueError("Length not proper format: {}".format(length))

    def get_hours(self):
        return self.hours

    def get_minutes(self):
        return self.hours * 60 + self.minutes

    def get_seconds(self):
        return self.get_minutes() * 60 + self.seconds


class Song:

    def __init__(self, title="Unknown", artist="Unknown", album="Unknown", length="0"):
        self.title = title
        self.artist = artist
        self.album = album
        self.length = length

    def __str__(self):
        message = "{} - {} from {} - {}"
        result = message.format(
            self.artist, self.title, self.album, self.length)
        return result

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __hash__(self):
        return hash(self.__str__())

    def json_prep(self):
        return {
            key: self.__dict__[key]
            for key in self.__dict__ if not key.startswith("_")
            }

    def length(self, argument):
        list_length = self.length.split(":")

        if argument == "seconds":
            return int(list_length[0]) * 60 + int(list_length[1])

        elif argument == "minutes":
            return int(list_length[0])

        elif argument == "hours":
            return int(list_length[0]) // 60

        else:
            return self.length


class Playlist:

    def __init__(self, name, repeat=False, shuffle=False):
        self.name = name
        self.repeat = repeat
        self.shuffle = shuffle
        self.__current_song_index = 0
        self.__shuffle_played_songs = set()
        self.playlist = []

    def __str__(self):
        return str(self.playlist)

    def __repr__(self):
        return self.playlist.__str__()

    def add_song(self, song):
        self.playlist.append(song)

    def remove_song(self, song):
        try:
            self.playlist.remove(song)
        except ValueError:
            pass

    def add_songs(self, s_list):
        self.playlist.append(s_list)

    def total_length(self):
        total = 0
        for song in self.playlist:
            total += song.length

    def artists(self):
        all_artists = [song.artist for song in self.__songs]
        return {name: all_artists.count(name) for name in all_artists}

    def has_next_song(self):
        return self.__current_song_index < len(self.playlist)

    def next_song(self):
        if self.repeat == "SONG":
            return self.playlist[self.__current_song_index]

        if self.shuffle:
            return self.__shuffle()

        if not self.has_next_song() and self.repeat == "NONE":
            raise Exception("End of playlist")

        if not self.has_next_song() and self.repeat == "PLAYLIST":
            self.__current_song_index = 0

        song = self.playlist[self.__current_song_index]
        self.__current_song_index += 1

        return song

    def shuffle(self):
        song = random.choice(self.playlist)

        while song in self.__shuffle_played_songs:
            song = random.choice(self.playlist)

        self.__shuffle_played_songs.add(song)

        if len(self.__shuffle_played_songs) == len(self.playlist):
            self.__shuffle_played_songs = set()

        return song

    def prepare_for_json(self):
        info = {
            "name": self.name,
            "songs": [s.json_prep() for s in self.playlist]
        }
        return info

    def toJson(self):
        return json.dumps(self.prepare_for_json(), indent=True)

    def save(self, indent=True):
        filename = self.name.replace(" ", "-") + ".json"

        with open(filename, "w") as f:
            f.write(self.toJson())

    @staticmethod
    def load(filename):
        with open(filename, "r") as f:
            contents = f.read()
            data = json.loads(contents)
            pl = Playlist(data["name"])

            for dict_song in data["songs"]:
                song = Song(artist=dict_song["artist"],
                            title=dict_song["title"], album=dict_song["album"],
                            length=dict_song["length"])
                pl.add_song(song)
            return pl


class MusicCrawler:

    def __init__(self, path):
        self.path = path

    def crawl(self):
        pass
