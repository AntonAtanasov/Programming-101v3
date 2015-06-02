from PandaBook import Panda
from PandaBook import SocialNetwork
from PandaBook import PandaAlreadyThere
import unittest


class PandaTest(unittest.TestCase):
    def setUp(self):
        self.test_acc = Panda("Anton", "anton@mail.bg", "male")

    def test_init(self):
        self.assertTrue(isinstance(self.test_acc, Panda))

    def test_str(self):
        message = "Profile for {} ({}). For contacts : {}"
        result = message.format(self.test_acc.name, self.test_acc.gender, self.test_acc.email)
        self.assertEqual(str(self.test_acc), result)

    def test_isMale(self):
        self.assertTrue(self.test_acc.isMale())

    def test_isFemale(self):
        self.assertFalse(self.test_acc.isFemale())

    def test_hash(self):
        self.assertTrue(isinstance(hash(self.test_acc.email), int))


class SocialNetworkTest(unittest.TestCase):
    def setUp(self):
        self.ivo = Panda("Ivo", "ivo@pandamail.com", "male")
        self.rado = Panda("Rado", "rado@pandamail.com", "male")
        self.tony = Panda("Tony", "tony@pandamail.com", "female")

    def test_add_panda(self):
        with self.assertRaises(PandaAlreadyThere):
            SocialNetwork.add_panda(self.ivo)

    def test_has_panda(self):
        pass


if __name__ == '__main__':
    unittest.main()
