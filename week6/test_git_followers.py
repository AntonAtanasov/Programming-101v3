import unittest
from git_followers import GitHubSocial, NoSuchUserinCurrentSocLevel


class TestGitHubSocial(unittest.TestCase):

    def test_get_network_for(self):
        self.assertEqual(len(GitHubSocial.get_network_for('RadoRado')['followers']), 216)
        self.assertEqual(len(GitHubSocial.get_network_for('RadoRado')['following']), 77)

    def test_build_github_social(self):
        with self.assertRaises(ValueError):
            GitHubSocial.build_github_social('presianbg', 99)

        my_net = GitHubSocial('presianbg', 0)
        print(my_net)

    def test_do_you_follow(self):
        my_net = GitHubSocial('presianbg', 0)
        self.assertTrue(my_net.do_you_follow('sevgo'))
        self.assertFalse(my_net.do_you_follow('torvalds'))

    def test_do_you_follow_indirectly(self):
        my_net = GitHubSocial('presianbg', 1)
        self.assertTrue(my_net.do_you_follow_indirectly('torvalds'))
        self.assertFalse(my_net.do_you_follow_indirectly('awefwe'))

    def test_does_he_she_follows(self):
        my_net = GitHubSocial('presianbg', 0)
        self.assertTrue(my_net.does_he_she_follows('AnetaStoycheva'))
        self.assertFalse(my_net.does_he_she_follows('ArchangeGabriel'))
        with self.assertRaises(NoSuchUserinCurrentSocLevel):
            self.assertFalse(my_net.does_he_she_follows('torvalds'))

    def test_does_he_she_follows_indirectly(self):
        my_net = GitHubSocial('presianbg', 1)
        self.assertTrue(my_net.does_he_she_follows_indirectly('RadoRado'))
        with self.assertRaises(NoSuchUserinCurrentSocLevel):
            my_net.does_he_she_follows_indirectly('alabala-nica')

    def test_who_follows_you_back(self):
        my_net = GitHubSocial('presianbg', 0)
        print(my_net.who_follows_you_back())
