import unittest
from config import app
import index as api
import utils

class TestApi(unittest.TestCase):

    app.config['ENV'] = 'TESTING'
    # def test_endpoints(self):
    #     self.assertEqual(api.hello_world(), 'hello all possible worlds --- -- - ***')

    def test_utils(self):
        # allowing files types
        self.assertTrue(utils.allowed_file('filename.jpg'))
        self.assertFalse(utils.allowed_file('filename.gif'))
        self.assertTrue(utils.allowed_file('filename.png'))
        self.assertFalse(utils.allowed_file('filename.pdf'))

        # search file function
        self.assertTrue(utils.find_file('1.jpg'))
        self.assertTrue(utils.find_file('2.jpg'))
        self.assertFalse(utils.find_file('3.jpg'))

        # download function
        file = utils._download('https://external-content.duckduckgo.com/iu/?u=http%3A%2F%2F2.bp.blogspot.com%2F-WtdFq_e6eKo%2FTV5W5s-hS-I%2FAAAAAAAAAvM%2FgmCUYOx3bX8%2Fs1600%2FAnimals_Cats_Small_cat_005241_.jpg&f=1&nofb=1')
        self.assertTrue(file['success'])
        self.assertEqual(file['name'], file['name'])

        # remove function
        self.assertTrue(utils.remove_file(file['name']))
        self.assertFalse(utils.remove_file('randomanme.jpg'))

        # predict function
        self.assertEqual(utils.make_prediction('1.jpg'), 'dog')
        self.assertEqual(utils.make_prediction('2.jpg'), 'cat')
        

if __name__ == '__main__':
    unittest.main()