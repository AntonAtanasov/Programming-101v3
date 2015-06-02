from MusicPlayer import Song
import unittest


class SongTest(unittest.TestCase):

    def setUp(self):
        self.my_song = Song(
            title="Odin", artist="Manowar",
            album="The Sons of Odin", length="3:44")

    def test_init(self):
        self.assertTrue(isinstance(self.my_song, Song))

    def test_str(self):
        message = "{} - {} from {} - {}"
        result = message.format(
            self.my_song.artist, self.my_song.title, self.my_song.album,
            self.my_song.length)
        self.assertEqual(str(self.my_song), result)

    def test_eq(self):
        other_song = Song()
        self.assertFalse(self.my_song == other_song)

    def test_song_length(self):
        self.assertTrue(isinstance(str(self.my_song.length), str))

if __name__ == '__main__':
    unittest.main()
